# coding: utf8
import os
import sys
import json
import asyncio
import requests
import pyua
from pyobject import PyObject
from yundama import YunDaMa
from pybrowser import PyBrowser

log = PyObject().log

ydm = YunDaMa(username='asafish83', password='Tryqtyl2', 
		appid=1, appkey='22cc5376925e9387a23cf797cb9ba745')
		

async def screenshotElement(page, selector, path):
	js = """
		selector =>{
		const element = document.querySelector(selector);
		if (!element)
			return null;
		const {x, y, width, height} = element.getBoundingClientRect();
		return {left: x, top: y, width, height, id: element.id};
		}
	"""
	rect = await page.evaluate(js, selector)
	if not rect:
		return False
	await page.screenshot({'path': path, 'clip': {
			'x': rect['left'], 'y': rect['top'],
			'width': rect['width'], 'height': rect['height']}})


async def login_weibo(user, pswd):
	url = 'https://weibo.com/'
	async with PyBrowser(proxy_server='socks5://localhost:1080') as b:
		page = await b.newPage()
		await page.setViewport(viewport={'width':1280, 'height':800})
		await page.evaluate("""
			() =>{
				Object.defineProperties(navigator,{
					webdriver:{
					get: () => false
					}
				})
			}
		""")
		await page.setJavaScriptEnabled(enabled=True)
		await page.setUserAgent(pyua.CHROME)
		log.info('open page.. ')
		await page.goto(url, timeout=120000)
		
		log.info('wait for user element')
		selector = '#loginname'
		await page.waitForSelector(selector, options={'timeout': 5000, 'visible': True})
		log.info('typing user name')
		await page.click(selector)
		await page.keyboard.type(user, options={'delay': 100})
		
		log.info('wait for pswd element')
		selector2 = '#pl_login_form > div > div:nth-child(3) > div.info_list.password > div > input'
		await page.waitForSelector(selector2, options={'timeout': 5000, 'visible': True})
		await page.click(selector2)
		log.info('typing pswd')
		await page.keyboard.type(pswd, options={'delay': 100})

		log.info('wait for verify code element')
		selector3 = '#pl_login_form > div > div:nth-child(3) > div.info_list.verify.clearfix > a > img'
		await page.waitForSelector(selector3, options={'timeout': 5000, 'visible': True})
		await asyncio.sleep(2)
		log.info('screenshot code')
		await screenshotElement(page, selector3, 'code.jpg')
		log.info('decode code')
		cid, code = ydm.decode('code.jpg', 1005, 10)
		if not code:
			log.error('ydm decode failed {}'.format(cid))
			return
		
		log.info('typing code')
		selector4 = '#pl_login_form > div > div:nth-child(3) > div.info_list.verify.clearfix > div > input'
		await page.click(selector4)
		await page.keyboard.type(code, options={'delay': 100})
		
		log.info('login..')
		selector5 = '#pl_login_form > div > div:nth-child(3) > div:nth-child(6) > a > span'
		await page.waitForSelector(selector5, options={'timeout': 5000, 'visible': True})
		await page.click(selector5)
		
		while input('input:') != 'e':
			await asyncio.sleep(5)
			
		cookies = await page.cookies()
		log.info('save cookies: {}'.format(cookies))
		open('cookies', 'w').write(json.dumps(cookies, ensure_ascii=False))	
		
asyncio.run(login_weibo('18520191011', '1A.justaguest'))

