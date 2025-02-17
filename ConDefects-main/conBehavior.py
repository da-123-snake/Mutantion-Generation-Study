import subprocess
import os
import json
import math

import math

def find_fault(mutant_path):
    find_fault=0
    print("--------------------start----------------------")
    with open(mutant_path, "r", encoding="utf-8") as f:
        mutant = json.load(f)
    with open("faultyVersion_failtest.json", "r", encoding="utf-8") as f:
        faults = json.load(f)
    for fault in faults:
        try:
            fault_fail_tests=fault["fail tests:"].split("\n")
            boolfault=False
            for m in mutant:
                if fault["filepath"] in m['filepath'].replace("\\","/"):
                    for faul_fail_test in fault_fail_tests[0:-1]:
                        if faul_fail_test.strip() in m["fail_test:"]:
                            boolfault=True
                            break
            if boolfault:
                find_fault+=1
        except Exception as e:
            continue
    print("find fault:",find_fault,"/",len(faults))

def ochiai(mutant_path):
    fault_similarity_num=0
    mutant_number=0
    mutant_ochiai=0
    mutant_all=[]

    with open(mutant_path, "r", encoding="utf-8") as f:
        mutant = json.load(f)
    with open("faultyVersion_failtest.json", "r", encoding="utf-8") as f:
        faults = json.load(f)
    for fault in faults:
        for m in mutant:
            if fault["filepath"] in m['filepath'].replace("\\","/"):
                mutant_all.append(m)
    for fault in faults:
        if_fault_similarity=False
        fault_fail_tests=fault["fail tests:"].split("\n")
        for m in mutant_all:
            try:
                mutant_number+=1
                fenzi=0
                for faul_fail_test in fault_fail_tests[0:-1]:
                    if faul_fail_test.strip() in m["fail_test:"]:
                        fenzi+=1
                mutant_fail=m['fail_test:'].split("\n")
                mutant_fail_number=len(mutant_fail)-1
                if mutant_fail_number!=0:
                    Ochiai=fenzi/math.sqrt((len(fault_fail_tests)-1)*mutant_fail_number)
                else:
                    Ochiai=0
                if Ochiai>0.8:
                    if_fault_similarity=True
                    mutant_ochiai+=1
            except Exception as e:
                continue
        if if_fault_similarity:
            fault_similarity_num+=1

    print('fault_similarity_num:',fault_similarity_num,'/',len(faults),'mutant_ochiai>0.8',mutant_ochiai,'/',mutant_number)

mutant_path = 'your own path'
find_fault(mutant_path)
ochiai(mutant_path)  