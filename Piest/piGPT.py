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

    mutant_p=[]
    for mutant_tr in tr_contents:
        line=mutant_tr.find('a').get_text()

        p_classes = [p['class'] for p in mutant_tr.find_all('p') if 'class' in p.attrs]
        dict={}
        dict['line']=line
        dict['mutant_n']=len(p_classes)
        killed_n=0
        for p_class in p_classes:
            if p_class[0]=='KILLED':
                killed_n+=1
        dict['killed']=killed_n
        mutant_p.append(dict)
    return mutant_p

def compute(project,n,p,gpt_path):
    total=0
    killed=0
    print(project," start.....")
    for i in range(n):
        GPT_path = gpt_path+'/%s/%s_%s_test.json' % (project,project,i+1)
        folder_path = 'Pitest_mutant%s/%s/%s%s' % (p,project,project,i+1)
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
                        total+=mutant_p['mutant_n']
                        killed+=mutant_p['killed']
                        break
    return total,killed

gpt_path = 'your own path'
t,k=compute('Chart',26,'',gpt_path)
print('all:',t,k)


