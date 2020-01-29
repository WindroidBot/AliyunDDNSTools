import json
import os
import sys
from commonModule import *

domainConfigPath = "C:/Users/windr/Documents/domainInfo.json"
userConfigPath = "C:/Users/windr/Documents/userInfo.json"
domainConfig = ReadConfig(domainConfigPath, 'r')
UserConfig = ReadConfig(userConfigPath, 'r')

domainName = UserConfig['domainName']
client = GetAliyunClient(userConfigPath)

RemoteList_RecordIdRRValue = GetRemoteRecordsIpAddress()
publicAddress = GetPublicIpAddress()

#UpdateAliyunDNSRecord
def UpdateAliyunDNSRecord():
    for i in range(len(domainConfig['Record'])):
        local_RR = domainConfig['Record'][i]['RR']
        local_Type = domainConfig['Record'][i]['Type']
        local_RecordId = domainConfig['Record'][i]['RecordId']
        local_Line = domainConfig['Record'][i]['Line']

        print("---------------------------------------------------")
        #local_RecordId为空，则添加记录
        if local_RecordId == "":
            #print("第"+i+"个数据RecordId为空")
            try:            
                AddDomainRecord = AddDomainRecordHelper(client, domainName, local_RR, local_Type, publicAddress, local_Line)
                RecordId = json.loads(AddDomainRecord)['RecordId']
                print("DNS记录添加成功："+RecordId+" | "+local_RR+"."+domainName+" | "+local_Type+" | "+publicAddress+" | "+local_Line)
            except:
                print("DNS记录添加失败：", sys.exc_info()[0])
            '''
            将修改过的新RecordId回写进userConfig中
            '''
            domainConfigDirt = ReadConfig(domainConfigPath, 'r')
            domainConfigDirt['Record'][i]['RecordId'] = json.loads(AddDomainRecord)['RecordId']
            with open(domainConfigPath, 'w+') as domainConfig_newJson:
                json.dump(domainConfigDirt, domainConfig_newJson ,indent=4)
            continue
        elif isRecordExistAndNotEqual(local_RecordId, RemoteList_RecordIdRRValue):
            try:
                UpdateDomainRecordHelper(client, local_RecordId, local_RR, local_Type, publicAddress, local_Line)
                print("更新记录成功local_RecordId："+local_RecordId)
            except:
                print("更新记录失败local_RecordId："+local_RecordId, sys.exc_info()[0])
    print("---------------------------------------------------")
    print("动态DNS更新地址完成")

#根据本地记录的RecordId在云端查找是否已存在该记录且是否不相等（此时需要修改）,False表示无需更改，True表示需要更新数据
def isRecordExistAndNotEqual(LocalRecordIdStr, RemoteList):
    for i in range(len(RemoteList)):
        if LocalRecordIdStr == RemoteList[i]['Remote_RecordId']:
            print("LocalRecordId："+LocalRecordIdStr+"存在")
            if publicAddress == RemoteList[i]['Remote_Value']:
                print("云端记录地址为"+publicAddress+"与本地相同，无需更改")
                return False
            else:
                print("云端记录地址为"+RemoteList[i]['Remote_Value']+"与当前公网地址"+publicAddress+"不相同，需更改")
                return True
    print("LocalRecordId："+LocalRecordIdStr+"不存在")
    return False

UpdateAliyunDNSRecord()