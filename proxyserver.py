#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
使用 mitmproxy 修改响应
"""
import sys
import os
import yaml

from proxyrule import ProxyRule

from mitmproxy import flowfilter, http, ctx
from operator import methodcaller


class ProxyServer:
    def __init__(self, rulepath):
        self.rulepath = rulepath
        with open(self.rulepath, encoding='UTF-8') as f:
            self.proxy_rules = yaml.safe_load(f)
        self.globle_filter = self.proxy_rules.get("filter", None)
        self.rules = self.proxy_rules.get("rules", [])
        self.redirect = self.proxy_rules.get("redirect", None)
        self.filepath = os.path.dirname(self.rulepath)

    def request(self, flow):
        """
        :param flow:
        :return:
        """
        request = flow.request
        # 开始访问全局过滤器，只有满足才会进入
        if flowfilter.match(self.globle_filter, flow) or self.globle_filter is None:
            if self.redirect:
                flow.request.host = self.redirect.split(":")[0] if ":" in self.redirect else self.redirect
                flow.request.port = int(self.redirect.split(":")[-1] if ":" in self.redirect else flow.request.port)
            ctx.log.info("========================== 开始 拦截请求 ==========================")
            ctx.log.info("========================== host is:{} ========================== ".format(request.host))
            ctx.log.info("========================== url is:{} ========================== ".format(request.pretty_url))
            ctx.log.info("========================== path is:{} ========================== ".format(request.path))
            ctx.log.info("========================== method is:{} ========================== ".format(request.method))
            ctx.log.info("========================== body is:{} ========================== ".format(request.get_text()))
            ctx.log.info("========================== intercept request end ==========================")

    def response(self, flow):
        """
        篡改 response返回数据
        :param flow:
        :return:
        """
        if flowfilter.match(self.globle_filter, flow) or self.globle_filter is None:
            for rule in self.rules:
                if rule.get("filter"):
                    if flowfilter.match(rule.get("filter"), flow):
                        redirect_http(flow, rule, self.filepath)
                else:
                    redirect_http(flow, rule, self.filepath)


def redirect_http(flow, rule, filepath):
    original_data = flow.response.text
    if rule.get("urlpath") == flow.request.path:
        ctx.log.info("========================== 开始 篡改返回值 ==========================")
        ctx.log.info("========================== 原始值 is： {} ==========================".format(original_data))
        if rule.get("ruleName") == "intercept_status_code":
            code, resp_value = methodcaller(rule.get("ruleName"), rule.get("ruleValue"))(ProxyRule(original_data, filepath))
            flow.response = http.HTTPResponse.make(code,  # (optional) status code
                                                   resp_value,  # (optional) content
                                                   {"Content-Type": "text/html"}  # (optional) headers
                                                   )
        else:
            response_value = methodcaller(rule.get("ruleName"), rule.get("ruleValue"))(ProxyRule(original_data, filepath))
            flow.response.set_text(response_value)
        ctx.log.info("========================== 篡改后的返回值 is： {} ==========================".format(flow.response.get_text()))
        ctx.log.info("========================== intercept response end ==========================")
    else:
        ctx.log.info("========================== 未匹配到需要篡改的URL: {}==========================".format(rule.get("urlpath")))


def start():
    if len(sys.argv) != 2:
        print("未传入规则路径，则获取当前路径")
        rule_path = os.path.join(os.getcwd(), "proxyrule.yaml")
    else:
        rule_path = sys.argv[0]

    return ProxyServer(rule_path)


addons = [
    start()
]
