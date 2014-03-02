import h
import sys

"""State represent state.
	0 is original state
	1 is to in Forums
	2 is to in Sub"""
state = 0
forumNum = 0
forumPage = 0
subNum = 0
subPage = 0
def ctrl(pn=0):
	flow = ctrlDict[pn]
	flow()

def ori():
	global state
	global forumNum
	global forumPage
	link.getForums();

	cmd = input("Please input your command; goto X for Xid Forums, quit for exit\n");
	if cmd.find("goto")!=-1:
		cmd, num = cmd.split(' ')
		state = 1
		forumNum = int(num)
		forumPage = 1
	elif cmd.find("quit")!=-1:
		print("Byebye, Zombie!")
		sys.exit()
	else:
		print("TAT Don't know your demand, try again")
	ctrl(state)

def inForum():
	global state
	global forumNum
	global forumPage
	global subNum
	global subPage

	link.getRoot(forumNum, forumPage)
	cmd=input("goto ID for goto sub, next for next page, return for goto upper layer\n")
	if cmd.find("goto")!=-1:
		cmd, num = cmd.split(' ')
		state = 2
		subNum = int(num)
		subPage = 1
	elif cmd.find("return")!=-1:
		state = 0
	elif cmd.find("next")!=-1:
		forumPage +=1
		link.getRoot(forumNum, forumPage)
	else:
		print("TAT Don't know your demand, try again")
	ctrl(state)

def inSub():
	global state
	global subNum
	global subPage

	link.getSub(subNum, subPage)
	cmd=input("next for goto next page, return for goto upper layer\n")
	if cmd.find("return")!=-1:
		state = 1
	elif cmd.find("next")!=-1:
		subPage +=1
	else:
		print("TAT Don't know your demand, try again")
	ctrl(state)

ctrlDict = {
	0:ori,
	1:inForum,
	2:inSub}

link = h.ConnectAcfun()
ctrl(state)