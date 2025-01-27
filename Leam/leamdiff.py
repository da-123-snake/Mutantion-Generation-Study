import json
import subprocess
from tqdm import tqdm
def git_diff(file1_path, file2_path):
    command = ["git", "diff", "--no-index", "--color-words", file1_path, file2_path]
    diff_output = subprocess.run(command, capture_output=True, text=True)
    return diff_output.stdout

def diff(project,bot,top):
    add = 0
    for ii in range(bot,top):
        my_mutants=[]
        mutant_path = 'Leam/LEAM-main/mutants/%s-%s.json'% (project,ii+1)
        print(mutant_path)
        with open(mutant_path,'r') as f:
            mutants = json.load(f)
        for mutant in tqdm(mutants):  
            with open('Leam/tem.java','w') as f2:
                f2.write(mutant['aftercode'])

            file1_path = mutant['filepath'].replace('/mnt/disk1/cmd/defects4j_fixed','defects4j_fixed')
            if project == 'Lang' and ii +1 >39:
                file1_path = file1_path.replace('_fixedd/','_fixed/')
            file2_path = "Leam/tem.java"
            differences = git_diff(file1_path, file2_path)
            diff_number = differences.count("@@")
            try:
                pre_code = open(file1_path, "r",errors='ignore').read().strip().splitlines()
            except Exception as e:
                continue
            after_code = open(file2_path, "r",errors='ignore').read().strip().splitlines()
            for i in range(1,diff_number,2):
                diff = differences.split('@@')[i].strip()
                mutant_line = int(diff.split(' ')[0].split(',')[0].replace('-',''))
                pre_number = int(diff.split(' ')[0].split(',')[1])
                after_nummber = int(diff.split(' ')[1].split(',')[1])
                for j in range(mutant_line,mutant_line+max(pre_number,after_nummber)):
                    #print(j,mutant['precode'].strip(),pre_code[j - 1])
                    if j > len(pre_code):
                        break
                    if mutant['precode'].strip() == pre_code[j - 1].strip():
                        if pre_number > after_nummber:
                            mutant['aftercode'] = ''
                            mutant['line'] = j
                            my_mutants.append(mutant)
                        elif pre_number == after_nummber:
                            mutant['aftercode'] = after_code[j-1]
                            mutant['line'] = j
                            my_mutants.append(mutant)
                        else:
                            add+=1
                            #print(differences)
                        #my_mutants.append(mutant)
                        break
                break
        savepath='Leam/mutant/%s_%s_test.json' % (project,ii+1) 
        #savepath = '/root/autodl-tmp/Leam/mutant/%s-%s.json'% (project,ii+1) 
        with open(savepath, 'w', encoding='utf-8') as file1:
            json.dump(my_mutants, file1, ensure_ascii=False,indent=4)
    print(add)


diff("Chart",0,1)
