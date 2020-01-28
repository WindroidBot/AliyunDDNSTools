import json
import os
import sys
from commonModule import *

domainConfigPath = "C:/Users/windr/Documents/domainInfo.json"
domainConfig = ReadConfig(domainConfigPath)
print(type(domainConfig))
for i in range(len(domainConfig['Record'])):
    local_RR = domainConfig['Record'][i]['RR']
    local_Type= domainConfig['Record'][i]['Type']
    local_Value= GetPublicIpAddress()
    local_Line= domainConfig['Record'][i]['Line']
    print(local_RR+","+local_Type+","+local_Value+","+local_Line+"\n")
    

#responseDict = json.dumps(domainConfig,indent=4)
#print(responseDict)

#UpdateRecord
