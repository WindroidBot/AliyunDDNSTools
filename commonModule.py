from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException

from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

import json
import os
import sys
import urllib.request
import logging
from logging.config import fileConfig

logging.config.fileConfig('log.conf')
logger = logging.getLogger('Common')

#从指定的配置文件读取配置，rwopt为读写选项
def ReadConfig(configPath, rwopt):
    try:
        with open(configPath, rwopt, encoding='utf-8') as jsonFile:
            config = json.load(jsonFile)
        jsonFile.close()
    except:
        logger.error("Loading JSON file failed: "+configPath)
    logger.info("Load JSON file successfully: "+configPath)
    return config

'''
从已生成的client执行request并返回结果，注意：返回的结果是str类型，需要使用json.loads(...)转为json，才可以访问
或者不使用responseDict=json.dumps(responseJson,indent=4)，直接返回responseJson
'''
def ExecuteGetResults(client,request):
    response = client.do_action_with_exception(request)
    try:
        responseStr = str(response, encoding = "utf8")
    except:
        logger.error("Execution failed")
    responseJson = json.loads(responseStr)
    responseDict=json.dumps(responseJson,indent=4)
    logger.debug("Return message: "+responseStr)
    return responseDict

#从指定的配置文件构造client对象
def GetAliyunClient(configPath):
    UserConfig = ReadConfig(configPath, 'r')
    accessKeyId = UserConfig['accessKeyId']
    accessSecret = UserConfig['accessSecret']
    domainName = UserConfig['domainName']
    try:
        client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
        logger.info("Client created successfully")
    except:
        logger.error("Client creation failed")
        quit()
    return client

#获取当前公网地址
def GetPublicIpAddress():
    requestIpUrl="http://ip.42.pl/raw"
    try:
        response=urllib.request.urlopen(requestIpUrl).read()   
        responseIpAddress = str(response, encoding = "utf8")
    except:
        logger.error("Failed to obtain public network address, retrying...")
        return GetPublicIpAddress()
    logger.info("Successfully obtained public network address: "+responseIpAddress)
    return responseIpAddress

#获取指定域名的所有子域名信息
#https://help.aliyun.com/document_detail/29776.html?spm=a2c4g.11186623.6.650.94a13b59Q6kBCd
def DescribeDomainRecordsRequestHelper(Client, DomainName):
    Request = DescribeDomainRecordsRequest()
    Request.set_accept_format('json')

    Request.set_DomainName(DomainName)

    result = ExecuteGetResults(Client,Request)
    #print(result)
    return result

#增加主机记录
#https://help.aliyun.com/document_detail/29772.html?spm=a2c4g.11186623.6.653.46333b595r89tS
def AddDomainRecordHelper(Client, DomainName, RR, Type, Value, Line):
    Request = AddDomainRecordRequest()
    Request.set_accept_format('json')

    #设置增加记录的信息
    Request.set_DomainName(DomainName)
    Request.set_RR(RR)
    Request.set_Type(Type)
    Request.set_Value(Value)
    Request.set_Line(Line)

    result = ExecuteGetResults(Client,Request)
    #print(result)
    return result

#根据RecordID删除记录
#https://help.aliyun.com/document_detail/29773.html?spm=a2c4g.11186623.6.654.4f611cebnCahyS
def DeleteDomainRecordHelper(Client, RecordId):
    Request = DeleteDomainRecordRequest()
    Request.set_accept_format(RecordId)

    #设置待删除记录的RecordId
    Request.set_RecordId(RecordId)

    result = ExecuteGetResults(Client,Request)
    print(result)
    return result

#根据主机记录删除记录
#https://help.aliyun.com/document_detail/29779.html?spm=a2c4g.11186623.6.656.570d2846hOPSu6
def DeleteSubDomainRecordsHelper(Client, DomainName, RR):
    Request = DeleteSubDomainRecordsRequest()
    Request.set_accept_format('json')

    #设置待删除记录的信息
    Request.set_DomainName(DomainName)
    Request.set_RR(RR)

    result = ExecuteGetResults(Client,Request)
    print(result)
    return result

#根据RecordId修改对应的记录的信息
#https://help.aliyun.com/document_detail/29774.html?spm=a2c4g.11186623.6.655.43fd3192UJmbmD
def UpdateDomainRecordHelper(Client, RecordId, RR, Type, Value, Line):
    Request = UpdateDomainRecordRequest()
    Request.set_accept_format('json')

    #设置新的记录的信息
    Request.set_RecordId(RecordId)
    Request.set_RR(RR)
    Request.set_Type(Type)
    Request.set_Value(Value)
    Request.set_Line(Line)

    result = ExecuteGetResults(Client,Request)
    #print(result)
    return result