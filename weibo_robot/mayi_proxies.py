#coding: utf8 
import time
import hashlib
                 

class MayiProxies(object):
    def __init__(self):
        self.app_key = '250388484'
        self.secret = '70f911adedf027abb6e07f35cec5fcc6'
        self.proxies = {'http': 's2.proxy.mayidaili.com:8123', 
                'https': 's2.proxy.mayidaili.com:8123'}
    
        params = {'app_key': self.app_key, 
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")}
        ks = [k for k in params.keys()]
        ks.sort()
        content = '{}{}{}'.format(self.secret, 
                ''.join(['{}{}'.format(k, params[k]) for k in ks]), 
                self.secret)
        sign = hashlib.md5(content.encode('utf8')).hexdigest().upper()
        params['sign'] = sign
        auth = 'MYH-AUTH-MD5 ' + '&'.join('{}={}'.format(k, v) 
                for k,v in params.items())
        self.headers = {'Proxy-Authorization': auth}

mayi = MayiProxies()

