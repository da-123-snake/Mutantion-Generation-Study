import json
from tqdm import tqdm
import glob
import subprocess
import os
import numpy as np
import json
def gptastdiff(way, gumtree_path):
    sum=0
    kk = []
    list_number=[]
    pros = ['Chart','Lang','Time','Mockito','Math','Closure','Cli','Codec','Csv','Gson','JacksonCore','Jsoup']
    pro_nums = [26,65,27,38,106,133,40,18,16,18,26,93]

    for project,nums in zip(pros,pro_nums):
        for i in range(nums):
            mutant_file = '%s/mutant_filter/%s/%s_%s_test.json' % (way, project, project, i+1)
            with open(mutant_file,"r",encoding="utf-8") as f:
                mutant = json.load(f)
            print(mutant_file)
            for m in mutant:
                d4j_fix_path = m['filepath']
                try:
                    lines1 = open(d4j_fix_path, "r",errors='ignore').read().strip()
                    liness = lines1.splitlines()
                    liness[m['line']-1]=m['aftercode']

                    after_mutant_path = 'Deepseek.java'
                    with open(after_mutant_path, "w") as file:
                        file.write('\n'.join(liness))
                    cmd="java -cp %s/target/gumtree-spoon-ast-diff-SNAPSHOT.jar:%s/target/gumtree-spoon-ast-diff-SNAPSHOT-jar-with-dependencies.jar gumtree.spoon.AstComparator %s %s"%(gumtree_path,gumtree_path, d4j_fix_path,after_mutant_path)

                    log=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True)
                    stdout, stderr = log.communicate()
                    #print(log.returncode)
                    if log.returncode != 0:
                        continue
                    output = stdout.decode('utf-8')

                    number = output.count('\n\t')

                    list_number.append({'ast':number, 'line':m['line'],'filepath':d4j_fix_path, 'precode':m['precode'],'aftercode':m['aftercode']})
                except Exception as e:
                    print(d4j_fix_path,"打开失败")
                    continue
    list_number = sorted(list_number,key=lambda x:x['ast'])
    savepath = f'gumAST/{way}.json'
    with open(savepath, 'w', encoding='utf-8') as file1:
        json.dump(list_number, file1, ensure_ascii=False,indent=4)

way = 'Deepseek'
gumtree_path = 'your own path'
gptastdiff(way, gumtree_path)

        