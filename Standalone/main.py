import urllib.request
import urllib.parse
from urllib.error import HTTPError
from MainParser import MainParser
import html

def listreports(url, username, password):
	
	request = urllib.request.Request(url)
	# adding charset parameter to the Content-Type header.
	request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
	try:
		with urllib.request.urlopen(request) as f:
			csrf = f.getheader("Set-Cookie").split(";")
			request.add_header("Cookie",f.getheader("Set-Cookie"))
			item = csrf[0].split("=")[1]
			data = urllib.parse.urlencode({'next': "/", 'username': username, 'password': password, 'csrfmiddlewaretoken': item})
			data = data.encode('utf-8')
			try:
				with urllib.request.urlopen(request,data) as f2:
					string = f2.read().decode('utf-8')
					html.unescape(string)
					#print(string)
					parser = MainParser()
					parser.feed(string)
					parser.close()
			except HTTPError as e:
				print(e.read())
	except HTTPError as e:
		print(e.read())

if __name__=="__main__":
	listreports("http://127.0.0.1:8000/accounts/login/","fdsa","fdsa")