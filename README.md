# AliyunDDNSTools
基于阿里云的DDNS自动更新工具<br>
首先手动创建userconfigure.json，格式如下：<br>
{<br>
"accessKeyId": "Your accessKeyId",<br>
"accessSecret": "Your accessSecret",<br>
"domainName": "Your domainName"<br>
}<br>
然后修改源代码中userConfigPath变量的值为userconfigure.json的路径
