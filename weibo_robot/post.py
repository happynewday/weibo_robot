# coding: utf8
import os
import sys
import json
import asyncio
import requests
import pyua
from pyobject import PyObject
from .pybrowser import PyBrowser

log = PyObject().log
		

async def post(url, cookies, msg):
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
		
		log.info('set cookies')
		cookies = json.loads(cookies)
		await page.setCookie(*cookies)
			
		log.info('open page.. ')
		await page.goto(url, timeout=120000)
		
		log.info('wait for contents')
		selector1 = '#Pl_Official_MyProfileFeed__20 > div > div:nth-child(2) > div.WB_feed_handle > div > ul > li:nth-child(3) > a > span > span > span'
		await page.waitForSelector(selector1, options={'timeout': 60000, 'visible': True})
		await asyncio.sleep(1)
		
		for i in range(10):
			log.info('click on comment')
			await page.click(selector1, {'delay': 100})
			await asyncio.sleep(2)
			
			log.info('wait for comment area')
			selector2 = '#Pl_Official_MyProfileFeed__20 > div > div:nth-child(2) > div.WB_feed_repeat.S_bg1 > div > div > div.WB_feed_publish.clearfix > div.WB_publish > div.p_input > textarea'
			try:
				await page.waitForSelector(selector2, options={'timeout': 10000, 'visible': True})
			except Exception as e:
				continue
			
			log.info('typing msg')
			await page.focus(selector2)
			await page.keyboard.type(msg, options={'delay': 100})
			
			log.info('click send')
			await asyncio.sleep(2)
			selector3 = '#Pl_Official_MyProfileFeed__20 > div > div:nth-child(2) > div.WB_feed_repeat.S_bg1 > div > div > div.WB_feed_publish.clearfix > div.WB_publish > div.p_opt.clearfix > div.btn.W_fr > a'
			try:
				await page.waitForSelector(selector3, options={'timeout': 5000, 'visible': True})
			except Exception as e:
				continue
			await page.focus(selector3)
			await page.click(selector3, {'delay': 100})
			break
		
		while input('input:') != 'e':
			await asyncio.sleep(5)	
		


