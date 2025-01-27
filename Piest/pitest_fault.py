from bs4 import BeautifulSoup
import json
import os
def pi_mutant(htmlpath):
    with open(htmlpath, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')


    mutations_h2 = soup.find('h2', string='Mutations')


    tr_contents = []


    mutations_tr = mutations_h2.find_parent('tr')

    for tr in mutations_tr.find_all_next('tr'):
        tr_contents.append(tr)  

    kill_tests=[]
    for mutant_tr in tr_contents:
        line=mutant_tr.find('a').get_text()

        p_classes = [p for p in mutant_tr.find_all('p') if 'class' in p.attrs]
        for p in p_classes:
            if p['class'][0]=='KILLED':
                dict={}
                dict['line']=line
                b=p.get_text()
                test=b.split(' ')[5].split('(')[0]

                last_dot_index = test.rfind('.')

                kill_test = test[:last_dot_index] + '::' + test[last_dot_index + 1:]
                dict['killtest']=kill_test
                kill_tests.append(dict)
    return kill_tests

def find_fault(project,n,d4j_path):
    tri_test_num=0
    tri_test_in=0
    find_fault=0
    pi_kill_test=[]
    print(project," start.....")
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
                kill_tests=pi_mutant(mutant_file)
                for test in kill_tests:
                    if int(mutant['line'])==int(test['line']) and (test['killtest'] not in pi_kill_test):
                        pi_kill_test.append(test['killtest'])


    for i in range(n):
        folder_path1 = '%s/framework/projects/%s/trigger_tests/%s' % (d4j_path,project,i+1)
        with open(folder_path1, "r", encoding="utf-8") as f:
            data = f.readlines()
        trigger_tests=[]
        for j in data:
            if "---" in j:
                tri_test_num+=1
                trigger_tests.append(j.replace('---','').strip())
        

        if_detect_fault=False
        for trigger_test in trigger_tests:
            if trigger_test in pi_kill_test:
                tri_test_in+=1
                if_detect_fault=True
        if if_detect_fault:
            find_fault+=1
    print(p,":")

    print("   find_fault:",find_fault,"/",n)



d4jpath = 'your own path'
find_fault('Chart',1,d4jpath)











