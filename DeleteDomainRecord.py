#根据RecordID删除记录
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
import json
import os
import sys
from commonModule import *

userConfigPath = "C:/Users/windr/Documents/userInfo.json"

UserConfig = ReadUserConfig(userConfigPath)
domainName = UserConfig['domainName']

client = GetAliyunClient(userConfigPath)

request = DeleteDomainRecordRequest()
request.set_accept_format('json')

#设置待删除记录的RecordId
request.set_RecordId("19044300258808832")

result = ExecuteGetResults(client,request)
print(result)