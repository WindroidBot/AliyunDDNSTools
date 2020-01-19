from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
import json
import os
import sys
from commonModule import *

userConfigPath = "C:/Users/windr/Documents/userInfo.json"

UserConfig = ReadUserConfig(userConfigPath)
domainName = UserConfig['domainName']

client = GetAliyunClient(userConfigPath)

request = DescribeDomainRecordsRequest()
request.set_accept_format('json')

request.set_DomainName(domainName)

result = ExecuteGetResults(client,request)
print(result)