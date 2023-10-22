

from mako.template import Template

def start (
	links
):
	'''
	links = [
		{
			"path": "company/company.r.html",
			"name": "company/company"
		}
	]
	'''
	
	if (len (links) >= 1):
		open = links [0]['path']
	else:
		open = ""
	
	links_string = ""
	for link in links:
		path = link ['path']
		name = link ['name']
	
		links_string += (
			f'<a href="{ path }">{ name }</a>'
		)
		
		

	temp = Template ('''
<!doctype html>
<html lang="en">
<head>
	<meta charset="UTF-8" />
	<style>
	code {
		display: block;
		background: #EEE;
		padding: 10px;
		border-radius: 4px;
	}
	
	a {
		display: block;
	}
	

	</style>
</head>
<body style="padding: .5in; font-size: 1.3em; opacity: 0; transition: opacity .5s">
	<div
		style="
			display: flex;
		"
	>
		<div style="width: 250px">
			<h1>{ revenue }</h1>
			${ links_string }
		</div>
		<div style="width: calc(100% - 200px)">
			<iframe 
				id="statement"
				style="
					width: 100%;
					height: 800px;
					border: 0;
					opacity: 0;
					transition: opacity .1s;
				"
				src="${ open }" 
			></iframe>
		</div>
	</div>

	<script>
		console.log ("lyrics");

		document.addEventListener ("DOMContentLoaded", function(event) { 
			document.body.style.opacity = 1;
			
			setTimeout (() => {		
				document.body.style.opacity = 1;
			}, 500)
		});	

		const $__statement = document.getElementById ("statement")

		document.querySelectorAll ('a').forEach ($__link => {
			console.log ("for each", $__link)
			
			
			$__link.addEventListener ("click", function ($__event) {
				$__event.preventDefault ()
				$__statement.style.opacity = 0;
	
				console.log (this.href)

				setTimeout (() => {	
					$__statement.src = this.href
				}, 120);
				
				setTimeout (() => {	
					$__statement.style.opacity = 1;
				}, 140)
			})
		})
		
		
		document.addEventListener ("DOMContentLoaded", function(event) { 
			$__statement.style.opacity = 1;
			setTimeout (() => {		
				$__statement.style.opacity = 1;
			}, 500)
		});	
	</script>
</body>
</html>
''')

	return temp.render (
		links_string = links_string,
		open = open
	)