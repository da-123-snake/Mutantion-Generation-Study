import subprocess
import random
from tqdm import tqdm
import numpy as np
import math
import json
import os
import glob
import re
from nltk.translate.bleu_score import corpus_bleu

def remove_double_slash_comments(text):
    return re.sub(r'//.*', '', text)

def get_mutant_all_info(project,num,way):
    com_n = 0
    bleu_n = 0
    ast_n = 0
    for i in range(num):
        mutant_list = []
        mutant_path = '%s/mutant/%s/%s-%s.json' % (way,project,project,i+1)
        print("****************************",mutant_path)
        with open(mutant_path, 'r') as f1:

            mutants = json.load(f1)
        com_path = '%s/mutant_tested/%s/%s_%s_test.json' % (way,project,project,i+1)
        with open(com_path, 'r') as f:

            com_mutants = json.load(f)
        for mutant in mutants:
            Is_compilable = False
            dict={}
            dict["id"]=mutant['id']
            dict["line"]=mutant["line"]
            dict["filepath"]=mutant["filepath"]
            dict["precode"]=mutant["precode"]
            dict["aftercode"]=mutant["aftercode"]
            for com in com_mutants:
                if mutant['id'] == com['mutant_id:']:
                    try:
                        com_n+=1
                        dict['compilable'] = True
                        dict['fail_test_number:'] = com['fail_test_number:']
                        dict['fail_test:'] = com['fail_test:']

                        dict['bleu'] = 0.5
                        dict['ast distance'] = 0.5
                        Is_compilable = True
                    except Exception as e:
                        continue
            if Is_compilable == False:
                dict['compilable'] = False
            mutant_list.append(dict)
        print(len(mutant_list),com_n,bleu_n,ast_n)
        savepath='%s/mutant_all_info/%s/%s_%s_test.json' % (way,project,project,i+1) 
        with open(savepath, 'w', encoding='utf-8') as file1:
            json.dump(mutant_list, file1, ensure_ascii=False,indent=4)

def sample(sum,sample_num,filepath):
    sample_list = []
    folder_path = filepath
    mutant_files = glob.glob(os.path.join(folder_path, '**/*.json'), recursive=True)
    for mutant_file in mutant_files:
        with open(mutant_file, "r", encoding="utf-8") as f:
            mutants = json.load(f)
        m = round(len(mutants) * (sample_num / sum))
        m_list = random.sample(mutants,m)
        sample_list.extend(m_list)
    return(sample_list)

def findFault(filter_list, d4j_path):
    kill_tests = []
    bleu_list = []
    ast_distance = []
    for mutant in filter_list:
        try:
            if mutant['fail_test_number:']>0:
                test=mutant['fail_test:'].split('\n')[1:]
                for t in test:
                    if len(t)>0:
                        if t.split(' ')[-1] not in kill_tests:
                            kill_tests.append(t.split(' ')[-1])
        except Exception as e:
            continue
    find = 0
    pros = ['Chart','Lang','Time','Mockito','Math','Closure','Cli','Codec','Csv','Gson','JacksonCore','Jsoup']
    pro_nums = [26,65,27,38,106,133,40,18,16,18,26,93]
    for pro,nums in zip(pros, pro_nums):
        for i in range(nums):
            folder_path = '%s/framework/projects/%s/trigger_tests/%s' % (d4j_path,pro,i+1)
            with open(folder_path, "r", encoding="utf-8") as f:
                data = f.readlines()
            trigger_tests=[]
            for j in data:
                if "---" in j:
                    trigger_tests.append(j.replace('---','').strip())
            for te in trigger_tests:
                if te in kill_tests:
                    find+=1
                    break
    return find,np.mean(bleu_list),np.mean(ast_distance)

def filter(sample_list):
    com = 0
    filter_list = []
    good=0
    notk=0
    for mutant in sample_list:
        try:
            if mutant['compilable']:
                com += 1
                file_path=mutant['filepath']
                with open(file_path, "r", encoding="utf-8") as f:
                    mutantfile = f.readlines()
                if mutant['precode'] in mutantfile[mutant['line']-1] and mutant['precode'] != mutant['aftercode']and mutant['precode'] != "\n":
                    if len(mutant['precode'].strip()) > 0:
                        if mutant['precode'].strip()[0].isalpha():
                            filter_list.append(mutant)
                            good += 1
                            if mutant['fail_test_number:'] == 0:
                                notk += 1
                    else:
                        if len(mutant['aftercode'].strip()) > 0:
                            if mutant['aftercode'].strip()[0] != '/':
                                filter_list.append(mutant)
                                good+=1
                                if mutant['fail_test_number:'] == 0:
                                    notk += 1
                        else:
                            filter_list.append(mutant)
                            good += 1
                            if mutant['fail_test_number:'] == 0:
                                notk += 1
        except Exception as e:
            continue
    score = (good - notk) / good
    return filter_list,com,score

def get_coupling_rate(filter_list,d4j_path):
    trigger_tests = []
    coupling_mutant = 0
    pros = ['Chart','Lang','Time','Mockito','Math','Closure','Cli','Codec','Csv','Gson','JacksonCore','Jsoup']
    pro_nums = [26,65,27,38,106,133,40,18,16,18,26,93]

    for pro,nums in zip(pros,pro_nums):
        for i in range(nums):
            folder_path = '%s/framework/projects/%s/trigger_tests/%s' % (d4j_path, pro, i+1)
            with open(folder_path, "r", encoding="utf-8") as f:
                data = f.readlines()
            for j in data:
                if "---" in j:
                    trigger_tests.append(j.replace('---','').strip())

    for mutant in filter_list:
        for tri_test in trigger_tests:
            if tri_test in mutant["fail_test:"]:
                coupling_mutant += 1
                break
    coupling_rate = coupling_mutant / len(filter_list)
    return coupling_rate

def get_ochiai(filter_list, d4j_path):  
    coupling_mutant = 0
    pros = ['Chart','Lang','Time','Mockito','Math','Closure','Cli','Codec','Csv','Gson','JacksonCore','Jsoup']
    pro_nums = [26,65,27,38,106,133,40,18,16,18,26,93]
    fault_similarity_num = 0
    for pro,nums in zip(pros,pro_nums):
        for i in range(nums):
            is_fault_similarity = False
            folder_path = '%s/framework/projects/%s/trigger_tests/%s' % (d4j_path, pro, i+1)
            with open(folder_path, "r", encoding="utf-8") as f:
                data = f.readlines()
            trigger_tests = []
            for j in data:
                if "---" in j:
                    trigger_tests.append(j.replace('---','').strip())
            
            for mutant in filter_list:
                fenzi = 0
                for tri_test in trigger_tests:
                    if tri_test in mutant['fail_test:']:
                        fenzi += 1
                mutant_fail_number = int(mutant['fail_test_number:'])
                if mutant_fail_number > 0:
                    Ochiai = fenzi/math.sqrt(len(trigger_tests)*mutant_fail_number)
                else:
                    Ochiai = 0
                if Ochiai > 0.8:
                    is_fault_similarity = True
            if is_fault_similarity:
                fault_similarity_num += 1
    return fault_similarity_num

def get_result(way, all_mutant, sample_num, d4j_path):    

    filepath = f'{way}/mutant_all_info'
    sum_list=[]
    com_list=[]
    score_list=[]
    fault_list=[]
    ast_list=[]
    coupling_list=[]
    ochiai_list=[]
    filter_num=[]
    for i in tqdm(range(10)):
        sample_list = sample(all_mutant, sample_num, filepath)
        filter_list, com, score = filter(sample_list)
        find_fault = findFault(filter_list, d4j_path)
        coupling_rate = get_coupling_rate(filter_list, d4j_path)
        ochiai = get_ochiai(filter_list, d4j_path)
        sum_list.append(len(sample_list))
        com_list.append(com)
        filter_num.append(len(filter_list))
        score_list.append(score)
        fault_list.append(find_fault)
        coupling_list.append(coupling_rate)
        ochiai_list.append(ochiai)

    ####################################
    print('com:',np.mean(com_list)/np.mean(sum_list))
    useless = (np.mean(com_list) - np.mean(filter_num)) / np.mean(sum_list)
    print('useless:',useless)
    print('bug det:',np.mean(fault_list) / 605)
    print('coup:',np.mean(coupling_list)) 
    print('ochiai:',np.mean(ochiai_list) / 605)


if __name__ == '__main__':
    way = 'Deepseek'
    d4j_path = 'your own path'
    get_result(way, 33511, 11397, d4j_path)

    # ways = ['Deepseek', 'Codellama', 'Gpt/gpt3.5', 'Gpt/gpt4o', 'Gpt/gpt4omini', 'Leam', 'Major', 'Starchat']
    # numbers = [33511, 26053, 30427, 30739, 33197, 34540, 19841, 26852]
    # for way, number in zip(ways, numbers):
    #     get_result(way, number, 11397, d4j_path)

