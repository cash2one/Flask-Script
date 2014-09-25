# coding=utf-8
from random import randint
import string
import urllib
from flask import current_app
from flask.ext.mail import Mail, Message
import urllib2

__author__ = 'GaoJie'


def send_email(title, content, to_list, cc_list=None, bcc_list=None, sender=None):
    """
    发送邮件
    """
    mail = Mail(current_app)
    extra = {
        "Accept-Charset": "ISO-8859-1,utf-8"
    }
    msg = Message(subject=title, html=content, recipients=to_list, sender=sender, cc=cc_list, bcc=bcc_list, extra_headers=extra)
    return mail.send(msg)


def get_url_content(url, data={}, header={}):
    """
    get方式获取页面信息
    """
    if url.find('?') >= 0:
        url += '&'
    else:
        url += '?'
    if data:
        url += urllib.urlencode(data)
    try:
        current_app.logger.debug('[ URL REQUEST ] %s', url)
        if header:
            current_app.logger.debug('[ URL HEADER ] %s', header)
        request = urllib2.Request(url, headers=header)
        content = urllib2.urlopen(request).read()
        current_app.logger.debug('[ URL RESPONSE ] %s', content)
    except Exception as e:
        current_app.logger.error('[ URL EXCEPTION ] %s', e)
        raise
    return content


def post_url_content(url, data, header={}):
    """
    post方式获取页面信息
    """
    try:
        current_app.logger.debug('[ URL REQUEST ] %s', url)
        if header:
            current_app.logger.debug('[ URL HEADER ] %s', header)
        if data:
            current_app.logger.debug('[ URL DATA ] %s', data)
            if isinstance(data, dict):
                data = urllib.urlencode(data)
        request = urllib2.Request(url, data=data, headers=header)
        content = urllib2.urlopen(request).read()
        current_app.logger.debug('[ URL RESPONSE ] %s', content)
    except Exception as e:
        current_app.logger.error('[ URL EXCEPTION ] %s', e)
        raise
    return content


def random_str(str_len=8):
    """
    生成固定长度随机字符串
    :param str_len:
    :return:
    """
    s = ''
    chars = list(string.ascii_letters + string.digits)
    length = len(chars) - 1
    for i in xrange(str_len):
        s += chars[randint(0, length)]
    return s