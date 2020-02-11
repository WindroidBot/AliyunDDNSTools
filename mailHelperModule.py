import smtplib
import sys
from email.mime.text import MIMEText
from email.header import Header
import logging
from logging.config import fileConfig
from commonModule import ReadConfig

logging.config.fileConfig('log.conf')
logger = logging.getLogger('mailHelperModule')

def sendMessage(userConfigPath,newIPAddress,oldIPAddress):
    UserConfig = ReadConfig(userConfigPath, 'r')
    if UserConfig['remind']['enable'] != "ture":
        return
    smtp_host = UserConfig['remind']['smtp_host']
    smtp_user = UserConfig['remind']['smtp_user']
    smtp_pass = UserConfig['remind']['smtp_pass']
    sender = UserConfig['remind']['sender']
    receivers = UserConfig['remind']['receivers']

    subject = 'AliyunDDNTS Message'
    messageStr = "Your public address has changed. The new address is: " + newIPAddress + ",and the old address is: " + oldIPAddress + ".This message was sent automatically by an unattended mailbox, please do not reply."
 
    message = MIMEText(messageStr, 'plain', 'utf-8')
    message['From'] = Header("Alert", 'utf-8')
    #message['To'] =  Header("AliyunDDNTS Users", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(smtp_host, 25)
        smtpObj.login(smtp_user,smtp_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        logger.info("Mail sent successfully")
    except smtplib.SMTPException:
        logger.error("Failed to send mail", sys.exc_info()[0])