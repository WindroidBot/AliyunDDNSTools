AliyunDDNSTools
===
基于阿里云的DDNS自动更新工具<br>
## 运行环境<br>
1、Python3<br>
2、Aliyun Python SDK Core https://pypi.org/project/aliyun-python-sdk-core-v3/<br>
3、Aliyun Python SDK for AliDNS https://pypi.org/project/aliyun-python-sdk-alidns/<br>
4、Aliyun Python SDK for Domain https://pypi.org/project/aliyun-python-sdk-domain-intl/<br>
## 运行方式<br>
首先手动创建userconfigure.json，格式如下：<br>
{<br>
>>>"accessKeyId": "Your accessKeyId",<br>
>>>"accessSecret": "Your accessSecret",<br>
>>>"domainName": "Your domainName"<br>
}<br>
然后修改源代码中userConfigPath变量的值为userconfigure.json的路径
