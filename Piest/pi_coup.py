from bs4 import BeautifulSoup
import json
import os
import math
import glob
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
                if kill_test not in dict['fail tests']:
                    dict['fail tests'].append(kill_test)
        dict['killed']=killed_n
        mutant_p.append(dict)
    return mutant_p
fault_similarity_num=0

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
    
def No_Subtitution(fail_tests, project,d4j_path):
    trigger_tests = []
    all_trigger_paths = glob.glob(f'{d4j_path}/framework/projects/{project}/trigger_tests/*')
    for trigger_path in all_trigger_paths:
        trigger_tests.extend(get_trigger_tests(trigger_path))

    for test in fail_tests:
        if test in trigger_tests:
            return False
    return True

def judge(project, fail_tests, func,d4j_path):   
    all_trigger_paths = glob.glob(f'{d4j_path}/framework/projects/{project}/trigger_tests/*')
    for trigger_path in all_trigger_paths:
        trigger_tests = get_trigger_tests(trigger_path)
        sorted_failtest = sorted(fail_tests)
        sorted_triggertest = sorted(trigger_tests)
        if func(sorted_failtest, sorted_triggertest):
            return True
    return False

strong,partial,strong_additional,partial_additional,no_Subtitution, Not_Detected = 0,0,0,0,0,0
def mutant_coup(project,n,d4j_path):
    global strong,partial,strong_additional,partial_additional,no_Subtitution, Not_Detected
    print(project," start..........................................................................\n")

    mutant_all=[]
    for i in range(n):
        GPT_path = 'Gpt/gpt4omini/mutant/%s/%s-%s.json' % (project,project,i+1)
        folder_path = 'pitest/Pitest_mutant/%s/%s%s' % (project,project,i+1)
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
                    try:
                        if int(mutant['line'])==int(mutant_p['line']):
                            
                            fail_tests = mutant_p['fail tests']
                            if len(fail_tests) == 0:
                                Not_Detected += 1
                            elif No_Subtitution(fail_tests, project):
                                no_Subtitution += 1
                            elif judge(project, fail_tests, Strong):
                                strong += 1
                            elif judge(project, fail_tests, Strong_Additional):
                                strong_additional += 1
                            elif judge(project, fail_tests, Partial):
                                partial += 1
                            else:
                                partial_additional += 1
                    except Exception as e:
                        continue

d4j_path = 'your own path'
mutant_coup('Chart',1,d4j_path)

all_mutant_nums = strong+Not_Detected+no_Subtitution+partial+strong_additional+partial_additional
print('num:',all_mutant_nums)
print('Strong:',strong/all_mutant_nums)
print('Strong_Additional:',strong_additional/all_mutant_nums)
print('Partial:',partial/all_mutant_nums)
print('Partial_Additional:',partial_additional/all_mutant_nums)
print('No_Subtitution:',no_Subtitution/all_mutant_nums)
print('Not_Detected:',Not_Detected/all_mutant_nums)
