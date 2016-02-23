#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Julius web server (with CherryPy:http://www.cherrypy.org/)
# written by Ryota NISHIMURA 2015/Dec./16

### configure ###########
JULIUS_HOME		= "/home/delihiros/Documents/work/dictation-kit/bin/linux"
JULIUS_EXEC		= "/home/delihiros/Documents/work/dictation-kit/bin/linux/julius -C /home/delihiros/Documents/work/dictation-kit/am-gmm.jconf -C /home/delihiros/Documents/work/dictation-kit/main.jconf -input file -outfile"
SERVER_PORT 	= 8000
ASR_FILEPATH	= '/home/delihiros/Documents/work/trapepper/resources/'
ASR_IN			= 'asr.wav'
ASR_RESULT		= 'asr.out'
OUT_CHKNUM		= 5 # for avoid that the output file is empty

### import ##############
import cherrypy
import subprocess
import sys
import os
import time
import socket
from cherrypy import request

### class define ########
class ASRServer(object):
	# Julius execution -> subprocess
	p = subprocess.Popen (JULIUS_EXEC, shell=True, cwd=JULIUS_HOME, 
		stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		close_fds=True)
	(stdouterr, stdin) = (p.stdout, p.stdin)

	# main task
	def index(self):
		return """
			<html><body>
				<h2>Julius Server</h2>
				USAGE:<br />
				- 16000Hz, wav(or raw)-file, big-endian, mono<br />
				<br />
				<form action="asr_julius" method="post" enctype="multipart/form-data">
				filename: <input type="file" name="myFile" /><br />
				<input type="submit" />
				</form>
			</body></html>
			"""
	index.exposed = True
		
	def asr_julius(self, myFile):	        
		# receive WAV file from client & write WAV file
		with open(ASR_FILEPATH + ASR_IN, 'wb') as f:
			f.write(myFile.file.read())
		f.close()
		
		# ASR using Julius
		if os.path.exists(ASR_FILEPATH + ASR_RESULT):
			os.remove(ASR_FILEPATH + ASR_RESULT)			# delete a previous result file

		self.p.stdin.write(bytes(ASR_FILEPATH + ASR_IN + '\n', 'utf-8'))	# send wav file name to Julius
		# print(self.p.stdout.read())
		self.p.stdin.flush()

		# wait for result file creation & result writing (avoid the file empty)
		while not (os.path.exists(ASR_FILEPATH + ASR_RESULT) and len(open(ASR_FILEPATH + ASR_RESULT).readlines()) == OUT_CHKNUM):
			time.sleep(0.1)
			
		# read result file & send it to client
		outlines = open(ASR_FILEPATH + ASR_RESULT).read()
		outlines = "<xmp>" + outlines + "</xmp>"
		return outlines
	asr_julius.exposed = True

### main ################
# get own IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]

# start the CherryPy server
cherrypy.config.update({'server.socket_port': SERVER_PORT,})
cherrypy.config.update({'server.socket_host': server_ip,})
cherrypy.quickstart(ASRServer())
