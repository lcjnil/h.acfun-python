import httplib2
import urllib.request, urllib.parse
import json
import sys
import re
class ConnectAcfun(object):
	def __init__(self):
		self.h = httplib2.Http(".cache")
		self.access_token="null"
		self.forumsList=list()
		self.used = False
		res, con = self.h.request("http://h.acfun.tv/api/Metadata")
		con = json.loads(con.decode("utf8"))
		if con["status"]!=200:
			print("Connection not sussess")
			sys.exit()
		self.access_token=con["access_token"]
		print("Connection sussess!!!")
	def getForums(self):
		res, con = self.h.request("http://h.acfun.tv/api/Forums")
		con = json.loads(con.decode("utf8"))
		forums = con['model']['ArrayOfForumGroup']['ForumGroup']
		self.__printForums(forums)
		self.used = True

	def __printForums(self,forums):
		for eachForumGroup in forums:
			print(eachForumGroup['Area'])
			for eachForum in eachForumGroup['ForumNames']['string']:
				if not self.used:
					self.forumsList.append(eachForum)
				print("\t",len(self.forumsList),":",eachForum,sep="")

	def getRoot(self, forumNumber, pn=1):
		forumNumber -= 1
		print(self.forumsList[forumNumber])
		print()

		url = 'http://h.acfun.tv/api/thread/root?forumName='+urllib.parse.quote(self.forumsList[forumNumber])+'&pn='+ str(pn)
		res, con = self.h.request(url)
		con = json.loads(con.decode("utf8"))
		con = con['model']
		for eachSub in con:
			print(self.__formatTime(eachSub['UpdateDateTime']), eachSub['UID'], "\t", eachSub['ID'], "Response", eachSub['ResponseCount'])
			print(eachSub['Title'])
			print(self.__formatSub(eachSub['Content']))
			print()
	def getSub(self, subNumber, pn=1, count=20):
		parentId=subNumber
		url="http://h.acfun.tv/api/thread/sub?parentId="+str(parentId)+"&pn="+str(pn)+"&count="+str(count)
		res, con = self.h.request(url)
		con = json.loads(con.decode("utf8"))
		con = con['model']
		for eachSub in con[::-1]:
			print(self.__formatTime(eachSub['UpdateDateTime']), eachSub['UID'], "\t", eachSub['ID'], "Response", eachSub['ResponseCount'])
			print(self.__formatSub(eachSub['Content']))
			print()
	def __formatTime(self, time):
		"""Format Sub time!"""
		pat = re.compile('\d\d-\d\dT\d\d:\d\d')
		ftime = pat.findall(time)[0]
		return ftime[0:5]+" "+ftime[6:11]
	def __formatSub(self, sub):
		"""Format Sub!"""
		pat = re.compile('<br/>\s*')
		return urllib.parse.unquote(pat.sub("\n", sub))