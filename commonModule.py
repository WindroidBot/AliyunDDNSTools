from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
import json

#从指定的配置文件读取用户配置
def ReadUserConfig(configPath):
    with open(configPath,'r') as jsonFile:
        config = json.load(jsonFile)
    return config

#执行request并返回结果
def ExecuteGetResults(client,request):
    response = client.do_action_with_exception(request)
    responseStr = str(response, encoding = "utf8")
    responseJson = json.loads(responseStr)
    responseDict=json.dumps(responseJson,indent=4)
    return responseDict

#从指定的配置文件构造client对象
def GetAliyunClient(configPath):
    UserConfig = ReadUserConfig(configPath)
    accessKeyId = UserConfig['accessKeyId']
    accessSecret = UserConfig['accessSecret']
    domainName = UserConfig['domainName']
    client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')
    return client