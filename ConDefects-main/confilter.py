import subprocess
import os
import json
import math

import math
def filter(mutant_path,save_path):
    print("--------------------filter----------------------")
    good=0
    notk=0

    filter_test=[]

    with open(mutant_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for mutant in data:
        try:
            file_path=mutant['filepath'].replace("\\","/")
            with open(file_path, "r", encoding="utf-8") as f:
                mutantfile = f.readlines()
            if mutant['precode'] in mutantfile[mutant['line']-1] and mutant['precode']!=mutant['aftercode']and mutant['precode']!="\n":
                if len(mutant['precode'].strip()) > 0:
                    if mutant['precode'].strip()[0].isalpha():
                        filter_test.append(mutant)
                        good+=1
                        if mutant['fail_test:']=="":
                            notk+=1
                else:
                    if len(mutant['aftercode'].strip()) > 0:
                        if mutant['aftercode'].strip()[0]!='/':
                            filter_test.append(mutant)
                            good+=1
                            if mutant['fail_test:']=="":
                                notk+=1
                    else:
                        filter_test.append(mutant)
                        good+=1
                        if mutant['fail_test:']=="":
                            notk+=1
        except Exception as e: 
            continue

    with open(save_path, 'w', encoding='utf-8') as file1:
        json.dump(filter_test, file1, ensure_ascii=False,indent=4)
    print("all:",good,"    killed",good-notk,"      score:",(good-notk)/good)
    
mutant_path = 'your own path'
save_path = 'your own path'
filter(mutant_path,save_path)