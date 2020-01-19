#根据主机记录删除记录
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
import json
import os
import sys
from commonModule import *

userConfigPath = "C:/Users/windr/Documents/userInfo.json"

UserConfig = ReadUserConfig(userConfigPath)
domainName = UserConfig['domainName']

client = GetAliyunClient(userConfigPath)

request = DeleteSubDomainRecordsRequest()
request.set_accept_format('json')

#设置待删除记录的信息
request.set_DomainName(domainName)
request.set_RR("host")

result = ExecuteGetResults(client,request)
print(result)