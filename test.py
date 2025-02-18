import subprocess
import json
import os
all = 0
def mutant_test(project,bot,top,way):
    global all
    print(project," start....................................................................")
    sum = 0
    compile_num = 0
    test_pass = 0
    dead = 0
    for i in range(bot,top):
        folder_path = '%s/mutant/%s/%s-%s.json' % (way,project, project, i+1)

        print("****************************",folder_path)
        with open(folder_path, 'r') as f:
            data = json.load(f)
        test = []
        for mutant in data:
            all += 1
            sum += 1
            if sum%200 == 0:
                print("mutant",sum,"testing......")
            dict={}
            filepath=mutant['filepath']
            try:
                oricode=open(filepath,"r",errors='ignore').read()
                lines1 = open(filepath, "r",errors='ignore').read().strip()
                liness = lines1.splitlines()
                if way == 'Major':
                    liness[mutant['line']-1] = liness[mutant['line'] - 1].replace(mutant['precode'], mutant['aftercode'])
                else:
                    liness[mutant['line']-1]=mutant['aftercode']
                with open(filepath, "w") as file:
                    file.write('\n'.join(liness))
            except Exception as e:
                print(filepath,"fail to open")
                open(filepath, "w").write(oricode)
                continue
            cmd = 'defects4j compile -w defects4j_fixed/%s/%s_%s_fixed' % (project,project,i+1)
            try:
                log=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
                if len(log) > 1 and log[1].decode('utf-8') == 'Running ant (compile)...................................................... OK\nRunning ant (compile.tests)................................................ OK\n':
                    compile_num+=1
                    try:
                        test_cmd='timeout 500 defects4j test -w defects4j_fixed/%s/%s_%s_fixed' % (project,project,i+1)
                        log_test=subprocess.Popen(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
                        index = log_test[0].decode('utf-8').index("Failing tests:")
                        number = int(log_test[0].decode('utf-8')[index + len("Failing tests:"):].split()[0])
                        if number == 0:
                            test_pass+=1
                        dict["mutant_id:"] = mutant['id']
                        dict["line"] = mutant["line"]
                        dict["filepath"] = mutant["filepath"]
                        dict["precode"] = mutant["precode"]
                        dict["aftercode"] = mutant["aftercode"]
                        dict["fail_test_number:"] = number
                        dict["fail_test:"] = log_test[0].decode('utf-8')
                        test.append(dict)
                    except Exception as e:
                        dead+=1
                        dict["mutant_id:"] = mutant['id']
                        dict["line"] = mutant["line"]
                        dict["filepath"] = mutant["filepath"]
                        dict["precode"] = mutant["precode"]
                        dict["aftercode"] = mutant["aftercode"]
                        dict["time out"] = True
                        test.append(dict)
                        open(filepath, "w").write(oricode)
                        continue
                open(filepath, "w").write(oricode)
            except Exception as e:
                open(filepath, "w").write(oricode)
                continue
        savepath='%s/mutant_tested/%s/%s_%s_test.json' % (way,project,project,i+1) 
        with open(savepath, 'w', encoding='utf-8') as file1:
            json.dump(test, file1, ensure_ascii=False,indent=4)
    print("sum mutant:",sum)
    print("compile_num:",compile_num)
    print("test_pass:",test_pass)
    print("dead:",dead,"mutant id:",list)

mutant_test("Chart",0,1,'Deepseek')
