import os
import json
import os
import time
import subprocess
import json
def generate_mutant(project,project_id,savepath,llm,d4j_path = 'defects4j',
                                d4jbug_path = 'defects4j_fixed'):
    """
    d4j_path : The installation path for Defects4J
    d4jbug_path: The download path for the fixed version projects in Defects4J
    """
    start_time=time.time()
    id=0
    print("..............................................................",project,project_id+1,"......................................................................")
    patch_path = f'{d4j_path}/framework/projects/{project}/patches/{project_id+1}/src.patch'
    mu_list=[]

    try:
        with open(patch_path, 'r',errors='ignore') as patch:
            patch_content = patch.readlines()  
    except Exception as e:
        return
        
    fixed_bug=d4jbug_path + "/%s/%s_" % (project,project) +str(project_id+1)+"_fixed/"+patch_content[2][6:]
    fixed_bug=fixed_bug.strip()
    try:
        liness = open(fixed_bug, "r").read().strip().splitlines()
    except Exception as e:
        return

    patch_lines=[]
    # java_classes=[]
    for i in patch_content:
        if "@@" in i:
            patch_lines.append(i)
    for patch_line in patch_lines:
        split_result = patch_line.split(" ")[1] 
        start_line, mutant_lines = map(int, split_result.split(','))
        start_line=-start_line
        end_line=start_line+mutant_lines

        for i in range(start_line,end_line):
            dict={}
            maskcode=""
            predict_words=[]
            cmd='./mBERT.sh -in=%s -N=1 -l=%s'%(fixed_bug,i)
            log_test=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            output = log_test[0].decode('utf-8')
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
            dict['filepath']=fixed_bug
            dict['aftercode']=aftercode
            mu_list.append(dict)
            print(dict)
    save_path='mBERTm/mbert_mutant/%s/%s-' % (project,project) +str(project_id+1)+'.json' 
    print(save_path)
    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(mu_list, file, ensure_ascii=False,indent=4)

for i in range(0,1):
    generate_mutant("Chart",i)
