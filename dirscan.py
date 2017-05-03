#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import threading
from Queue import Queue
import sys
from optparse import OptionParser
import time


headers = { # HTTP 头设置
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
	'Referer' : 'http://www.google.com',
	'Cookie': 'whoami=wyscan_dirfuzz',
}


class DirScanMain:
	def __init__(self,options):
		self.target = options.url
		self.ext = options.ext
		self.thread_count = options.thread
		self.outfile = options.outfile
		

	class DirScan(threading.Thread):
		def __init__(self, queue, total, outfile):
			threading.Thread.__init__(self)
			self._queue = queue
			self.total = total
			self.outfile = outfile

		def run(self):
			self.start_time = time.time()
			while not self._queue.empty():
				url = self._queue.get()
				threading.Thread(target=self._print_msg).start()
				try:
					r = requests.get(url=url, timeout=6, headers=headers)

					if r.status_code < 400:
						sys.stdout.write('\r'+'[*]%s:%s'%(r.status_code,url)+'\n')
						f = open(self.outfile+'.html','a+')			
						f.write('<a href="'+url+'" target="_blank">'+url+'</a>')
						f.write('\r\n</br>')
						f.close()
				except Exception,e:
					print e
					pass

		def _print_msg(self):
			per = 100-float(self._queue.qsize())/float(self.total)*100
			# print '[*]Complete: %.1f %s'%(100-per,'%')
			msg = '%s Left| %1.f%s|Scan in %1.f seconds' %(self._queue.qsize(), per, '%', time.time()-self.start_time)
			# sys.stdout.write('\n')
			sys.stdout.write('\r'+'[*]'+msg+'\r')



	def start(self):
		f = open(self.outfile+'.html','w')
		f.close()
		queue = Queue()
		f = open('./dics/%s.txt'%self.ext, 'r')
		for i in f:
			queue.put(self.target+i.rstrip('\n'))

		total = queue.qsize()


		threads = []

		thread_count = self.thread_count

		for i in range(thread_count):
			threads.append(self.DirScan(queue, total, self.outfile))

		for t in threads:
			t.start()
		for t in threads:
			t.join()

if __name__ == '__main__':
	print'''
	 ___ ___ ___  ___  ___   _   _  _ 
	|   \_ _| _ \/ __|/ __| /_\ | \| |
	| |) | ||   /\__ \ (__ / _ \| .` |
	|___/___|_|_\|___/\___/_/ \_\_|\_|               

'''

	parser = OptionParser()
	parser.add_option("-u", "--url", dest="url", help="Target url")
	parser.add_option("-f", "--file_ext", dest="ext", help="Web code")
	parser.add_option("-t", "--thread", dest="thread", type="int", default=10, help="Thread for scan")
	parser.add_option("-o", "--outfile", dest="outfile", default='result', help="Result for scan")
	(options, args) = parser.parse_args()
	# print args
	# if len(args) != 1:
	if options.ext and options.url:
		d = DirScanMain(options)
		d.start()
		sys.exit(0)
	else:
		parser.print_help()
		sys.exit(0)