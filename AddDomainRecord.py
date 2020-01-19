#增加主机记录
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
import json
import os
import sys
from commonModule import *

userConfigPath = "C:/Users/windr/Documents/userInfo.json"

UserConfig = ReadUserConfig(userConfigPath)
domainName = UserConfig['domainName']

client = GetAliyunClient(userConfigPath)

request = AddDomainRecordRequest()
request.set_accept_format('json')

#设置增加记录的信息
request.set_DomainName(domainName)
request.set_RR("test5")
request.set_Type("A")
request.set_Value("4.5.6.7")

result = ExecuteGetResults(client,request)
print(result)
