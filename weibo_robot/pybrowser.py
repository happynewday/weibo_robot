# coding: utf8 
""" 提供模拟浏览器环境 
"""
from __future__ import absolute_import, unicode_literals
import signal
import psutil
import pyppeteer
import pyua
from pyobject import PyObject


class PyBrowser(PyObject):
    def __init__(self, proxy_server=None, executable_path=None, userDataDir=None, headLess=False):
        PyObject.__init__(self)
        self.proxy_server = proxy_server
        self.executable_path = executable_path
        self.userDataDir = userDataDir
        self.headLess = headLess
        self.browser = None
        self.pid = None


    async def __aenter__(self):
        await self.launch()
        return self.browser

    
    async def __aexit__(self, exc_type, exc, tb):
        self.log.info('close browser')
        await self.browser.close()
        self.force_close()


    async def launch(self):
        self.log.info('launch browser')
        args = [ 
                '--disable-web-security',
                '--disable-extensions',
                '--hide-scrollbars',
                '--disable-bundled-ppapi-flash',
                '--mute-audio',
                '--no-sandbox',
				'--enable-viewport',
                '--disable-setuid-sandbox',
                '--disable-gpu']
        if self.proxy_server:
            args.append('--proxy-server={}'.format(self.proxy_server))
        print(args)
        kwargs = {
            'headless': False, 
            'devtools': True,
            'args': args,
            'dumpio': True, 
            'ignoreHTTPSErrors': True, 
            'handleSIGHUP': False, 
            'autoClose': False
        }
        if self.executable_path:
            kwargs['executablePath'] = self.executable_path
        if self.userDataDir:
            kwargs['userDataDir'] = self.userDataDir
        if self.headLess:
            kwargs['headless'] = True
        self.browser = await pyppeteer.launch(kwargs)
        self.pid = self.browser.process.pid
        self.log.info('browser launched [{}][{}]'.format(
                self.browser.process.pid, self.browser.wsEndpoint))



    def force_close(self):
        try:
            parent = psutil.Process(self.pid)
            # todo: check if is a chrome process
        except psutil.NoSuchProcess:
            return
        self.log.info('force close browser')
        sig = signal.SIGTERM
        children = parent.children(recursive=True)
        for c in children:
            c.send_signal(sig)
        parent.send_signal(sig)

