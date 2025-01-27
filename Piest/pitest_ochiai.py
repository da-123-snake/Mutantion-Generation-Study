from bs4 import BeautifulSoup
import json
import os
import math
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

def ochiai(project,n,d4j_path):

    print("\n")
    print(project," start..........................................................................")

    mutant_all=[]
    for i in range(n):
        GPT_path = 'Gpt/gpt4omini/mutant/%s/%s-%s.json' % (project,project,i+1)
        folder_path = 'Pitest_mutant/%s/%s%s' % (project,project,i+1)
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
                        mutant_all.append(mutant_p)
    fault_similarity_num=0#ochiai>0.8
    fault_similarity_num7=0#ochiai>0.7
    mutant_ochiai=0#ochiai>0.8
    mutant_ochiai7=0#ochiai>0.7
    mutant_number=0
    for i in range(n):
        if_fault_similarity=False
        if_fault_similarity7=False
        trigger_tests=[]
        folder_path = '%s/framework/projects/%s/trigger_tests/%s' % (d4j_path,project,i+1)
        with open(folder_path, "r", encoding="utf-8") as f:
            data = f.readlines()
        for j in data:
            if "---" in j:
                trigger_tests.append(j.replace('---','').strip())

        for m in mutant_all:
            mutant_number+=int(m['mutant_n'])
            fenzi=0
            for tri_test in trigger_tests:
                if tri_test in m['fail tests']:
                    fenzi+=1
            mutant_fail_number=len(m['fail tests'])
            if mutant_fail_number!=0:
                Ochiai=fenzi/math.sqrt(len(trigger_tests)*mutant_fail_number)
            else:
                Ochiai=0
            if Ochiai>0.8:
                if_fault_similarity=True
                mutant_ochiai+=int(m['mutant_n'])
            if Ochiai>0.7:
                if_fault_similarity7=True
                mutant_ochiai7+=int(m['mutant_n'])
        if if_fault_similarity:
            fault_similarity_num+=1
        if if_fault_similarity7:
            fault_similarity_num7+=1
    print("ochiai>0.8:",fault_similarity_num,'/',n,"    ",mutant_ochiai,'/',mutant_number)
    print("ochiai>0.7:",fault_similarity_num7,'/',n,"    ",mutant_ochiai7,'/',mutant_number)

d4jpath = 'your own path'
ochiai('Chart',26,'',d4jpath)
