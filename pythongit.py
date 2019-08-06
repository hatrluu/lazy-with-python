import subprocess
import csv
import sys

PIPE = subprocess.PIPE
source = "C:/Development/remote/eisuite/"
git = ".git"
target = "C:/Development/projects/CriterionSys/criterion-sys3/"
commitNames = [
   
]
array = []

def getDiff(commitName):
    print("getDiff step")
    out = subprocess.check_output(["git","--git-dir="+source+git, "diff-tree","--no-commit-id","--name-only","-r",commitName]).splitlines()
    for i in out:
        print(i)
        array.append(i.decode("utf8"))
    return array

def copyDiff(array):
    print("copyDiff step")
    for i in array:
        print(source+i +" copy to "+ target+i)
        subprocess.call(["cp",source+i,target+i])


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        for i in range(len(commitNames)):
            changes = getDiff(commitNames[i])
            copyDiff(changes)
    else:
        if(len(sys.argv) == 2):
            copyDiff(getDiff(sys.argv[1]))
    pass
