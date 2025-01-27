from bs4 import BeautifulSoup
import json
import os
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
def pi_mutant(htmlpath):
    with open(htmlpath, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')

    mutations_h2 = soup.find('h2', string='Mutations')

    tr_contents = []
    mutations_tr = mutations_h2.find_parent('tr')

    for tr in mutations_tr.find_all_next('tr'):
        tr_contents.append(tr)  

    mutant_p=[]
    for mutant_tr in tr_contents:
        line=mutant_tr.find('a').get_text()

        p_classes = [p['class'] for p in mutant_tr.find_all('p') if 'class' in p.attrs]
        p_s = [p for p in mutant_tr.find_all('p') if 'class' in p.attrs]
        dict={}
        dict['line']=line
        dict['mutant_n']=len(p_classes)
        dict['fail tests']=[]
        killed_n=0
        for p in p_s:
            if p['class'][0]=='KILLED':
                killed_n+=1
                b=p.get_text()
                test=b.split(' ')[5].split('(')[0]
   
                last_dot_index = test.rfind('.')

                kill_test = test[:last_dot_index] + '::' + test[last_dot_index + 1:]
                dict['fail tests'].append(kill_test)
        dict['killed']=killed_n
        mutant_p.append(dict)
    return mutant_p

def mutant_test(project,n,d4j_path):
    all_mutant = []
    total=0
    killed=0
    use_mutant=0
    print("\n")
    print(project," start..........................................................................")
    trigger_tests=[]
    for i in range(n):
        folder_path = '%sframework/projects/%s/trigger_tests/%s' % (d4j_path,project,i+1)
        with open(folder_path, "r", encoding="utf-8") as f:
            data = f.readlines()
        for j in data:
            if "---" in j:
                trigger_tests.append(j.replace('---','').strip())
    for i in range(n):
        GPT_path = 'Gpt/gpt4omini/mutant/%s/%s-%s.json' % (project,project,i+1)
        folder_path = 'Pitest_mutant/%s/%s%s' % (project,project,i+1)
        #print(folder_path)
        all_files=[]
        for root, dirs, files in os.walk(folder_path):
            for file in files:

                if file.endswith('.java.html'):
                    all_files.append(os.path.join(root, file))

        with open(GPT_path, 'r') as f:

            data = json.load(f)
        for mutant in data:
            pi_path=mutant['filepath'].split('/')[-1]+".html"
            mutant_files = [file for file in all_files if file.endswith(pi_path)]
            for mutant_file in mutant_files:
                mutants_p=pi_mutant(mutant_file)
                for mutant_p in mutants_p:
                    if int(mutant['line'])==int(mutant_p['line']):
                        all_mutant.append(mutant_p)
                        break
    return all_mutant

chart=mutant_test('Chart',26,'')
with open('Pitest/Pitest_mutant/chart.json', 'w', encoding='utf-8') as file1:
    json.dump(chart, file1, ensure_ascii=False,indent=4)
lang=mutant_test('Lang',65,'')
with open('Pitest/Pitest_mutant/lang.json', 'w', encoding='utf-8') as file1:
    json.dump(lang, file1, ensure_ascii=False,indent=4)
time=mutant_test('Time',27,'')
with open('Pitest/Pitest_mutant/time.json', 'w', encoding='utf-8') as file1:
    json.dump(time, file1, ensure_ascii=False,indent=4)
mockito=mutant_test('Mockito',38,'')
with open('Pitest/Pitest_mutant/mockito.json', 'w', encoding='utf-8') as file1:
    json.dump(mockito, file1, ensure_ascii=False,indent=4)
math=mutant_test('Math',106,'')
with open('Pitest/Pitest_mutant/math.json', 'w', encoding='utf-8') as file1:
    json.dump(math, file1, ensure_ascii=False,indent=4)
closure=mutant_test('Closure',133,'')
with open('Pitest/Pitest_mutant/closure.json', 'w', encoding='utf-8') as file1:
    json.dump(closure, file1, ensure_ascii=False,indent=4)
cli=mutant_test('Cli',40,'')
with open('Pitest/Pitest_mutant/cli.json', 'w', encoding='utf-8') as file1:
    json.dump(cli, file1, ensure_ascii=False,indent=4)
codec=mutant_test('Codec',18,'')
with open('Pitest/Pitest_mutant/codec.json', 'w', encoding='utf-8') as file1:
    json.dump(codec, file1, ensure_ascii=False,indent=4)
csv=mutant_test('Csv',16,'')
with open('Pitest/Pitest_mutant/csv.json', 'w', encoding='utf-8') as file1:
    json.dump(csv, file1, ensure_ascii=False,indent=4)
gson=mutant_test('Gson',18,'')
with open('Pitest/Pitest_mutant/gson.json', 'w', encoding='utf-8') as file1:
    json.dump(gson, file1, ensure_ascii=False,indent=4)
jacksoncore=mutant_test('JacksonCore',26,'')
with open('Pitest/Pitest_mutant/jacksoncore.json', 'w', encoding='utf-8') as file1:
    json.dump(jacksoncore, file1, ensure_ascii=False,indent=4)
jsoup=mutant_test('Jsoup',93,'')
with open('Pitest/Pitest_mutant/jsoup.json', 'w', encoding='utf-8') as file1:
    json.dump(jsoup, file1, ensure_ascii=False,indent=4)

def sample(sample_num):
    sample_list = []
    summ = 0
    mutant_files = ['chart','lang','time','mockito','math','closure','cli','codec','csv','gson','jacksoncore','jsoup']
    for pro in mutant_files:
        mutant_file = f'Pitest/Pitest_mutant/{pro}.json'
        with open(mutant_file, "r", encoding="utf-8") as f:
            mutants = json.load(f)
        summ += len(mutants)
    for pro in mutant_files:
        mutant_file = f'Pitest/Pitest_mutant/{pro}.json'
        with open(mutant_file, "r", encoding="utf-8") as f:
            mutants = json.load(f)
        m = round(len(mutants) * (sample_num / summ))
        m_list = random.sample(mutants,m)
        sample_list.extend(m_list)
    return(sample_list)

def to_ki_coup(sample_list,d4j_path):
    pros = ['Chart','Lang','Time','Mockito','Math','Closure','Cli','Codec','Csv','Gson','JacksonCore','Jsoup']
    pro_nums = [26,65,27,38,106,133,40,18,16,18,26,93]
    total=0
    killed=0
    coup_mutant=0
    trigger_tests=[]
    for pro,nums in zip(pros,pro_nums):
        for i in range(nums):
            folder_path = '%s/framework/projects/%s/trigger_tests/%s' % (d4j_path,pro,i+1)
            with open(folder_path, "r", encoding="utf-8") as f:
                data = f.readlines()
            for j in data:
                if "---" in j:
                    trigger_tests.append(j.replace('---','').strip())
        
    for mutant in sample_list:
        total+=mutant['mutant_n']
        killed+=mutant['killed']
        for kill in mutant['fail tests']:
            if kill in trigger_tests:
                coup_mutant+=1
                break
    return total,killed,coup_mutant

def get_fault(sample_list,d4j_path):
    kill_tests = []
    find = 0
    for mutant in sample_list:
        kill_tests.extend(mutant['fail tests'])
    pros = ['Chart','Lang','Time','Mockito','Math','Closure','Cli','Codec','Csv','Gson','JacksonCore','Jsoup']
    pro_nums = [26,65,27,38,106,133,40,18,16,18,26,93]
    for pro,nums in zip(pros,pro_nums):
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
    return find

def get_ochiai(sample_list,d4j_path):
    pros = ['Chart','Lang','Time','Mockito','Math','Closure','Cli','Codec','Csv','Gson','JacksonCore','Jsoup']
    pro_nums = [26,65,27,38,106,133,40,18,16,18,26,93]
    fault_similarity_num = 0
    for pro,nums in zip(pros,pro_nums):
        for i in range(nums):
            is_fault_similarity = False
            folder_path = '%s/framework/projects/%s/trigger_tests/%s' % (pro,i+1)
            with open(folder_path, "r", encoding="utf-8") as f:
                data = f.readlines()
            trigger_tests = []
            for j in data:
                if "---" in j:
                    trigger_tests.append(j.replace('---','').strip())
            
            for mutant in sample_list:
                fenzi = 0
                for tri_test in trigger_tests:
                    if tri_test in mutant['fail tests']:
                        fenzi += 1
                mutant_fail_number = len(mutant['fail tests'])
                if mutant_fail_number > 0:
                    Ochiai = fenzi/math.sqrt(len(trigger_tests)*mutant_fail_number)
                else:
                    Ochiai = 0
                if Ochiai > 0.8:
                    is_fault_similarity = True
            if is_fault_similarity:
                fault_similarity_num += 1
    return fault_similarity_num

d4j_path = 'your own path'
total_list=[]
killed_list=[]
coup_list=[]
fault_list=[]
ochiai_list=[]
sum_list = []
for i in tqdm(range(10)):
    sample_list = sample(11946)
    total,kill,coupling = to_ki_coup(sample_list,d4j_path)
    fault = get_fault(sample_list,d4j_path)
    ochiai = get_ochiai(sample_list,d4j_path)
    total_list.append(total)
    killed_list.append(kill)
    coup_list.append(coupling)
    fault_list.append(fault)
    ochiai_list.append(ochiai)
print(np.mean(sum_list))
print(np.mean(total_list))
print(np.mean(killed_list))
print(np.mean(coup_list))
print(np.mean(fault_list))
print(np.mean(ochiai_list))

    