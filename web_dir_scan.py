#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Queue import Queue
import gevent
from gevent import monkey; monkey.patch_all()
import requests
import sys

headers = { # HTTP 头设置
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
	'Referer' : 'http://www.google.com',
	'Cookie': 'whoami=wyscan_dirfuzz',
}

def scan(queue):
	while not queue.empty():
		url = queue.get()
		try:
			r = requests.get(url=url, headers=headers, timeout=3)
			if r.status_code != 404:
				print '[*]%s:%s'%(r.status_code,url)
		except Exception,e:
			pass

def creat(host, file_ext):
	queue = Queue()
	f = open('./dics/%s.txt'%file_ext, 'r')
	for i in f:
		queue.put(host+i.rstrip('\n'))

	return queue

def run(host, file_ext):
	queue = creat(host, file_ext)

	gevent_pool = []
	thread_count = 50

	for i in range(thread_count):
		gevent_pool.append(gevent.spawn(scan,queue))
	gevent.joinall(gevent_pool)

# run('http://www.rqzhzh.net/', 'php')
if __name__ == '__main__':
	if len(sys.argv) == 3:
		run(sys.argv[1], sys.argv[2])
		sys.exit(0)
	else:
		print 'Usage: %s http://www.baidu.com/ php'%(sys.argv[0])
		sys.exit(-1)
