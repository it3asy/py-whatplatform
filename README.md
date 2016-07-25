# whatplatform 1.0
=====================
platform指网站的开发语言类型，当前定义了java,asp,asp.net,php四种类型. whtatplatform是用来快速识别网站开发语言的工具.

## 两种识别platform的方式
* 通过网站动态页面后缀；
* 通过HTTP HEADER识别;

## 网站动态页面后缀与platform关系定义
> asp: .asp,
> asp.net: .aspx, .asmx, .ashx, .axd,
> php: .php,
> java: .jspx, .jsp, .do, .action,

## 网站动态页面后缀获取使用两种方式
* 通过首页抓取动态后缀;
* 通过枚举常见页面确定网站动态页面后缀;

## HTTP HEADER头部识别通过3个固定字段Server, X-Powered-By, Set-Cookie.
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


## confuse me
=================
1) HTTP HEADER判断platform的一个问题：是不是同一个网站所有页面的HTTP-HEADER中的那几个识别字段是一致的呢？

2) Server和X-Powered-By中存在"PHP/"能否判断为php？
* 理论上引起误差主要有:
  - 反向代理导致前置服务器的HEADER不能作判断依据;
  - 虚拟主机X-Powered-By同时包含ASP.NET和PHP;

实际验证：
  - 当前验证在896个java网站中有1个Server存在"PHP/",0个X-Powered-By中存在"PHP/".
    - 并有1个网站原数据错误,网站当为php.
  - 当前验证在903个asp.net网站中有0个Server存在"PHP/",0个X-Powered-By中存在"PHP/".
    - 并有5个网站原数据错误,网站当为php.
  - 当前验证在2350个asp网站中有0个Server存在"PHP/",0个X-Powered-By中存在"PHP/".
    - 并有11个网站原数据错误,网站当为php.
 







