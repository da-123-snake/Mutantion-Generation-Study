import os
import json
import os
import time
import json
def generate_mutant(project,project_id):
    id=0
    dd=0
    loc=''
    print("..............................................................",project,project_id+1,"......................................................................")
    folder_path = 'defects4j/framework/projects/%s/patches/' % (project)
    all_files = os.listdir(folder_path)
    patch_files = [file for file in all_files if file.endswith('src.patch')]
    for patch_file in patch_files:
        if int(patch_file.split('.')[0])>133:
            continue
        dd+=1
        patch_path=os.path.join(folder_path, patch_file)
        print(dd,"****************************",patch_path)
        try:
            with open(patch_path, 'r',errors='ignore') as patch:
                patch_content = patch.readlines()  
        except Exception as e:
            continue
        fixed_bug = ''
        if project == 'Chart':
            path=patch_content[2][13:]
            path=path.strip()
            fixed_bug=path.split('.')[0]
            fixed_bug=fixed_bug.replace('/','.')
        if project == 'Lang' or project == 'Math' or project == 'Time':
            path=patch_content[2][20:]
            path=path.strip()
            fixed_bug=path.split('.')[0]
            fixed_bug=fixed_bug.replace('/','.')
        if project == 'Mockito' or project == 'Closure':
            path=patch_content[2][10:]
            path=path.strip()
            fixed_bug=path.split('.')[0]
            fixed_bug=fixed_bug.replace('/','.')
        patch_lines=[]
        # java_classes=[]
        for i in patch_content:
            if "@@" in i:
                patch_lines.append(i)
        for patch_line in patch_lines:
            split_result = patch_line.split(" ")[2]  
            start_line, mutant_lines = map(int, split_result.split(','))
            for ii in range(mutant_lines):
                line=start_line+ii
                loc=loc+fixed_bug+'#'+str(line)+'      1\n'
    savepath='location2/%s/%s/parsed_ochiai_result'%(project,project_id+1)
    os.mkdir(savepath.replace("/parsed_ochiai_result",""))
    with open(savepath, 'w', encoding='utf-8') as file:
        file.write(loc)
for i in range(0,26):
    generate_mutant('Chart',i)
for i in range(0,65):
    generate_mutant('Lang',i)
for i in range(0,106):
    generate_mutant('Math',i)
for i in range(0,38):
    generate_mutant('Mockito',i)
for i in range(0,27):
    generate_mutant('Time',i)
for i in range(0,133):
    generate_mutant('Closure',i)
for i in range(0,40):
    generate_mutant('Cli',i)
for i in range(0,18):
    generate_mutant('Codec',i)
for i in range(0,16):
    generate_mutant('Csv',i)
for i in range(0,18):
    generate_mutant('Gson',i)
for i in range(0,26):
    generate_mutant('JacksonCore',i)
for i in range(0,93):
    generate_mutant('Jsoup',i)