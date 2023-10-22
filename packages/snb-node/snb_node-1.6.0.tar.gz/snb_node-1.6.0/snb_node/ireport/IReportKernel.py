import json
import sys
import time
from typing import Union, Optional, Awaitable, Dict, Any

import requests
import tornado.websocket
from tornado import gen, web
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from jupyter_client.jsonutil import json_default
import snb_plugin.utils.snb_RSA as snb_rsa
from snb_plugin.utils.snb_kernel_client import SnbKernelClient
from snb_plugin.graph.ToGraph import parsePara, toGraph
from snb_node.config.Config import SNB_SERVER_URL, config, pem, workspace_uid, envir_uid


# 系统缓存
client_cache = {}


class CellRunError(Exception):
    pass


def dep_search(output_cell_uid, edge_dict):
    res_list = []
    for output_uid in output_cell_uid:
        if output_uid in edge_dict:
            res_list.extend(edge_dict[output_uid])
            res_list.extend(dep_search(edge_dict[output_uid], edge_dict))
    return list(set(res_list))


def dep_process(snb, init_cell_uid, input_cell_uid, input_para, output_cell_uid):
    cell_data = parsePara(snb)
    graph_data = toGraph(cell_data)

    node_dict = {}
    edge_dict = {}
    for node in graph_data["node"]:
        node_dict[node["cell_uid"]] = node
    for edge in graph_data["edge"]:
        if edge["dst_uid"] in edge_dict:
            edge_dict[edge["dst_uid"]].append(edge["src_uid"])
        else:
            edge_dict[edge["dst_uid"]] = [edge["src_uid"]]

    dep_cell_uid = dep_search(output_cell_uid, edge_dict)
    try:
        for cell_uid in dep_cell_uid:
            node_dict[cell_uid]["is_exec"] = "dep"

        for cell_uid in init_cell_uid:
            if not cell_uid:
                continue
            node_dict[cell_uid]["is_exec"] = "init"

        for cell_uid_index, cell_uid in enumerate(input_cell_uid):
            node_dict[cell_uid]["is_exec"] = "input"
            node_dict[cell_uid]["input_cell_code"] = input_para[cell_uid_index]

        for cell_uid in output_cell_uid:
            node_dict[cell_uid]["is_exec"] = "output"
            node_dict[cell_uid]["is_out"] = "output"
    except KeyError as e:
        raise CellRunError(f"运行失败，单元格不存在{str(e)}")

    return graph_data


def get_notebook(snb_uid, preview=""):
    url = "".join([SNB_SERVER_URL, "/api/snb_native/nbver_last/" + snb_uid, "?preview="+preview])
    sign_str = snb_rsa.sign("/api/snb_native/nbver_last/" + snb_uid+"?preview="+preview, pem)
    header = {"Cookie": "cookie", "sign": sign_str, "workspaceUid": workspace_uid}
    conn_info = requests.get(url, headers=header)
    resp = conn_info.json()
    if resp["code"] == 200:
        snb = json.loads(resp["data"])
        return snb
    else:
        raise Exception("Notebook版本不存在")


class IReportKernelHandler(web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    # @interceptor
    def post(self, ws_uid) -> {"GRADE": ["BASIC", "PRO", "ENT"], "ROLE": ["ADMIN", "EDITOR"]}:
        try:
            body = json.loads(self.request.body.strip().decode("utf-8"))
            snb_uid = body.get("snb_uid")
            kernel_id = body.get("kernel_id", "")
            init_cell_uid = body.get("init_cell_uid", [])
            input_cell_uid = body.get("input_cell_uid", [])
            input_para = body.get("input_para", [])
            output_cell_uid = body.get("output_cell_uid", [])
            preview = body.get("preview", "")

            snb = get_notebook(snb_uid, preview)

            dep_res = dep_process(snb, init_cell_uid, input_cell_uid, input_para, output_cell_uid)
            #print(json.dumps(dep_res), file=sys.stderr)
            client, kernel_id = yield self.connect_client(kernel_id=kernel_id, dep_res=dep_res, snb_uid=snb_uid)
            output_res,error_res = yield self.get_output(client=client, dep_res=dep_res)
            res = {"code": 200, "msg": "成功", "data": {"result": output_res, "kernel_id": kernel_id,"error_res":error_res}}
            self.finish(json.dumps(res, default=json_default))
        except CellRunError as e:
            print(e,file=sys.stderr)
            res = {"code": 400, "msg": "失败:" + str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))
        except Exception as e:
            print(e,file=sys.stderr)
            res = {"code": 400, "msg": "失败:" + str(e), "data": []}
            self.finish(json.dumps(res, default=json_default))

    @run_on_executor
    def get_output(self, client, dep_res):
        """执行关联代码的output"""
        output_res = {}
        error_res=[]
        for node in dep_res["node"]:
            is_exec=node.get("is_exec", "")
            if is_exec == "input" or is_exec == "dep" or is_exec == "output":
                if node["cell_type"] == "sql":
                    res = client.execute(node["py_code"])
                else:
                    if node['snb_cell_type'].startswith("interact"):
                        res = client.execute(node["cell_code"])
                        if 'input_cell_code' in node :
                            client.execute(node["input_cell_code"])
                    else:
                        res = client.execute(node["cell_code"])
                for r in res:
                    if 'output_type' in r and r['output_type'] == 'error':
                        error_res.append({"node":node,"error":r})

                if node.get("is_out", "") == 'output':
                    output_res[node["cell_uid"]] = res
        return output_res,error_res

    @run_on_executor
    def connect_client(self, kernel_id, dep_res, snb_uid):
        """连接kernel"""
        key = snb_uid + "_" + kernel_id
        print(key, file=sys.stderr)

        if kernel_id and key in client_cache and client_cache[key].is_alive():
            client = client_cache[key]
            kernel_id = client.get_kernel_id()
            print('is_exist',key, file=sys.stderr)
        else:
            if kernel_id and key in client_cache:
                del client_cache[key]

            client = SnbKernelClient()
            print('not_exist', key, file=sys.stderr)

            kernel_id = client.startKernel()
            for node in dep_res["node"]:
                if node.get("is_exec", "") == "init":
                    if node["cell_type"] == "sql":
                        client.execute(node["py_code"])
                    else:
                        client.execute(node["cell_code"])
            key = snb_uid + "_" + kernel_id
            client_cache[key] = client
        return client, kernel_id

_conn_uid_regex = r"(?P<conn_uid>.*)"
_ws_uid = r"(?P<ws_uid>[^/]+)"
default_handlers = [
    (rf"/api/snb/node/ireportKernel/{_ws_uid}", IReportKernelHandler),
]
