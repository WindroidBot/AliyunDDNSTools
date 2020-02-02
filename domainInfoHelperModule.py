import json
import os
import sys
from commonModule import *
import logging

logging.config.fileConfig('log.conf')
logger = logging.getLogger('DomainInfoHelper')

domainConfigPath = "C:/Users/windr/Documents/domainInfo.json"
userConfigPath = "C:/Users/windr/Documents/userInfo.json"
domainConfig = ReadConfig(domainConfigPath, 'r')
UserConfig = ReadConfig(userConfigPath, 'r')

domainName = UserConfig['domainName']
client = GetAliyunClient(userConfigPath)

'''
获取所有云端记录的IP地址
格式为[{'Remote_RecordId':..., 'Remote_RR': ..., 'Remote_Value': ..., 'Remote_Line':...}, {...}]
'''
def GetRemoteRecordsIpAddress():
    UserConfig = ReadConfig(userConfigPath, 'r')
    domainName = UserConfig['domainName']
    client = GetAliyunClient(userConfigPath)
    DescribeDomainRecords = DescribeDomainRecordsRequestHelper(client, domainName)
    DescribeDomainRecordsJson = json.loads(DescribeDomainRecords)
    RemoteList_RecordIdRRValue = []
    for i in range(len(DescribeDomainRecordsJson['DomainRecords']['Record'])):
        Remote_RecordId = DescribeDomainRecordsJson['DomainRecords']['Record'][i]['RecordId']
        Remote_RR = DescribeDomainRecordsJson['DomainRecords']['Record'][i]['RR']
        Remote_Value = DescribeDomainRecordsJson['DomainRecords']['Record'][i]['Value']  
        Remote_Line = DescribeDomainRecordsJson['DomainRecords']['Record'][i]['Line']     
        RemoteDict_RRValue = {'Remote_RecordId':Remote_RecordId, 'Remote_RR':Remote_RR, 'Remote_Value':Remote_Value, 'Remote_Line':Remote_Line}
        RemoteList_RecordIdRRValue.append(RemoteDict_RRValue)
    logger.debug("Obtained cloud DNS list: "+str(RemoteList_RecordIdRRValue))
    return RemoteList_RecordIdRRValue

#UpdateAliyunDNSRecord
def UpdateAliyunDNSRecord():
    RemoteList_RecordIdRRValue = GetRemoteRecordsIpAddress()
    publicAddress = GetPublicIpAddress()

    for i in range(len(domainConfig['Record'])):
        local_RR = domainConfig['Record'][i]['RR']
        local_Type = domainConfig['Record'][i]['Type']
        local_RecordId = domainConfig['Record'][i]['RecordId']
        local_Line = domainConfig['Record'][i]['Line']

        #logger.debug("------UpdateAliyunDNSRecord------")
        #local_RecordId为空，则添加记录
        if local_RecordId == "":
            #print("第"+i+"个数据RecordId为空")
            logger.debug("The No."+ str(i) +" data RecordId is empty")
            try:            
                AddDomainRecord = AddDomainRecordHelper(client, domainName, local_RR, local_Type, publicAddress, local_Line)
                RecordId = json.loads(AddDomainRecord)['RecordId']
                #print("DNS记录添加成功："+RecordId+" | "+local_RR+"."+domainName+" | "+local_Type+" | "+publicAddress+" | "+local_Line)
                logger.info("DNS record added successfully: "+RecordId+" | "+local_RR+"."+domainName+" | "+local_Type+" | "+publicAddress+" | "+local_Line)
            except:
                #print("DNS记录添加失败：", sys.exc_info()[0])
                logger.error("DNS record addition failed")
            '''
            将修改过的新RecordId回写进userConfig中
            '''
            domainConfigDirt = ReadConfig(domainConfigPath, 'r')
            domainConfigDirt['Record'][i]['RecordId'] = json.loads(AddDomainRecord)['RecordId']
            with open(domainConfigPath, 'w+') as domainConfig_newJson:
                json.dump(domainConfigDirt, domainConfig_newJson ,indent=4)
            continue
        elif isRecordExistAndNotEqual(local_RecordId, RemoteList_RecordIdRRValue, publicAddress):
            try:
                UpdateDomainRecordHelper(client, local_RecordId, local_RR, local_Type, publicAddress, local_Line)
                #print("更新记录成功local_RecordId："+local_RecordId)
                logger.info("Update DNS record successfully")
            except:
                logger.error("Update DNS record failed,local_RecordId: "+local_RecordId, sys.exc_info()[0])
    #logger.debug("------UpdateAliyunDNSRecord------")
    logger.info("Dynamic DNS update address completed")

#根据本地记录的RecordId在云端查找是否已存在该记录且是否与本地当前地址不相等（此时需要修改）,False表示无需更改，True表示需要更新数据
def isRecordExistAndNotEqual(LocalRecordIdStr, RemoteList, LocalPublicAddress):
    for i in range(len(RemoteList)):
        if LocalRecordIdStr == RemoteList[i]['Remote_RecordId']:
            #print("LocalRecordId："+LocalRecordIdStr+"存在")
            logger.info("LocalRecordId: " + LocalRecordIdStr + " exists")
            if LocalPublicAddress == RemoteList[i]['Remote_Value']:
                #print("云端记录地址为"+publicAddress+"与本地相同，无需更改")
                logger.info("Cloud Record Address is: " + LocalPublicAddress + " is the same as the local one, no need to change")
                return False
            else:
                logger.info("Cloud Record Address is "+RemoteList[i]['Remote_Value']+" is different from the local public network address "+LocalPublicAddress+" and needs to be changed")
                return True
    logger.warning("LocalRecordId: "+LocalRecordIdStr+" does not exist")
    return False