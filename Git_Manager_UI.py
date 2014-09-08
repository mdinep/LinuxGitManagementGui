#! /usr/bin/env python
import os,sys
import time
import getpass
import re
try:
	from Tkinter import *
	import tkMessageBox
	import tkFileDialog
except:
	print "Please install Tkinter before running this app"
	time.sleep(3)
	sys.exit()
	
currentDir = os.getcwd()
master = Tk()
master.resizable(width=FALSE, height=FALSE)
master.wm_title("Git Branch Management Tool")
directory = "empty"
comment = "none"

def createNew():
	if directory != "empty":
		os.system("git checkout master")
		os.system("git pull")
		os.system("git checkout -b " + e.get())
		os.system("git push origin")
		textBox.delete(1.0, END)
		textBox.insert(END, getBranches())
	else:
		tkMessageBox.showwarning("Warning", "Please set git repo directory")
		
def create():
	if directory != "empty":
		os.system("git checkout -b " + e.get() + " origin/" + e.get())
		textBox.delete(1.0, END)
		textBox.insert(END, getBranches())
	else:
		tkMessageBox.showwarning("Warning", "Please set git repo directory")
		
def checkout():
	if directory != "empty":
		os.system("git checkout " + e.get())
		textBox.delete(1.0, END)
		textBox.insert(end, getBranches())
	else:
		tkMessageBox.showwarning("Warning", "Please set git repo directory")
		
def delete():
	if directory != "empty":
		result = tkMessageBox.askquestion("Delete", "Are You Sure?", icon='warning')
		if result == 'yes':
			os.system("git checkout master")
			os.system("git branch -D " + e.get())
			textBox.delete(1.0, END)
			textBox.insert(END, getBranches())
		else:
			return
	else:
		tkMessageBox.showwarning("Warning", "Please set git repo directory")
		
def setDir():
	global directory
	directory = tkFileDialog.askdirectory(initialdir="/home/" + getpass.getuser(), title="Git Directory", mustexist=True)
	os.chdir(directory)
	validDir = getBranches()
	if len(validDir) < 1:
		tkMessageBox.showwarning("Warning", "Please select a valid git directory")
		directory = "empty"
	else:
		setDirectory.configure(bg="chartreuse", activebackground="pale green")
		textBox.insert(END, validDir)
		
def getBranches():
	branchList = os.popen("git branch -all").read()
	return branchList
	
def status():
	if directory != "empty":
		statWin = Toplevel()
		statWin.title("Branch Status")
		statWin.grid()
		status = os.popen("git status").read()
		sFrame = Frame(statWin)
		sFrame.grid(row=0, column=0)
		sbFrame = Frame(statWin)
		sbFrame.grid(row=1, column=0)
		sBox = Text(statWin, height=20, width=160)
		scroll = Scrollbar(statWin)
		sBox.pack(in_=sFrame, side=LEFT, fill=Y)
		scroll.pack(in_=sFrame, side=RIGHT, fill=Y)
		scroll.config(command=sBox.yview)
		sBox.config(yscrollcommand=scroll.set)
		closeButton = Button(statWin, text="Close", width=10, command=lambda: statWin.destroy())
		closeButton.pack(in_=sbFrame)
		sBox.insert(END, status)
		statWin.mainloop()
	else:
		tkMessageBox.showwarning("Warning", "Please set git repo directory")
		
def pull():
	if directory != "empty":
		os.system("git pull")
	else:
		tkMessageBox.showwarning("Warning", "Please set git repo directory")
		
def push():
	if directory != "empty":
		pushWin = Toplevel()
		pushWin.title("Commit comment")
		pushWin.grid()
		pFrame = Frame(pushWin)
		pFrame.grid(row=0, column=0, columnspan=2)
		label = Label(pFrame, text="Comment: ")
		label.pack(side=LEFT)
		com = Entry(pFrame, width=60, cursor="xterm")
		com.pack(side=RIGHT, padx=20, pady=20)
		comButton = Button(pushWin, text="Submit", width=20, command=lambda: submit(pushWin, com.get()), bg="dark grey")
		comButton.grid(row=1, column=0, pady=15)
		cancelButton = Button(pushWin, text="Cancel", width=20, command=lambda: pushWin.destroy(), bg="dark grey")
		cancelButton.grid(row=1, column=1, pady=15)
		pushWin.mainloop()
	else:
		tkMessageBox.showwarning("Warning", "Please set git repo directory")
		
def submit(pushWin, com):
	os.system("git add .")
	os.system("git commit -m \"" + com + "\"")
	os.system("git push")
	pushWin.destroy()
	
def exit():
	master.destroy()
	
top = Frame(master)
bottom = Frame(master, bd=30)
right = Frame(master)
top.grid(row=0, column=0)
bottom.grid(row=1, column=0)
right.grid(row=0, column=1, rowspan=2)

setDirectory = Button(master, text="Set Git Directory", width=12, command=setDir, bg="orange red", activebackground="tomato", bd=3)
setDirectory.pack(in_=top, side=TOP, anchor=W, padx=6, pady=20)
e = Entry(master, text="Branch Name", width=40)
L1 = Label(master, text="Branch Name: ")
clearButton = Button(master, text="x", command=lambda: e.delete(0,END), bg="dark grey", height=1)
L1.pack(in_=top, side=LEFT)
e.pack(in_=top, side=LEFT)
clearButton.pack(in_=top, side=RIGHT)
e.focus_set()

buttonFrame = Frame(bottom, bd=8)
buttonFrame.pack()
pullButton = Button(master, text="Pull Changes", width=10, command=pull, bg="light sky blue", bd=3)
pullButton.pack(in_=buttonFrame, side=LEFT)
pushButton = Button(master, text="Commit Changes", width=10, command=push, bg="light sky blue", bd=3)
pushButton.pack(in_=buttonFrame, side=LEFT)
statusButton = Button(master, text="Get Status", width=10, command=status, bg="light sky blue", bd=3)
statusButton.pack(in_=buttonFrame, side=LEFT)

createNewButton = Button(master, text="Create New Remote Branch", width=30, command=createNew)
createNewButton.pack(in_=bottom)
createButton = Button(master, text="Create Branch Tracking Remote", width=30, command=create)
createButton.pack(in_=bottom)
checkoutButton = Button(master, text="Checkout Existing Branch", width=30, command=checkout)
checkoutButton.pack(in_=bottom)
deleteButton = Button(master, text="Delete Local Branch", width=30, command=delete)
deleteButton.pack(in_=bottom)
exitButton = Button(master, text="Exit", width=30, command=exit)
exitButton.pack(in_=bottom)

scroll = Scrollbar(master)
textBox = Text(master, height=20, width=85)
scroll.pack(in_=right, side=RIGHT, fill=Y)
textBox.pack(in_=right, side=LEFT, fill=Y)
scroll.config(command=textBox.yview)
textBox.config(yscrollcommand=scroll.set)

mainloop()