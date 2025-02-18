import subprocess
import json
import os
def get_mutant(project,n,gpt_mutant_path):
    for i in range(n):
        dict_line=[]
        print("..............................................................",project,i+1,"......................................................................")
        folder_path = 'major/log/%s/%s%s' % (project,project,i+1)#
        all_files = os.listdir(folder_path)
        log_files = [folder_path+'/'+file for file in all_files if file.endswith('mutants.log')]
        filter_mutant=gpt_mutant_path+'/%s/%s-%s.json'%(project,project,i+1)
        with open(filter_mutant, 'r') as f:
            data = json.load(f)
        id=0
        for mutant in data:
            mutant_logs = [file for file in log_files if file.endswith(mutant['filepath'].split('/')[-1]+'mutants.log')]
            mutant_log=mutant_logs[0]
            with open(mutant_log, 'r',errors='ignore') as fp:
                mutant_content = fp.readlines()  
            for mutant_line in mutant_content:
                line=mutant_line.split(':')[5]
                try:
                    if int(line)==int(mutant['line']):
                        try:
                            if '<NO-OP>' not in mutant_line:
                                id+=1
                                dict={}
                                _code=mutant_line.split(':'+line+':')[1].strip()
                                pre_code=_code.split('|==>')[0].strip()
                                after_code=_code.split('|==>')[1].strip()
                                dict['id']=id
                                dict['line']=int(line)
                                dict['precode']=pre_code
                                dict['aftercode']=after_code
                                dict['filepath']=mutant['filepath']
                                dict_line.append(dict)
                            else:
                                id+=1
                                dict={}
                                _code=mutant_line.split(':'+line+':')[1].strip()
                                pre_code=_code.split('|==>')[0].strip()
                                dict['id']=id
                                dict['line']=int(line)
                                dict['precode']=pre_code
                                dict['aftercode']=''
                                dict['filepath']=mutant['filepath']
                                dict_line.append(dict)
                        except Exception as e:
                            #print(mutant_line)
                            exit()
                            continue
                except Exception as e:
                    #print(mutant_line)
                    continue
        savepath='major/mutant/%s/%s_%s.json' % (project,project,i+1)
        if not os.path.exists(f'major/mutant/{project}'):
            os.makedirs(f'major/mutant/{project}') 
        with open(savepath, 'w', encoding='utf-8') as file1:
            json.dump(dict_line, file1, ensure_ascii=False,indent=4)

gpt_mutant_path = 'your own path'
get_mutant('Chart',1,gpt_mutant_path)

# projects = ['Chart', 'Closure', 'Lang', 'Math', 'Mockito', 'Time', 'Cli', 'Codec', 'Csv', 'Gson', 'JacksonCore', 'Jsoup']
# pro_ids = [26, 133, 65, 85, 38, 27, 40, 18, 16, 18, 26, 93]
# for project,pro_id in zip(projects,pro_ids):
#     get_mutant(project,pro_id,gpt_mutant_path)