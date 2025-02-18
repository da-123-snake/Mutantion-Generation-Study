import subprocess
import os
import math
from tqdm import tqdm
import json
def filter(project,num,way):
    print("--------------------",project,"----------------------")
    filter_num = 0
    not_killed = 0
    com = 0
    for i in range(num):
        filter_test = []
        folder_path = '%s/mutant_tested/%s/%s_%s_test.json' % (way,project,project,i+1)#遍历
        with open(folder_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for mutant in data:
            com += 1
            try:
                file_path = mutant['filepath']
                with open(file_path, "r", encoding="utf-8") as f:
                    mutantfile = f.readlines()
                if mutant['precode'] in mutantfile[mutant['line']-1] and mutant['precode'] != mutant['aftercode'] and mutant['precode'] != "\n":
                    if len(mutant['precode'].strip()) > 0:
                        if mutant['precode'].strip()[0].isalpha():
                            filter_test.append(mutant)
                            filter_num += 1
                            if mutant['fail_test_number:'] == 0:
                                not_killed += 1
                    else:
                        if len(mutant['aftercode'].strip()) > 0:
                            if mutant['aftercode'].strip()[0] != '/':
                                filter_test.append(mutant)
                                filter_num += 1
                                if mutant['fail_test_number:'] == 0:
                                    not_killed += 1
                        else:
                            filter_test.append(mutant)
                            filter_num += 1
                            if mutant['fail_test_number:'] == 0:
                                not_killed += 1
            except Exception as e:
                continue
        savepath='%s/mutant_filter/%s/%s_%s_test.json' % (way,project,project,i+1) 
        with open(savepath, 'w', encoding='utf-8') as file1:
            json.dump(filter_test, file1, ensure_ascii=False,indent=4)
    print("com:",com)
    print("all:",filter_num,"    killed",filter_num-not_killed,"      score:",(filter_num-not_killed) / filter_num)

def find_fault(project,num,way,d4j_path):
    print("--------------------",project,"----------------------")
    kill_tests=[]
    for i in range(num):
        mutant_path = '%s/mutant_filter/%s/%s_%s_test.json' % (way, project, project, i+1)
        with open(mutant_path, "r", encoding="utf-8") as f:
            mutant = json.load(f)
        for m in mutant:
            try:
                if m['fail_test_number:'] > 0:
                    test = m['fail_test:'].split('\n')[1:]
                    for t in test:
                        if len(t) > 0:
                            if t.split(' ')[-1] not in kill_tests:
                                kill_tests.append(t.split(' ')[-1])
            except Exception as e:
                continue
    find = 0
    for i in range(num):
        folder_path = '%s/framework/projects/%s/trigger_tests/%s' % (d4j_path, project, i+1)
        with open(folder_path, "r", encoding = "utf-8") as f:
            data = f.readlines()
        trigger_tests = []
        for j in data:
            if "---" in j:
                trigger_tests.append(j.replace('---','').strip())
        for te in trigger_tests:
            if te in kill_tests:
                find += 1
                break
    print(project, 'find fault:',find,'   all:',num)

def ochiai(project, num, way, d4j_path):
    print("--------------------",project,"----------------------")
    fault_similarity_num = 0
    mutant_number = 0
    mutant_ochiai = 0
    mutant_all = []
    for j in range(num):
        mutant_path = '%s/mutant_filter/%s/%s_%s_test.json' % (way, project, project, j+1)
        with open(mutant_path, "r", encoding="utf-8") as f:
            mutant = json.load(f)
        for m in mutant:
            mutant_number+=1
            mutant_all.append(m)

    for i in range(num):
        if_fault_similarity=False
        folder_path = '%s/framework/projects/%s/trigger_tests/%s' % (way, project, i+1)
        with open(folder_path, "r", encoding="utf-8") as f:
            data = f.readlines()
        trigger_tests = []
        for j in data:
            if "---" in j:
                trigger_tests.append(j.replace('---','').strip())

        for m in mutant_all:
            try:
                mutant_numbe += 1
                fenzi = 0
                for tri_test in trigger_tests:
                    if tri_test in m['fail_test:']:
                        fenzi += 1
                mutant_fail_number = int(m['fail_test_number:'])
                if mutant_fail_number > 0:
                    Ochiai = fenzi/math.sqrt(len(trigger_tests)*mutant_fail_number)
                else:
                    Ochiai = 0
                if Ochiai > 0.8:
                    if_fault_similarity = True
                    mutant_ochiai += 1
            except Exception as e:
                continue
        if if_fault_similarity:
            fault_similarity_num += 1
    
    print('fault_similarity_num:',fault_similarity_num,'/',num,'mutant_ochiai>0.8',mutant_ochiai,'/',mutant_number)

if __name__ == "__main__":
    way = 'Deepseek'
    d4j_path = 'your own path'
    filter('Chart', 26, way, d4j_path)
    find_fault('Chart', 26, way, d4j_path)
    ochiai('Chart', 26, way, d4j_path)

    # ways = ['Deepseek', 'Codellama', 'Gpt/gpt3.5', 'Gpt/gpt4o', 'Gpt/gpt4omini', 'Leam', 'Major', 'mBert', 'Starchat']
    # projects = ['Chart', 'Closure', 'Lang', 'Math', 'Mockito', 'Time', 'Cli', 'Codec', 'Csv', 'Gson', 'JacksonCore', 'Jsoup']
    # pro_ids = [26, 133, 65, 85, 38, 27, 40, 18, 16, 18, 26, 93]
    # for way in ways:
    #     for project, pro_id in zip(projects, pro_ids):
    #         filter(project, pro_id, way, d4j_path)
    #         find_fault(project, pro_id, way, d4j_path)
    #         ochiai(project, pro_id, way, d4j_path)