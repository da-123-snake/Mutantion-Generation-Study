import subprocess
import os
from tqdm import tqdm
import json
def download(project,n):
    for i in range(0,n):
        cmd='defects4j checkout -p %s -v %sf -w defects4j_fixed/%s/%s_%s_fixed' % (project,i+1,project,project,i+1)
        print(cmd)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()


download("Chart",26)
download("Closure",133)
download("Lang",65)
download("Math",106)
download("Mockito",38)
download("Time",27)
download("Cli",40)
download("Codec",18)
download("Csv",16)
download("Gson",18)
download("JacksonCore",26)
download("Jsoup",93)


def bugdownload(project,n):
    for i in range(0,n):
        cmd='defects4j checkout -p %s -v %sb -w defects4j_bug/%s/%s_%s_bug' % (project,i+1,project,project,i+1)
        print(cmd)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()


bugdownload("Chart",26)
bugdownload("Closure",133)
bugdownload("Lang",65)
bugdownload("Math",106)
bugdownload("Mockito",38)
bugdownload("Time",27)
bugdownload("Cli",40)
bugdownload("Codec",18)
bugdownload("Csv",16)
bugdownload("Gson",18)
bugdownload("JacksonCore",26)
bugdownload("Jsoup",93)
