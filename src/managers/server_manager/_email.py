from datetime import datetime
from email.mime.text import MIMEText

from aiosmtplib import SMTP, SMTPException
from src.utils.config import config
from src.utils.log import logger


class MailClient(object):
    '''发送邮件class'''
    _host: str
    '''服务器地址'''
    _pord: int
    '''服务器端口'''
    _user: str
    '''用户名'''
    _pass: str
    '''授权码'''
    _sender: str
    '''发送者'''
    _receiver: str
    '''接受方'''

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(MailClient, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        '''初始化'''
        self._host = config.mail['host']
        self._pord = config.mail['pord']
        self._user = config.mail['user']
        self._pass = config.mail['pass']
        self._sender = config.mail['sender']
        self._receiver = config.mail['receiver']

    async def send_mail(self, robot_id: int) -> None:
        '''
        :说明
            发送邮件给配置内用户
        :参数
            * robot_id：机器人QQ
        '''
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = f"你的机器人：[{str(robot_id)}] 在 {time_now} 掉线了！"
        message = MIMEText(text)
        message['From'] = self._sender
        message['To'] = self._receiver
        message["Subject"] = f"机器人[{str(robot_id)}]掉线了"
        try:
            async with SMTP(hostname=self._host, port=self._pord, use_tls=True) as smtp:
                await smtp.login(self._user, self._pass)
                await smtp.send_message(message)
        except SMTPException as e:
            log = f"发送邮件失败，原因：{str(e)}"
            logger.opt(colors=True).error(log)
        except Exception as e:
            logger.opt(colors=True).error(f"<r>发送邮件失败，可能是你的配置有问题：{str(e)}</r>")


mail_client = MailClient()
'''发送邮件客户端'''
