

import flask

import pathlib
from os.path import dirname, join, normpath
THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()

import revenue.basin.treasury as treasury

def OPEN (
	paths = []
):
	from flask import Flask

	app = Flask (__name__)

	treasury_string = treasury.start (
		links = paths
	)

	@app.route ("/")
	def treasury_route ():
		return treasury_string
	
	#@app.route('/', defaults={'path': ''})
	@app.route ("/<path:path>")
	def page (path):
		print (path)
		
		for found_path in paths:
			if (found_path ['path'] == path):
				return "".join (open (found_path ['find'], "r").readlines())
				
	
		return 'not found'
	
	
	'''
	fns = {}
	def create_route (route):
		@app.route (route)
		def fn ():
			return "route 1"
	
		
	for path in paths:	
		route = "/" + path ["path"]
		create_route (route)
	'''
	
	#
	#	https://stackoverflow.com/questions/2470971/fast-way-to-test-if-a-port-is-in-use-using-python
	#
	def is_port_in_use (port: int) -> bool:
		import socket
		with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as s:
			return s.connect_ex (('localhost', port)) == 0
	
		
	def run (limit, loop):
		print (f"run attempt { loop } of { limit }")
	
		try:
			port = 9988 + loop
			unavailable = is_port_in_use (port)
			#print ("unavailable:", unavailable)
			
			if (unavailable):
				raise Exception ("unavailable")
		
			app.run (
				port = port
			)
		
			print ('revenue app started')
			return			
		except Exception as E:
			pass;
			
		loop += 1;	
		
		run (
			limit,
			loop = loop
		)
			
		
			
	run (
		limit = 100,
		loop = 1
	)