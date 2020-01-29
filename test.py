import json
import os
import sys
from commonModule import *

userConfigPath = "C:/Users/windr/Documents/userInfo.json"
UserConfig = ReadConfig(userConfigPath, 'r')

domainName = UserConfig['domainName']

client = GetAliyunClient(userConfigPath)

#DescribeDomainRecordsRequestHelper(client,domainName)
#AddDomainRecordHelper(client, domainName, "qwe", "A", "1.2.3.4", "default")
#UpdateDomainRecordHelper(client, "19051380032864256", "bbb", "A", "8.8.8.8", "default")
#DescribeDomainRecordsRequestHelper(client,domainName)
GetRemoteRecordsIpAddress()