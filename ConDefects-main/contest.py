import os
import json
import openai
import os
import subprocess
import glob
import json


def mutant_test(mutantfile,savepath):
    mu_list=[]
    id=0
    print("...........................................start test..............................................................")
    print("****************************",mutantfile)
    with open(mutantfile, 'r') as f:
        data = json.load(f)
    test=[]
    sum=0
    compile=0
    test_pass=0
    for mutant in data:
        sum+=1
        if sum%20==0:
            print("mutant",sum,"testing......")
        dict={}
        filepath=mutant['filepath'].replace("\\","/").replace('java2024-0304','java2024-0306').replace('java2024-0406','java2024-0306')
        task=filepath.split('/')[1]
        program_id=filepath.split('/')[3]
        try:
            oricode=open(filepath,"r",errors='ignore').read()
            liness = open(filepath, "r",errors='ignore').read().strip().splitlines()
            liness[mutant['line']-1]=mutant['aftercode']
            with open(filepath, "w") as file:
                file.write('\n'.join(liness))
        except Exception as e:
            print(filepath,"failure")
            open(filepath, "w").write(oricode)
            continue
        cmd="timeout 600 python ConDefects.py run -w ConDefects-main/java2024-0306 -s %s"%(task)
        try:
            log=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()

            tasks=log[0].decode('utf-8').split("--------------------------------------------------")
            for mytask in tasks:
                if program_id in mytask:
                    result=mytask
                    break
            if "Error: Test failed." not in result:
                compile+=1
                fail_tests=result.split("fail test:\n")[1].split("pass rate:")[0]
                if fail_tests.strip()=='':
                    test_pass+=1
                dict["mutant_id:"]=mutant['id']
                dict["line"]=mutant["line"]
                dict["filepath"]=mutant["filepath"]
                dict["precode"]=mutant["precode"]
                dict["aftercode"]=mutant["aftercode"]
                dict["fail_test:"]=fail_tests
                test.append(dict)
        except Exception as e:
            open(filepath, "w").write(oricode)
            continue
        open(filepath, "w").write(oricode)

    with open(savepath, 'w', encoding='utf-8') as file1:
        json.dump(test, file1, ensure_ascii=False,indent=4)
    
    print("sum mutant:",sum)
    print("compile_num:",compile)
    print("kill:",compile-test_pass)
    print("score:",(compile-test_pass)/compile)

mutantfile = "your own path"
savepath = 'your own path'
mutant_test(mutantfile,savepath)
