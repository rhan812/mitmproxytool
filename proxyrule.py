#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
mitmproxy 规则处理
"""
import random
import json
import time


class ProxyRule:
    def __init__(self, req_json):
        # 真实的响应结果
        self.req_json = eval(req_json)

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
        return json.dumps(value)

    def intercept_response_part(self, value):
        """
        篡改部分返回值
        :return:
        """
        pass

    def not_intercept(self, _):
        """
        不篡改返回值
        :return:
        """
        return json.dumps(self.req_json)

    def delay_response_time(self, value=5):
        """
        返回数据延迟处理
        :return:
        """
        time.sleep(value)
        print("delay_respones_time:{}ms".format(value))
        return json.dumps(self.req_json)

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
