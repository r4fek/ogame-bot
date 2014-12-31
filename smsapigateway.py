# -*- coding: utf-8 -*-
import urllib2
from urlparse import urlparse
from urllib import quote

class SMSAPIGateway(object):
	PASS_MD5 = '85d9ee56e9927912119fbc89de2eb22e'
	USERNAME = 'username'
	URL = 'https://ssl.smsapi.pl/sms.do?'
	TO = 'PHONE_NUMBER'

	def send(self, msg):
		url = '%susername=%s&password=%s&message=%s&to=%s&eco=1&encoding=utf-8' % \
			(self.URL, self.USERNAME, self.PASS_MD5, msg, self.TO)
		url = quote(url, safe='/:?&=')
		try:
			print urllib2.urlopen(url).read()
		except Exception, e:
			print e

if __name__ == "__main__":
	SMSAPIGateway().send('tesfg zażółć gęślą jażźń')
