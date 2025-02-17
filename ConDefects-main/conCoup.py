import subprocess
import os
import math
from tqdm import tqdm
import glob
import json
def get_trigger_tests(filepath, faults,m):
    #fail_tests = []
    for fault in faults:
        fault_path = fault['filepath'].split('/')[-1]
        if fault_path in filepath:
            if '\n' in fault['fail tests:']:
                tests = fault['fail tests:'].split('\n')
                fail_tests = [test.strip() for test in tests if len(test.strip()) > 0]
            else:
                fail_tests = []
            break
    return fail_tests

def Strong(fail_tests, triggers_tests):
    if fail_tests == triggers_tests:
        return True
    return False
    
def Strong_Additional(fail_tests, triggers_tests):
    if len(fail_tests) <= len(triggers_tests):
        return False
    if triggers_tests == fail_tests[:len(triggers_tests)]:
        return True
    return False
    
def Partial(fail_tests, triggers_tests):
    if len(fail_tests) >= len(triggers_tests):
        return False
    if fail_tests == triggers_tests[:len(fail_tests)]:
        return True
    return False

def Partial_Additional(fail_tests, triggers_tests):
    flag1 = False
    flag2 = False
    for test in fail_tests:
        if test in triggers_tests:
            flag1 = True
        else:
            flag2 = True
    if flag1 and flag2:
        return True
    
    return False
    
def No_Subtitution(fail_tests, trigger_tests):
    for test in fail_tests:
        if test in trigger_tests:
            return False
    return True

def judge(project, fail_tests, func):   
    all_trigger_paths = glob.glob('defects4j/framework/projects/%s/trigger_tests/*' % project)
    for trigger_path in all_trigger_paths:
        trigger_tests = get_trigger_tests(trigger_path)
        sorted_failtest = sorted(fail_tests)
        sorted_triggertest = sorted(trigger_tests)
        if func(sorted_failtest, sorted_triggertest):
            return True
    return False

def coup(mutant_path, faults_path):
    strong,partial,strong_additional,partial_additional,no_Subtitution, Not_Detected = 0,0,0,0,0,0
    with open(mutant_path, "r", encoding="utf-8") as f:
        mutants = json.load(f)
    with open(faults_path, "r", encoding="utf-8") as f:
        faults = json.load(f)
    for m in mutants:
        if '\n' in m['fail_test:']:
            tests = m['fail_test:'].split('\n')
            fail_tests = [test.strip() for test in tests if len(test.strip()) > 0]
        else:
            fail_tests = []
        trigger_tests = get_trigger_tests(m['filepath'], faults,m)
        sorted_failtest = sorted(fail_tests)
        sorted_triggertest = sorted(trigger_tests)
        if len(fail_tests) == 0:
            Not_Detected += 1
        elif No_Subtitution(sorted_failtest, sorted_triggertest):
            no_Subtitution += 1
        elif Strong(sorted_failtest, sorted_triggertest):
            strong += 1
        elif Strong_Additional(sorted_failtest, sorted_triggertest):
            strong_additional += 1
        elif Partial(sorted_failtest, sorted_triggertest):
            partial += 1
        elif Partial_Additional(sorted_failtest, sorted_triggertest):
            partial_additional += 1
           
    all_mutant_nums = strong+Not_Detected+no_Subtitution+partial+strong_additional+partial_additional
    print("strong:",strong)
    print("partial:",partial)
    print("strong_additional:",strong_additional)
    print("partial_additional:",partial_additional)
    print("no_Subtitution:",no_Subtitution)
    print("Not_Detected:",Not_Detected)
    print('num:',all_mutant_nums)

mutant_path = 'ConDefects-main/java20240304_mutant/deepseek_java20240304_mutant_new_test.json'
faults_path = 'ConDefects-main/java20240304_faultyVersion_failtest.json'
coup(mutant_path, faults_path)

mutant_path = 'ConDefects-main/java20240406_mutant/deepseek_java20240406_mutant_new_test.json'
faults_path = 'ConDefects-main/java20240406_faultyVersion_failtest.json'
coup(mutant_path, faults_path)