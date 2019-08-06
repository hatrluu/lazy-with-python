import subprocess
import csv
import sys


PIPE = subprocess.PIPE
source = "C:/Development/remote/eisuite/"
git = ".git"
target = "C:/Development/projects/CriterionSys/criterion-sys3/"
array = []
def getDiff(commitName):
    print("getDiff step")
    out = subprocess.check_output(["git","--git-dir="+source+git, "diff-tree","--no-commit-id","--name-only","-r",commitName]).splitlines()
    for i in out:
        # print(i)
        array.append(i.decode("utf8"))
    return array

    
if __name__ == "__main__":
    if(len(sys.argv) == 2):
        changes = getDiff(sys.argv[1])
        for i in changes:
            print(i)
    else:
        print("Need 1 argument")
    pass