import urllib.request
import urllib.parse
from urllib.error import HTTPError
from http import cookiejar
from MainParser import MainParser, AuthParser
from DetailParser import DetailParser
import html
import getpass

_DEBUG = True
cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def getpage(url,username,password, page):
	urllib.request.install_opener(opener)

	request = urllib.request.Request(url+'/accounts/login/')
	request2 = urllib.request.Request(url+page)
	# adding charset parameter to the Content-Type header.
	request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
	try:
		with opener.open(request) as f:
			"""for cookie in cj:
				print(cookie)"""
			csrf = f.getheader("Set-Cookie").split(";")
			request.add_header("Cookie",f.getheader("Set-Cookie"))
			item = csrf[0].split("=")[1]
			data = urllib.parse.urlencode({'next': page, 
										   'username': username,
										   'password': password,
										   'csrfmiddlewaretoken': item,
										   'login':'login'})
			data = data.encode('utf-8')
			try:
				with opener.open(request,data) as f2:
					"""for cookie in cj:
						print(cookie)"""
					pass
				with opener.open(request2) as f2:
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
	string = getpage(url,username,password,'/')
	parser = MainParser()
	parser.feed(string)
	parser.close()


def auth(url,username, password):
	string = getpage(url,username,password,'/')
	parser = AuthParser()
	# print(string)
	parser.feed(string)
	parser.close()
	return parser.authenticated

def detail(url, username, password, num):
	string = getpage(url,username,password,'/reports/detail/'+num+'/')
	parser = DetailParser()
	# print(string)
	parser.feed(string)
	while(True):
		fileno = int(input("~Download File(-1 to go back to main menu): "))
		if fileno == -1:
			break
		if fileno >= len(parser.docs):
			print("Incorrect input: That doc does not exist")
			continue
		filedownload(url, parser.docs[fileno],parser.encrypted)
	parser.close()

def filedownload(url,doc, enc):
	address=url+doc
	file_name = address.split('/')[-1]
	with opener.open(address) as u:
		with open(file_name, 'wb') as f:
			if not enc:
				f.write(u.read())
			else:
				print("time to decrypt")

if __name__=="__main__":
	while True:
		url = input("Site URL: ")
		username = input("Username: ")
		pswd = getpass.getpass('Password:')
		if auth(url,username,pswd):
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
		command = input("~Enter Command: ")
		command = command.split(' ')
		if command[0] == "help":
			print("There are currently 3 commands implemented:")
			print("\tlist: list all reports accessible to you")
			print("\tdetail [x]: list details for report x from list")
			print("\tquit: exit this program")
		elif command[0] == "list":
			listreports(url,username,pswd)
		elif command[0] == "detail":
			detail(url,username,pswd,command[1])
		elif command[0] == "quit":
			break
		else:
			print("Command not recognized. Type help for list of commands")