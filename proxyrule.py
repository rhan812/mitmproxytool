#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
mitmproxy 规则处理
"""
import os
import re
import random
import yaml
import json
import time


class ProxyRule:
    def __init__(self, req_json, filepath):
        # 真实的响应结果
        self.req_json = eval(req_json)
        self.filepath = filepath

    def add_header(self):
        """
        修改头部信息
        :return:
        """
        pass

    def redirect_requests(self):
        """
        重定向请求
        :return:
        """
        pass

    def send_reply_from_proxy(self):
        """
        不从远程服务获取数据直接从代理
        :return:
        """
        pass

    def intercept_response_all(self, value):
        """
        篡改全部返回值
        :return:
        """
        return ProxyRule._regroup_response(value, self.filepath, self.req_json, False)

    def intercept_response_part(self, value):
        """
        篡改部分返回值
        :return:
        """
        return ProxyRule._regroup_response(value, self.filepath, self.req_json, True)

    def not_intercept(self, _):
        """
        不篡改返回值
        :return:
        """
        return json.dumps(self.req_json, ensure_ascii=False)

    def delay_response_time(self, value=5):
        """
        返回数据延迟处理
        :return:
        """
        time.sleep(value)
        print("delay_respones_time:{}ms".format(value))
        return json.dumps(self.req_json, ensure_ascii=False)

    def intercept_status_code(self, value=None):
        """
        篡改返回状态码
        :return:
        """
        resp_value = ''
        if value:
            status_code = value
        else:
            code_list = [404, 500, 503, 302, 301]
            status_code = random.choice(code_list)
        print("replace_status_code:{}".format(status_code))
        if status_code == 404:
            resp_value = "页面不存在"
        elif status_code == 500:
            resp_value = "服务异常"
        return status_code, resp_value

    @staticmethod
    def _regroup_response(value, filepath, originalValue, is_part=True):
        if isinstance(value, str):
            if value.endswith(".json"):
                # 读取 文件
                with open(os.path.join(filepath, "file", value), encoding='UTF-8') as f:
                    value_dict = yaml.load(f)
                # 判断是否部分修改
                if is_part:
                    value_ = json.dumps(dict(originalValue, **value_dict), ensure_ascii=False)
                else:
                    value_ = json.dumps(value, ensure_ascii=False)
            elif value.endswith(".html"):
                value_ = ''

        elif isinstance(value, dict):
            # 若设置某个 或多个值
            if is_part:
                for key, value in value.items():
                    if re.match('^\$\.|^DEL\.', key):
                        # 替換某個值
                        hierarchy_key = []
                        for key_ in re.sub(r'^\$\.|^DEL\.', "", key).split("."):
                            if '[' in key_ and ']' in key_:
                                hierarchy_key.append(key_)
                            else:
                                hierarchy_key.append("['{}']".format(str(key_)))
                        if key.startswith("$."):
                            if not isinstance(value, str):
                                exec_str = "originalValue" + "".join(hierarchy_key) + "={}".format(str(value))
                            else:
                                exec_str = "originalValue" + "".join(hierarchy_key) + "='{}'".format(value)
                        elif key.startswith("DEL."):
                            exec_str = "del originalValue" + "".join(hierarchy_key)
                            print(exec_str)
                        exec(str(exec_str))

                    else:
                        originalValue[key] = value
                value_ = json.dumps(originalValue, ensure_ascii=False)
            else:
                value_ = json.dumps(value, ensure_ascii=False)

        return value_




