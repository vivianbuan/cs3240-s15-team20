from html.parser import HTMLParser

class MainParser(HTMLParser):
	reading = False
	divs = 0
	printing = False

	def handle_starttag(self, tag, attrs):
		if tag == "div" and ('id','Reports') in attrs:
			self.reading = True
			self.divs=0
		if self.reading and tag == "div":
			self.divs = self.divs + 1
		if self.reading and tag == "a":
			for item in attrs:
				if item[0] == "href":
					string = item[1]
					string = string.split('/')
					string = string[3]
					print("ID: " + string)
		if self.reading and tag == "h3":
			print("Title: ", end="")
			self.printing = True
		if self.reading and tag == "h4":
			print("Date: ", end="")
			self.printing = True
	def handle_endtag(self, tag):
		if self.reading and tag == "div":
			self.divs = self.divs - 1
		if self.divs <= 0:
			self.reading = False
		if self.reading:
			if tag == "h3" or tag == "h4" or tag == "a":
				self.printing = False
				print()
	def handle_data(self, data):
		if self.reading:
			if self.printing:
				print(data, end="")
	def handle_charref(self, name):
		if name.startswith('x'):
			c = chr(int(name[1:], 16))
		else:
			c = chr(int(name))
		if self.reading:
			if self.printing:
				print(c, end="")


"""class MainParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
    def handle_data(self, data):
        print("Encountered some data  :", data)"""


"""from html.entities import name2codepoint

class MainParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("     attr:", attr)
    def handle_endtag(self, tag):
        print("End tag  :", tag)
    def handle_data(self, data):
        print("Data     :", data)
    def handle_comment(self, data):
        print("Comment  :", data)
    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)
    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)
    def handle_decl(self, data):
        print("Decl     :", data)"""