#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
使用 mitmproxy 修改响应
"""
import json
import os
import yaml
import typing

from proxyrule import ProxyRule

import mitmproxy.http
from mitmproxy import ctx
from mitmproxy import exceptions
from operator import methodcaller


class RedirectRequests:
    def __init__(self):
        self.host = ''

    def load(self, loader):
        loader.add_option(
            name="redirectrequest",
            typespec=typing.Optional[str],
            default=None,
            help="重定向请求"
        )

    def configure(self, updates):
        if "redirectrequest" in updates:
            if ctx.options.redirectrequest == '':
                raise exceptions.OptionsError("重定向的host不能为空")

    def request(self, flow: mitmproxy.http.HTTPFlow):
        """
        :param flow:
        :return:
        """
        request = flow.request
        ctx.log.info("========================== 开始 拦截请求 ==========================")
        ctx.log.info("========================== host is:{} ========================== ".format(request.host))
        ctx.log.info("========================== url is:{} ========================== ".format(request.pretty_url))
        ctx.log.info("========================== path is:{} ========================== ".format(request.path))
        ctx.log.info("========================== method is:{} ========================== ".format(request.method))
        ctx.log.info("========================== body is:{} ========================== ".format(request.get_text()))
        ctx.log.info("========================== 结束 拦截请求 ==========================")
        # 控制是否真实访问
        if ctx.options.redirectrequest is not None:
            flow.request.host = str(ctx.options.redirectrequest)


class SendFromProxy:
    def load(self, loader):
        loader.add_option(
            name="sendfromproxy",
            typespec=typing.Optional[str],
            default=None,
            help="不从远程服务获取数据直接从代理"
        )

    def configure(self, updates):
        pass

    def request(self, flow: mitmproxy.http.HTTPFlow):
        """
        :param flow:
        :return:
        """
        request = flow.request
        ctx.log.info("========================== 开始 拦截请求 ==========================")
        ctx.log.info("========================== host is:{} ========================== ".format(request.host))
        ctx.log.info("========================== url is:{} ========================== ".format(request.pretty_url))
        ctx.log.info("========================== path is:{} ========================== ".format(request.path))
        ctx.log.info("========================== method is:{} ========================== ".format(request.method))
        ctx.log.info("========================== body is:{} ========================== ".format(request.get_text()))
        ctx.log.info("========================== 结束 拦截请求 ==========================")
        # 控制是否真实访问
        if ctx.options.sendfromproxy is not None:

            flow.response = mitmproxy.http.HTTPResponse.make(
                200,  # (optional) status code
                json.dumps(ctx.options.sendfromproxy, ensure_ascii=False),  # (optional) content
                {"Content-Type": "text/html"}  # (optional) headers
            )


class ProxyServer:
    def __init__(self):
        self.rules = []

    def load(self, loader):
        loader.add_option(
            name="rulepath",
            typespec=str,
            default=os.path.join(os.getcwd(), "proxyrule.yaml"),
            help="篡改规则文件"
        )

    def configure(self, updates):
        if "rulepath" in updates:
            if ctx.options.rulepath is None:
                raise exceptions.OptionsError("规则文件不能为空, 请输入规则路径")

    def request(self, flow: mitmproxy.http.HTTPFlow):
        """
        :param flow:
        :return:
        """
        request = flow.request
        ctx.log.info("========================== 开始 拦截请求 ==========================")
        ctx.log.info("========================== host is:{} ========================== ".format(request.host))
        ctx.log.info("========================== url is:{} ========================== ".format(request.pretty_url))
        ctx.log.info("========================== path is:{} ========================== ".format(request.path))
        ctx.log.info("========================== method is:{} ========================== ".format(request.method))
        ctx.log.info("========================== body is:{} ========================== ".format(request.get_text()))
        ctx.log.info("========================== intercept request end ==========================")

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """
        篡改 response返回数据
        :param flow:
        :return:
        """

        original_data = flow.response.text
        ctx.log.info("========================== 开始 篡改返回值 ==========================")
        ctx.log.info("========================== 原始值 is： {} ==========================".format(original_data))
        with open(ctx.options.rulepath, encoding='UTF-8') as f:
            self.rules = yaml.safe_load(f)

        for rule in self.rules:
            if rule.get("urlpath") == flow.request.path:
                if rule.get("ruleName") == "intercept_status_code":
                    code, resp_value = methodcaller(rule.get("ruleName"), rule.get("ruleValue"))(ProxyRule(original_data))
                    flow.response = mitmproxy.http.HTTPResponse.make(code,  # (optional) status code
                                                                     resp_value,  # (optional) content
                                                                     {"Content-Type": "text/html"}  # (optional) headers
                                                                    )
                else:
                    response_value = methodcaller(rule.get("ruleName"), rule.get("ruleValue"))(ProxyRule(original_data))
                    flow.response.set_text(response_value)
        ctx.log.info("========================== 篡改后的返回值 is： {} ==========================".format(flow.response.get_text()))
        ctx.log.info("========================== intercept response end ==========================")


addons = [
    RedirectRequests(),
    SendFromProxy(),
    ProxyServer()
    ]
