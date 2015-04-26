from html.parser import HTMLParser

class DetailParser(HTMLParser):
	reading="None"
	encrypted=False
	doc=""
	docs=[]
	hashes=[]

	def handle_starttag(self, tag, attrs):
		# print("Start: " + tag)
		for name,value in attrs:
			if name == "id":
				if value == "short":
					self.reading="print"
					print("Short Description: ", end="")
				if value == "long":
					self.reading="print"
					print("Long Description: ", end="")
				if value == "loc":
					self.reading="print"
					print("Location: ", end="")
				if value == "date":
					self.reading="print"
					print("Date: ", end="")
				if value == "keys":
					self.reading="print"
					print("Keywords: ", end="")
				if "group" in value:
					self.reading="print"
					print("Shared with: ", end="")
				if value == "private":
					self.reading="print"
					print("Is Private: ", end="")
				if value == "enc" and tag == "ul":
					self.encrypted=True
					print("Documents are encrypted")
				if "doc" in value:
					self.reading="print"
					string = "Document " + value.split('doc')[1] + ": "
					print(string, end="")
					self.docs.append(self.doc)
				if "hash" in value:
					self.reading="hash"
			if name == "href" and tag == "a":
				self.doc=value

	def handle_endtag(self, tag):
		if tag == "span":
			if self.reading != "None":
				print()
			self.reading="None"

	def handle_data(self, data):
		if self.reading is "None":
			pass
		elif self.reading is "print":
			print(data, end="")
		elif self.reading is "hash":
			self.hashes.append(data)
		else:
			print("Error, Unhandled action")

	def handle_charref(self, name):
		if name.startswith('x'):
			c = chr(int(name[1:], 16))
		else:
			c = chr(int(name))
		if self.reading is 'print':
			print(c, end="")

	def clear(self):
		self.reading="None"
		self.encrypted=False
		self.doc=""
		self.docs=[]
		self.hashes=[]
		print("Clear: " + str(self.docs) + " " + str(self.hashes))
