# mitmproxytool

**介绍:**
    mitmproxy 可以用来拦截、修改、保存 HTTP/HTTPS 请求。
    本项目利用mitmproxy 的 scripting API 来自动拦截修改HTTP数据的目的。
    现在你无需编写任何py 脚本, 只需修改代理规则文件就可以使用
    
**安装说明：**

 1. 安装Python 3
 2. 安装 pip
 3. pip install requirements.txt

**使用说明：**

 1. 设置代理:
    postman: 百度 一下
    Browser: 百度一下
    Mobile: 百度一下
    默认端口: 8080
 2. 修改配置文件:
    urlpath: 需要拦截请求path
    ruleName: 规则名称
    ruleValue: 规则值

    规则名包含：
     intercept_response_all: 篡改全部返回值
     intercept_response_part: 篡改部分返回值
     not_intercept: 原值返回
     delay_response_time: 返回数据延迟处理
     intercept_status_code: 篡改返回状态码

 3. 开启代理工具:

    mitmdump -s proxyserver.py  或者  mitmdump -s xx/xx/proxyserver.py --set rulepath=xxxx/xxx/xx.yaml(没有gui模式)
    mitmweb -s proxyserver.py  或者  mitmdump -s xx/xx/proxyserver.py --set rulepath=xxxx/xxx/xx.yaml(启动web页面模式)

    mitmdump  -set sendfromproxy={}  # 不从远程服务获取数据直接从代理

    注：以上命令需要切换至 proxyserver.py文件所在目录

**TO DO:**
    **1. 篡改指定的值。**
    **2. 添加更多的功能。(可提需求)**
    **3. 重定向请求.(可定制，指定host 或者 完整的 url 进行重定向)**
