


import glob
import os
import inspect
import json

import revenue.basin as BASIN

import json

def start (params = {}):
	if ("directory" in params):
		directory = params ["directory"]
	else:
		directory = os.path.dirname (
			os.path.abspath ((inspect.stack ()[1]) [1])
		)
		
	if ("extension" in params):
		extension = params ["extension"]
	else:
		extension = ".r.html"
		
	if ("relative path" in params):
		relative_path = params ["relative path"]
	else:
		relative_path = directory


	glob_param = directory + "/**/*" + extension;

	finds = glob.glob (glob_param, recursive = True)
	print (finds)
	
	paths = []
	for find in finds:
		path = os.path.relpath (find, relative_path)
		name = path.split (extension)[0]
	
		paths.append ({
			"path": path,
			"name": name,
			"find": find
		})
		
	print ("paths:", json.dumps (paths, indent = 4))
	
	BASIN.OPEN (
		paths = paths
	)

	return;