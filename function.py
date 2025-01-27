from openai import OpenAI
import httpx
import os
import time
import re
import glob
import subprocess
import json

def generate_mutant(project,project_id,savepath,llm,d4j_path = 'defects4j',
                                d4jbug_path = 'defects4j_fixed'):
    """
    d4j_path : The installation path for Defects4J
    d4jbug_path: The download path for the fixed version projects in Defects4J
    """
    id=0
    print("..............................................................",project,project_id+1,"......................................................................")

    mu_list=[]
    fail=0
    patch_path = f'{d4j_path}/framework/projects/{project}/patches/{project_id+1}/src.patch'
    try:
        with open(patch_path, 'r',errors='ignore') as patch:
            patch_content = patch.readlines()  
    except Exception as e:
        return

    fixed_bug = d4jbug_path + "/%s/%s_" % (project,project) +str(project_id+1)+"_fixed/"+patch_content[2][6:]
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
        end_line=start_line+mutant_lines-1
        mutant_code=""
        for i in liness[start_line-1:end_line]:
            mutant_code=mutant_code+i+'\n'
        if(start_line>=len(liness)):
            continue
        end_line=start_line
        while('*/' not in liness[start_line-1]):
            start_line=start_line-1
            if start_line<1:
                break
        while('/**' not in liness[end_line-1]):
            end_line=end_line+1
            if end_line>=len(liness):
                break
        ori_code=""
        num_lines=(end_line-start_line) 
        for i in liness[start_line:end_line-1]:
            ori_code=ori_code+i+'\n'
        prompt="""
        %s\n
        Above is the original code. your task is to generate %s mutants in original code(notice:mutant refers to mutant in software engineering, i.e. making subtle alterations to the original code) in :
        %s\n

        as follows are some examples of mutants which you can refer to:
            {
            "precode": "n = (n & (n - 1));",
            "aftercode": " n = (n ^ (n - 1));"                                        
            },
            {
            "precode": "  while (!queue.isEmpty()) {",
            "aftercode": " while (true) { "             
            },                                        
            {
            "precode": "return depth==0;",
            "aftercode": "return true;"
            },                                        
            {
            "precode": "ArrayList r = new 
            ArrayList();r.add(first).addll(subset);to_add(r)",
            "aftercode": "to_add.addAll(subset);"
            },                               
            {
            "precode": "c = bin_op.apply(b,a);",
            "aftercode": "c = bin_op.apply(a,b);",    
            },                              
            {
            "precode":"while (Math.abs(x-approx*approx) > epsilon) { "     
            "aftercode": " while (Math.abs(x-approx) > epsilon) {"
            },                          
        #Requirement:
        1.Provide generated mutants directly
        2.A mutation can only occur on one line
        3.Your output must be like:
        [
            {
                "id":,
                "line":,
                "precode":"",
                "filepath":"kk",
                "aftercode":""
            }
        ]
        Where "id" stand for mutant serlal number,"Line" represent the line number of the mutated,"precode" represent the line of code before mutation and it can't be empty,"aftercode" represent the line of code after mutation
        4.Prohibit generating the exact same mutants
        5.all write in a json file

        """%(ori_code,mutant_lines,mutant_code)
        num=0
        for tem in range(3): 
            try:
                generated_text = llm._call(prompt)
                pattern = r'\[.*\]'
                generated_text = re.findall(pattern,generated_text,re.DOTALL)
                try:
                    mu=json.loads(generated_text[0])
                    for i in range(len(mu)):
                        id+=1
                        mu[i]['id']=id
                        mu[i]['filepath']=fixed_bug
                        for k in range(num_lines):
                            if mu[i]['precode'] in liness[start_line+k-1]:
                                mu[i]['line']=start_line+k
                                continue
                    mu_list.extend(mu)
                    break
                except Exception as e:
                    num+=1
                    continue
            except Exception as e:
                num+=1
                continue
        if num>=5:
            fail+=1
    save_path = savepath + '/%s/%s-' % (project,project) +str(project_id+1)+'.json' 
    print(save_path)
    with open(save_path, 'w', encoding='utf-8') as file:
        json.dump(mu_list, file, ensure_ascii=False,indent=4)
    print("fail times:",fail)

def con_generate_mutant(llm,conpath = 'ConDefects-main/java2024-0306',savepath='ConDefects-main/java2024-0306-mutant'):

    mu_list=[]
    id=0
    print("...........................................start generate..............................................................")
    folder_path = conpath
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
 
        start_line=int(patch_line[0])-2
        if start_line<1:
            start_line=1
        end_line=int(patch_line[0])+2
        if end_line>len(liness):
            end_line=len(liness)
        fault_line=int(patch_line[0])
        mutant_code=""
        for i in liness[start_line-1:end_line]:
            mutant_code=mutant_code+i+'\n'
        func=['long','Object','bool','class','public']
        while('static' not in liness[start_line-1]):
            start_line=start_line-1
            if start_line<1:
                break
            loop=False
            for i in func:
                if (i in liness[start_line-1]) and (liness[start_line-2]=='' or liness[start_line-2]=='\t'):
                    loop=True
                    break
            if loop:
                break
        while('static' not in liness[end_line-1]):
            end_line=end_line+1
            if end_line>=len(liness):
                    break
            loop=False
            for i in func:
                if (i in liness[end_line-1]) and (liness[end_line-2]=='' or liness[start_line-2]=='\t'):
                    loop=True
                    break
            if loop:
                break
            if '/*' in liness[end_line-1]:
                break
        ori_code=""
        num_lines=(end_line-start_line) 
        for i in liness[start_line-1:end_line-1]:
            ori_code=ori_code+i+'\n'
        

        promptt="""

        %s\n
        Above is the original code. your task is to generate 5 mutants(notice:mutant refers to mutant in software engineering, i.e. making subtle alterations to the original code) in the following code:
        %s\n

        as follows are some examples of mutants which you can refer to:
            {
            "precode": "n = (n & (n - 1));",
            "aftercode": " n = (n ^ (n - 1));"                                        
            },
            {
            "precode": "  while (!queue.isEmpty()) {",
            "aftercode": " while (true) { "             
            },                                        
            {
            "precode": "return depth==0;",
            "aftercode": "return true;"
            },                                        
            {
            "precode": "ArrayList r = new 
            ArrayList();r.add(first).addll(subset);to_add(r)",
            "aftercode": "to_add.addAll(subset);"
            },                               
            {
            "precode": "c = bin_op.apply(b,a);",
            "aftercode": "c = bin_op.apply(a,b);",    
            },                              
            {
            "precode":"while (Math.abs(x-approx*approx) > epsilon) { "     
            "aftercode": " while (Math.abs(x-approx) > epsilon) {"
            },                          
        #Requirement:
        1.Provide generated mutants directly
        2.A mutation can only occur on one line
        3.Your output must be like:
        [
            {
                "id":,
                "line":,
                "precode":"",
                "filepath":"kk",
                "aftercode":""
            }
        ]
        Where "id" stand for mutant serlal number,"Line" represent the line number of the mutated,"precode" represent the line of code before mutation and it can't be empty,"aftercode" represent the line of code after mutation
        4.Prohibit generating the exact same mutants
        5.all write in a json file
        """%(ori_code,mutant_code)
        #print(promptt)
        num=0
        for tem in range(3): 
            try:
                generated_text = llm._call(promptt)
                pattern = r'\[.*\]'
                generated_text = re.findall(pattern,generated_text,re.DOTALL)
                try:
                    mu=json.loads(generated_text[0])

                    for i in range(len(mu)):
                        id+=1
                        mu[i]['id']=id
                        mu[i]['filepath']=javaFile
                        for k in range(num_lines):
                            if mu[i]['precode'] in liness[start_line+k-1]:
                                mu[i]['line']=start_line+k
                                continue
                    mu_list.extend(mu)
                    break
                except Exception as e:
                    num+=1
                    continue
            except Exception as e:
                num+=1
                continue
        if num>=5:
            fail+=1
    print('savepath:',savepath)
    with open(savepath, 'w', encoding='utf-8') as file:
        json.dump(mu_list, file, ensure_ascii=False,indent=4)
    print("fail times:",fail)
