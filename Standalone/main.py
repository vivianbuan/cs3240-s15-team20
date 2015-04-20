import urllib.request
import urllib.parse
from urllib.error import HTTPError
from MainParser import MainParser, AuthParser
import html
import getpass

_DEBUG = True

def getpage(url,username,password):
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
					return string
			except HTTPError as e:
				if _DEBUG:
					print(e.read())
	except HTTPError as e:
		if _DEBUG:
			print(e.read())

def listreports(url, username, password):
	string = getpage(url,username,password)
	parser = MainParser()
	parser.feed(string)
	parser.close()


def auth(url,username, password):
	string = getpage(url,username,password)
	parser = AuthParser()
	parser.feed(string)
	parser.close()
	return parser.authenticated

if __name__=="__main__":
	while True:
		url = input("Site URL: ")
		username = input("Username: ")
		pswd = getpass.getpass('Password:')
		if auth(url + "/accounts/login/",username,pswd):
			loggedIn = True
			break
		while True:
			response = input("Incorrect Login Info. Continue (y or n)? ")
			if response == 'y':
				giveUp = False
				break
			elif response == 'n':
				loggedIn = False
				giveUp = True
				break
			else:
				print("Unrecognized Response.")
		if giveUp:
			break

	while loggedIn:
		command = input("#Enter Command: ")
		if command == "help":
			print("There are currently 2 commands implemented:")
			print("\tlist: list all reports accessible to you")
			print("\tquit: exit this program")
		elif command == "list":
			listreports(url+"/accounts/login/",username,pswd)
		elif command == "quit":
			break
		else:
			print("Command not recognized. Type help for list of commands")