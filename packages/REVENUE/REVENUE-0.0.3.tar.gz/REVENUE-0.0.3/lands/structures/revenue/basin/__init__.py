

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
		
		
	app.run (
		port = 9989
	)