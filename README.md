AliyunDDNSTools
===
基于阿里云的DDNS自动更新工具<br>
## 运行环境<br>
1、Python3<br>
2、Aliyun Python SDK Core https://pypi.org/project/aliyun-python-sdk-core-v3/<br>
3、Aliyun Python SDK for AliDNS https://pypi.org/project/aliyun-python-sdk-alidns/<br>
4、Aliyun Python SDK for Domain https://pypi.org/project/aliyun-python-sdk-domain-intl/<br>
5、APScheduler https://pypi.org/project/APScheduler/<br>
## 运行方式<br>
首先手动创建userconfigure.json，用于存储身份验证信息以及操作的主域名，格式如下：<br>
若要使用地址改变邮件提醒功能，请将remind下的enable设置为true，并且正确配置邮件信息，receivers可以定义多个收件人
```json
{
  "accessKeyId": "Your accessKeyId",
  "accessSecret": "Your accessSecret",
  "domainName": "Your domainName",
  "remind":{
		"enable": "true or false",
		"smtp_host": "Yor SMTP Server",
		"smtp_user": "Your Mail user name",
		"smtp_pass": "Your Mail password",
		"sender": "sender E-Mail Address",
		"receivers":[
			"receivers1 E-Mail Address",
      "receivers2 E-Mail Address",
      "More E-Mail Address"
		]
	}
}
```
然后修改源代码中userConfigPath变量的值为userconfigure.json的路径<br>
再创建domainInfo.json，用于存储需要解析的二级域名具体配置，格式如下：<br>
```json
{
    "IPaddr": "",
    "Record": [
        {
            "RR": "Your HostName",
            "RecordId": "",
            "Type": "A",
            "DomainName": "Your domainName",
            "Locked": false,
            "Line": "default",
            "TTL": 600
        },
        {
            "RR": "Your HostName",
            "RecordId": "",
            "Type": "A",
            "DomainName": "Your domainName",
            "Locked": false,
            "Line": "default",
            "TTL": 600
        }
     ]
 }
```
然后修改源代码中domainConfigPath变量的值为domainInfo.json的路径<br>
其中，IPaddr为当前公网地址，第一次运行保持空即可。RR为二级域名，RecordId保持为空且以后也不要修改，Type为DNS记录类型，DomainName为主域名，Line为解析线路枚举，保持默认即可，具体可参考阿里云文档[解析线路枚举](https://help.aliyun.com/document_detail/29807.html?spm=a2c4g.11186623.2.16.1fce2846njgztT)，TTL为解析生效时间，可根据所购买产品填写，免费版以及默认生效时间是600秒<br>
可根据需要自己添加更多子域名<br>
