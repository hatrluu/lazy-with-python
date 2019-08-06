#Productively lazy project

from tkinter import *
from tkinter.filedialog import askdirectory
import subprocess

def browse_button(input):
	folder_name = askdirectory()
	if(eval(input+'.get()!=\'\'')):
		eval(input+'.delete(0,END)')
	eval(input+'.insert(END, folder_name)')
	
def modifyCommit(direction,input):
	input = input.strip()
	if(direction=='add' and input!=''):
		commitList.insert(0,input)
		commitInput.delete(0,'end')
	elif(commitList.size()>0):
		if(commitList.curselection()):
			commitList.delete(commitList.curselection()[0])
		else:
			commitList.delete(0)
def move(direction):
	if(commitList.size()!=0):
		curSelectionVal = commitList.get(commitList.curselection()[0])
		if(direction=='up'):
			commitList.insert(commitList.curselection()[0]-1,curSelectionVal)
			commitList.delete(commitList.curselection()[0])
		else:
			print(commitList.curselection()[0])
			commitList.insert(commitList.curselection()[0]+2,curSelectionVal)
			commitList.delete(commitList.curselection()[0])
def getDiff():
	changes.delete(0,END)
	git = '/.git'
	if(commitList.size()>0):
		for commitName in commitList.get(0,END):
			out = subprocess.check_output(["git","--git-dir="+srcPath.get()+git, "diff-tree","--no-commit-id","--name-only","-r",commitName]).splitlines()
			#print('==========Printing from {}==========='.format(commitName))
			for i in out:
				#print(i.decode('utf8'))
				changes.insert(END,i.decode("utf8"))

def copyDiff():
	print("copyDiff step")
	progressWindow = Toplevel()
	progressWindow.geometry('500x500')
	progressBox = Listbox(progressWindow, height=10, width=50)
	progressBox.pack()
	for i in changes.get(0,END):
		print(srcPath.get()+i +" copy to "+ destPath.get()+i)
		progressBox.insert(END,srcPath.get()+i +" copy to "+ destPath.get()+i)#subprocess.call(["cp",source+i,target+i])
	progressWindow.mainloop()
    
	
mainFrame = Tk()
mainFrame.geometry('600x450')
mainFrame.title('Some Weird App')

#First Frame
firstFrame = Frame(mainFrame)
firstFrame.pack()

srcFolderLbl = Label(firstFrame, text='Source Folder').grid(row=0)
destFolderLbl = Label(firstFrame, text='Destination Folder').grid(row=1)
srcPath = Entry(firstFrame,width=50)
srcPath.grid(row=0,column=1)
destPath = Entry(firstFrame,width=50)
destPath.grid(row=1,column=1)
srcPathBtn = Button(firstFrame, text='Browse', width=10, command=lambda: browse_button('srcPath'))
srcPathBtn.grid(row=0,column=2)
destPathBtn = Button(firstFrame, text='Browse', width=10, command=lambda: browse_button('destPath'))
destPathBtn.grid(row=1,column=2)

#Second Frame
secondFrame = Frame(mainFrame)
secondLabelFrame = LabelFrame(secondFrame,text='Commit Name(s)')

secondFrame.pack()
secondLabelFrame.pack()

commitInput = Entry(secondLabelFrame,width=50)
commitAdd = Button(secondLabelFrame, text='+', width=3, command=lambda: modifyCommit('add', commitInput.get()))
commitDelete = Button(secondLabelFrame, text='-', width=3, command=lambda: modifyCommit('delete', commitInput.get()))
moveUp = Button(secondLabelFrame, text='^', width=3, command=lambda: move('up'))
moveDown = Button(secondLabelFrame, text='v', width=3, command=lambda: move('down'))
commitList = Listbox(secondLabelFrame, height=5, width=50)
getDiffBtn = Button(secondLabelFrame, text='Get Diff', width=10, command=getDiff)

commitInput.grid(row=0,column=0)
commitAdd.grid(row=0,column=1)
moveUp.grid(row=1,column=1)
moveDown.grid(row=2,column=1)
commitDelete.grid(row=3,column=1)
commitList.grid(row=1, rowspan=3)
getDiffBtn.grid(row=4)

#Third Frame
thirdFrame = Frame(mainFrame,relief=SUNKEN)
thirdLabelFrame = LabelFrame(thirdFrame, text='Changes List', bg='white')

scrollbar = Scrollbar(thirdLabelFrame) 
scrollbar.pack( side = RIGHT, fill = Y ) 
thirdFrame.pack()
thirdLabelFrame.pack()

changes = Listbox(thirdLabelFrame, height=10, width=50)
copyDiff = Button(thirdLabelFrame, text='Copy Diff', width=10, command=copyDiff)
scrollbar.config( command = changes.yview)
changes.pack(fill = BOTH)
copyDiff.pack()

mainFrame.mainloop()