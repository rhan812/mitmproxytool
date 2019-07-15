# mitmproxytool

**介绍:**
-------

>     mitmproxy 可以用来拦截、修改、保存 HTTP/HTTPS 请求。
>     本项目利用mitmproxy 的 scripting API 来自动拦截修改HTTP数据的目的。
>     现在你无需编写任何py 脚本, 只需修改代理规则文件就可以使用

**安装说明：**
---------

>  1. 安装Python 3
>  2. 安装 pip
>  3. pip install requirements.txt

**使用说明：**
---------

 1. 设置代理:

>     - postman: 百度 一下
>     - Browser: 百度一下
>     - Mobile: 百度一下
>     - 默认端口: 8080

 2. 规则配置文件:

>     filter: 过滤规则
>     redirect:  配置重定向URL, 配置了且 满足filter 重定向到配置的 url， 重定向后 规则集失效
>     urlpath: 需要拦截请求path
>     ruleName: 规则名称
>     ruleValue: 规则值 可以支持 str , dict, 文件(json 文件)
>         特殊配置
>         1. 设置值为具体的某个值 或者多个 值的格式。若有多层嵌套
>
>         例如：{"a":{"b":[{"c":1},{"c":2}]}} 设置方式 $.a.b.[0].c
>
>         2. 删除返回体中的某个 key {"DEL.key":""}
>
>     filter: 规则中的过滤
>
>     过滤规则：
>
>     {
>         "Request body": "~rb",
>         "Response body": "~bs",
>         "HTTP response code": "~c",
>         "Domain": "~d",
>         "Request header": "~hq",
>         "Response header": "~hs",
>         "Match HTTP flows": "~http",
>         "URL": "~u",
>         "Match destination address": "~dst",
>     }
>     具体: https://docs.mitmproxy.org/stable/concepts-filters/
>     书写方法:
>     ~d value & (~u value | ~d value)
>

    ** 规则名包含：**

>      intercept_response_all: 篡改全部返回值
>      intercept_response_part: 篡改部分返回值
>      not_intercept: 原值返回
>      delay_response_time: 返回数据延迟处理
>      intercept_status_code: 篡改返回状态码

 3. 开启代理工具:

>     mitmdump -s proxyserver.py  或者  mitmdump -s xx/xx/proxyserver.py xxxx/xxx/xx.yaml(没有gui模式)
>     mitmweb -s proxyserver.py  或者  mitmdump -s xx/xx/proxyserver.py xxxx/xxx/xx.yaml(启动web页面模式)


**TO DO:**
----------

>     1. 拦截的请求相关信息 保存至文件
>     2. locust 调用 拦截的请求进行性能测试


