import os
import json
import glob
import json
import subprocess
import torch
import time
def generate_mutant(save_path):
    mu_list=[]
    id=0
    print("...........................................start generate..............................................................")
    folder_path = 'ConDefects-main/java2024-0306'
    faultLocations = glob.glob(os.path.join(folder_path, '**/*.txt'), recursive=True)

    dd=0
    fail=0
    for location in faultLocations:
        dd+=1
        print(dd,"****************************",location)
        try:
            with open(location, 'r',errors='ignore') as patch:
                patch_line = patch.readlines()  
        except Exception as e:
            continue
        javaFile=location.replace("faultLocation.txt","correctVersion.java")
        try:
            liness = open(javaFile, "r",errors='ignore').read().strip().splitlines()
        except Exception as e:
            continue
 
        start_line=int(patch_line[0])-6
        if start_line<1:
            start_line=1
        end_line=int(patch_line[0])+6
        if end_line>len(liness):
            end_line=len(liness)
        for i in range(start_line,end_line):
            dict={}
            maskcode=""
            predict_words=[]
            cmd='./mBERT.sh -in=%s -N=1 -l=%s'%(javaFile,i)
            log_test=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            output = log_test[0].decode('utf-8')
            #print(output)
            try:
                output1=output.split("Here is the standard output of the command:")[1].split("{'score':")[0]
                output2=output1.split("\\n")
                for j in output2:
                    if "mask" in j:
                        maskcode=j
                for k in range(4):
                    predict=output.split("Here is the standard output of the command:")[1].split("{'score':")[k+1].split("\n")[-2]
                    predict_words.append(predict)

            except Exception as e:
                continue
            id+=1
            precode=liness[i-1]
            aftercode=""
            for word in predict_words:
                temp=maskcode.replace("<mask>",word).strip()
                if precode.replace(" ","")!= temp.replace(" ",""):
                    aftercode=maskcode.replace("<mask>",word)
                    break
            if len(aftercode)==0:
                continue
            dict['id']=id
            dict['line']=i
            dict['precode']=precode
            dict['filepath']=javaFile
            dict['aftercode']=aftercode
            mu_list.append(dict)
 
    print(save_path)
    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(mu_list, file, ensure_ascii=False,indent=4)
    print("fail times:",fail)

save_path = 'your own path'
generate_mutant(save_path)