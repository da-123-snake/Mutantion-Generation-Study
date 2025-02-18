import subprocess
import os
import math
from tqdm import tqdm
import glob
import json

def get_trigger_tests(folder_path):
    with open(folder_path, "r", encoding="utf-8") as f:
        data = f.readlines()
    trigger_tests = []
    for j in data:
        if "---" in j:
            trigger_tests.append(j.replace('---','').strip())
    return trigger_tests

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
    
def No_Subtitution(fail_tests, project, d4j_path):
    trigger_tests = []
    all_trigger_paths = glob.glob(f'{d4j_path}/framework/projects/{project}/trigger_tests/*')
    for trigger_path in all_trigger_paths:
        trigger_tests.extend(get_trigger_tests(trigger_path))

    for test in fail_tests:
        if test in trigger_tests:
            return False
    return True

def judge(project, fail_tests, func, d4j_path):   
    all_trigger_paths = glob.glob(f'{d4j_path}/framework/projects/{project}/trigger_tests/*')
    for trigger_path in all_trigger_paths:
        trigger_tests = get_trigger_tests(trigger_path)
        sorted_failtest = sorted(fail_tests)
        sorted_triggertest = sorted(trigger_tests)
        if func(sorted_failtest, sorted_triggertest):
            return True
    return False

def coup(way, d4j_path):
    print(way)
    strong,partial,strong_additional,partial_additional,no_Subtitution, Not_Detected = 0,0,0,0,0,0
    all_mutant_file_path = glob.glob(f'{way}/mutant_filter/*/*.json')
    for mutant_path in tqdm(all_mutant_file_path):
        pro = mutant_path.split('/')[-1].split('_')[0]
        pro_id = mutant_path.split('/')[-1].split('_')[1]
        with open(mutant_path, "r", encoding="utf-8") as f:
            mutants = json.load(f)
        
        for mutant in mutants:
            fail_tests = []
            try:
                test=mutant['fail_test:'].split('\n')[1:]
            except Exception as e:
                continue
            for t in test:
                if len(t)>0:
                    fail_tests.append(t.split(' ')[-1])

            if mutant['fail_test_number:'] == 0:
                Not_Detected += 1
            elif No_Subtitution(fail_tests, pro, d4j_path):
                no_Subtitution += 1
            elif judge(pro, fail_tests, Strong, d4j_path):
                strong += 1
            elif judge(pro, fail_tests, Strong_Additional, d4j_path):
                strong_additional += 1
            elif judge(pro, fail_tests, Partial, d4j_path):
                partial += 1
            else:
                partial_additional += 1

    all_mutant_nums = strong+Not_Detected+no_Subtitution+partial+strong_additional+partial_additional
    
    print('Strong:',strong)
    print('Strong_Additional:',strong_additional)
    print('Partial:',partial)
    print('Partial_Additional:',partial_additional)
    print('No_Subtitution:',no_Subtitution)
    print('Not_Detected:',Not_Detected)   
    print('num:',all_mutant_nums)   

if __name__ == '__main__':
    way = 'Deepseek'
    d4j_path = 'your own path' 
    coup(way, d4j_path)
    
    # ways = ['Deepseek', 'Codellama', 'Gpt/gpt3.5', 'Gpt/gpt4o', 'Gpt/gpt4omini', 'Leam', 'Major', 'Starchat']
    # for way in ways:
    #     coup(way, d4j_path)