# whatplatform 1.0
=====================
platform指网站的开发语言类型，whtatplatform是用来快速识别网站开发语言的工具,当前定义了java,asp,asp.net,php四种类型.

## 两种识别platform的方式
----------------------------------

### 通过网站动态页面后缀与开发语言对应关系识别:
网站动态页面后缀与platform关系定义
* asp: 
  - .asp
* asp.net:
  - .aspx .asmx .ashx .axd
* php: 
  - .php
* java: 
  - .jspx .jsp .do .action

### 通过HTTP-HEADER特定字段内容识别:
通过Server、Set-Cookie、X-Powered-By这3个字段中的特定关键字来识别网站开发语言,其规则定义:
* Server:
  - "Apache-Coyote" -> java
* Set-Cookie:
  - "JSESSIONID=" -> java
  - "PHPSESIONID=" -> php
  - "ASPSESSIONID=" -> asp
  - "ASP.NET_SessionId=" -> asp.net
* X-Powered-By:
  - "JBoss" -> java
  - "JSP/" -> java
  - "Servlet" -> java
  - "PHP/" -> php


## 网站动态页面后缀获取使用两种方式
------------------------------------
* 通过抓取网站首页的内部链接获得动态后缀;
* 通过枚举网站常见动态页面确定动态页面后缀;

<br>


# confuse me
=================
1) HTTP-HEADER判断platform的一个问题：是不是同一个网站所有页面的HTTP-HEADER中的Server/Set-Cookie/X-Powered-By字段是一致的呢？

2) Server和X-Powered-By中存在"PHP/"能否判断为php？
* 理论上引起误差主要有:
  - 反向代理导致前置服务器的HEADER不能作判断依据;
  - 虚拟主机X-Powered-By同时包含ASP.NET和PHP;

* 实际验证：
  - 当前验证在896个java网站中有1个Server存在"PHP/",0个X-Powered-By中存在"PHP/".
    - 并有1个网站原数据错误,网站当为php.
  - 当前验证在903个asp.net网站中有0个Server存在"PHP/",0个X-Powered-By中存在"PHP/".
    - 并有5个网站原数据错误,网站当为php.
  - 当前验证在2350个asp网站中有0个Server存在"PHP/",0个X-Powered-By中存在"PHP/".
    - 并有11个网站原数据错误,网站当为php.
 







