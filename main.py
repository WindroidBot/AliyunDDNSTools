from commonModule import *
from domainInfoHelperModule import *
import time
from apscheduler.schedulers.blocking import BlockingScheduler
'''
def dojob():
    scheduler = BlockingScheduler()
    scheduler.add_job(UpdateAliyunDNSRecord, 'interval', seconds=10, id='job1')
    scheduler.start()
dojob()
'''
UpdateAliyunDNSRecord()