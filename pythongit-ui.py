#Productively lazy project

from tkinter import *
from tkinter.filedialog import askdirectory
import subprocess

git = '/.git'

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
		
def getLatestCommits():
	out = subprocess.check_output(('git','--git-dir',srcPath.get()+git,'log','-30','--pretty=oneline')).splitlines()
	for i in out:
		latestCommitsBox.insert(END,i.decode("utf8"))

def doubleClick():
	commitList.insert(0,(latestCommitsBox.get(latestCommitsBox.curselection()[0]).split()[0]))

def getDiff():
	changes.delete(0,END)
	if(commitList.size()>0):
		for commitName in commitList.get(0,END):
			out = subprocess.check_output(["git","--git-dir="+srcPath.get()+git, "diff-tree","--no-commit-id","--name-only","-r",commitName]).splitlines()
			#print('==========Printing from {}==========='.format(commitName))
			for i in out:
				#print(i.decode('utf8'))
				changes.insert(END,i.decode("utf8"))

def copyDiff():
	print("copyDiff step")
	if(changes.size()!=0):
		progressWindow = Toplevel()
		progressWindow.geometry('400x500')
		progressBox = Listbox(progressWindow)
		progressBox.pack(fill=BOTH)
		for i in changes.get(0,END):
			print(srcPath.get()+'/'+i +" copy to "+ destPath.get()+'/'+i)
			subprocess.call(["cp",srcPath.get()+'/'+i,destPath.get()+'/'+i])
			progressBox.insert(END,srcPath.get()+'/'+i +" copy to "+ destPath.get()+'/'+i)
		Button(progressWindow,text='Close',command=progressWindow.destroy).pack(side=BOTTOM)
		progressWindow.mainloop()

def getCurrentBranch(pth):
	ps = subprocess.Popen(("git","--git-dir="+pth+git, "branch"), stdout=subprocess.PIPE)
	output = subprocess.check_output(('grep', "'*'"), stdin=ps.stdout)
	ps.wait()
	return output.decode("utf8").strip("*")


mainFrame = Tk()
mainFrame.geometry('700x700')
mainFrame.title('Some Weird App')

#Select Path Frame
selectPathFrame = Frame(mainFrame)
selectPathFrame.pack()

srcFolderLbl = Label(selectPathFrame, text='Source Folder').grid(row=0)
destFolderLbl = Label(selectPathFrame, text='Destination Folder').grid(row=1)
srcPath = Entry(selectPathFrame,width=50)
srcPath.grid(row=0,column=1)
srcPath.insert(END,'D:/Development/remote/eisuite')
destPath = Entry(selectPathFrame,width=50)
destPath.grid(row=1,column=1)
destPath.insert(END,'D:/Development/projects/CriterionSys/criterion-sys3')
srcPathBtn = Button(selectPathFrame, text='Browse', width=10, command=lambda: browse_button('srcPath'))
srcPathBtn.grid(row=0,column=2)
destPathBtn = Button(selectPathFrame, text='Browse', width=10, command=lambda: browse_button('destPath'))
destPathBtn.grid(row=1,column=2)
srcBranch = Label(selectPathFrame,text=getCurrentBranch(srcPath.get())).grid(row=0,column=3)
destBranch = Label(selectPathFrame,text=getCurrentBranch(destPath.get())).grid(row=1,column=3)

#Get Latest Commit Names Frame
getLatestCommitsFrame = Frame(mainFrame)
getLatestCommitsLabelFrame = LabelFrame(getLatestCommitsFrame,text='Lastest Commit(s)')

getLatestCommitsFrame.pack(fill=X)
getLatestCommitsLabelFrame.pack(fill=X)

getLatestCommitsBtn = Button(getLatestCommitsLabelFrame,text='Get Latest Commit(s)',command=getLatestCommits)
getLatestCommitsBtn.pack()

latestCommitsBox = Listbox(getLatestCommitsLabelFrame)
latestCommitsBox.pack(fill=BOTH)
latestCommitsBox.bind('<Double-1>', lambda x: doubleClick())

#getDiff Frame
getDiffFrame = Frame(mainFrame)
getDiffLabelFrame = LabelFrame(getDiffFrame,text='Commit Name(s)')

getDiffFrame.pack()
getDiffLabelFrame.pack()

commitInput = Entry(getDiffLabelFrame,width=80)
commitAdd = Button(getDiffLabelFrame, text='+', width=3, command=lambda: modifyCommit('add', commitInput.get()))
commitDelete = Button(getDiffLabelFrame, text='-', width=3, command=lambda: modifyCommit('delete', commitInput.get()))
moveUp = Button(getDiffLabelFrame, text='^', width=3, command=lambda: move('up'))
moveDown = Button(getDiffLabelFrame, text='v', width=3, command=lambda: move('down'))
commitList = Listbox(getDiffLabelFrame, height=5, width=80)
getDiffBtn = Button(getDiffLabelFrame, text='Get Diff', width=10, command=getDiff)

commitInput.grid(row=0,column=0)
commitAdd.grid(row=0,column=1)
moveUp.grid(row=1,column=1)
moveDown.grid(row=2,column=1)
commitDelete.grid(row=3,column=1)
commitList.grid(row=1, rowspan=3)
getDiffBtn.grid(row=4)

#copyDiff Frame
copyDiffFrame = Frame(mainFrame,relief=SUNKEN)
copyDiffLabelFrame = LabelFrame(copyDiffFrame, text='Changes List', bg='white')

scrollbar = Scrollbar(copyDiffLabelFrame) 
scrollbar.pack(side = RIGHT, fill = Y ) 
copyDiffFrame.pack(fill=X)
copyDiffLabelFrame.pack(fill=X)

changes = Listbox(copyDiffLabelFrame, height=10, width=50)
copyDiff = Button(copyDiffLabelFrame, text='Copy Diff', width=10, command=copyDiff)
scrollbar.config( command = changes.yview)
changes.pack(fill = BOTH)
copyDiff.pack()

mainFrame.mainloop()
