import subprocess
import json
import os
def generate(project,project_id):
    id=str(project_id+1)
    print("..............................................................",project,id,"......................................................................")
    folder_path = 'defects4j/framework/projects/%s/patches/' % (project)
    all_files = os.listdir(folder_path)
    patch_files = [file for file in all_files if file.endswith('src.patch')]
    dd=0
    log_path='log/%s/%s%s'%(project,project,project_id+1)
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    for patch_file in patch_files:
        dd+=1
        patch_path=os.path.join(folder_path, patch_file)

        print(dd,"****************************",patch_path)
        try:
            with open(patch_path, 'r',errors='ignore') as patch:
                patch_content = patch.readlines()  
        except Exception as e:
            continue
        mutant_path="defects4j_fixed/%s/%s_" % (project,project) +str(project_id+1)+"_fixed/"+patch_content[2][6:].strip()

        savename=patch_path.split('/')[-1].split('.')[0]+'.'+mutant_path.split('/')[-1]
   

        cmd=''
        if project=='Chart':
            spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
            classpath=spath+'/source:'+spath+'/build:'+spath+'/build_tests'
            cmd='javac -cp %s -XMutator=all.mml.bin -d major/class %s'%(classpath,mutant_path)
            #print(cmd)
        if project=='Lang':
            spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
            classpath=spath+'/src:'+spath+'/target/classes:'+spath+'/target/tests'
            cmd='javac -cp %s -XMutator=all.mml.bin -d major/class %s'%(classpath,mutant_path)
            #print(cmd)
        # if project=='Time':#1-11
        #     spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
        #     classpath=spath+'/src:'+spath+'/target/classes:'+spath+'/target/test-classes'
        #     cmd='javac -cp %s -XMutator=all.mml.bin -d major/class %s'%(classpath,mutant_path)
        #     #print(cmd)
        if project=='Time':#11-27
            spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
            classpath=spath+'/src:'+spath+'/build/classes:'+spath+'/build/tests'
            cmd='javac -cp %s -XMutator=all.mml.bin -d major/class %s'%(classpath,mutant_path)
            #print(cmd)

        # if project=='Mockito':#1-11
        #     spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
        #     classpath=spath+'/src:'+spath+'/build/classes/main:'+spath+'/build/classes/test'
        #     lib='%s/compileLib/byte-buddy-0.6.8.jar:defects4j/framework/projects/Mockito/lib/asm-all-5.0.4.jar:defects4j/framework/projects/Mockito/lib/assertj-core-2.1.0.jar:defects4j/framework/projects/Mockito/lib/cglib-and-asm-1.0.jar:defects4j/framework/projects/Mockito/lib/cobertura-2.0.3.jar:defects4j/framework/projects/Mockito/lib/fest-assert-1.3.jar:defects4j/framework/projects/Mockito/lib/fest-util-1.1.4.jar:defects4j/framework/projects/Mockito/lib/hamcrest-all-1.3.jar:defects4j/framework/projects/Mockito/lib/hamcrest-core-1.1.jar:defects4j/framework/projects/Mockito/lib/objenesis-2.1.jar:defects4j/framework/projects/Mockito/lib/objenesis-2.2.jar:defects4j/framework/projects/Mockito/lib/powermock-reflect-1.2.5.jar:'%(spath)
        #     cmd='javac -cp %s%s -XMutator=all.mml.bin -d major/class %s'%(lib,classpath,mutant_path)
        #     #print(cmd)
        if project=='Mockito':#11-38
            spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
            classpath=spath+'/src:'+spath+'/target/classes:'+spath+'/target/test-classes'
            lib='%s/compileLib/byte-buddy-0.6.8.jar:defects4j/framework/projects/Mockito/lib/asm-all-5.0.4.jar:defects4j/framework/projects/Mockito/lib/assertj-core-2.1.0.jar:defects4j/framework/projects/Mockito/lib/cglib-and-asm-1.0.jar:defects4j/framework/projects/Mockito/lib/cobertura-2.0.3.jar:defects4j/framework/projects/Mockito/lib/fest-assert-1.3.jar:defects4j/framework/projects/Mockito/lib/fest-util-1.1.4.jar:defects4j/framework/projects/Mockito/lib/hamcrest-all-1.3.jar:defects4j/framework/projects/Mockito/lib/hamcrest-core-1.1.jar:defects4j/framework/projects/Mockito/lib/objenesis-2.1.jar:defects4j/framework/projects/Mockito/lib/objenesis-2.2.jar:defects4j/framework/projects/Mockito/lib/powermock-reflect-1.2.5.jar:'%(spath)
            cmd='javac -cp %s%s -XMutator=all.mml.bin -d major/class %s'%(lib,classpath,mutant_path)
            # print(cmd)
        if project=='Math':
            spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
            classpath=spath+'/src:'+spath+'/target/classes:'+spath+'/target/test-classes'
            cmd='javac -cp %s -XMutator=all.mml.bin -d major/class %s'%(classpath,mutant_path)
            #print(cmd)
        if project=='Closure':
            spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
            lib='%s/lib/ant-launcher.jar:%s/lib/ant.jar:%s/lib/args4j.jar:%s/lib/caja-r4314.jar:%s/lib/guava.jar:%s/lib/jarjar.jar:%s/lib/json.jar:%s/lib/jsr305.jar:%s/lib/junit.jar:%s/lib/protobuf-java.jar:%s/build/lib/rhino.jar:'%(spath,spath,spath,spath,spath,spath,spath,spath,spath,spath,spath)
            classpath=spath+'/src:'+spath+'/build/classes:'+spath+'/build/test'
            cmd='javac -cp %s%s -XMutator=all.mml.bin -d major/class %s'%(lib,classpath,mutant_path)
            #print(cmd)
        if project == 'Codec':
            spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
            classpath=spath+'/src:'+spath+'/build/classes:'+spath+'/build/test'
            cmd='javac -cp %s -XMutator=all.mml.bin -d major/class %s'%(classpath,mutant_path)
            #print(cmd)
        if project in ['Cli','Csv','Gson','JacksonCore','Jsoup']:
            spath='defects4j_fixed/%s/%s_%s_fixed'%(project,project,project_id+1)
            classpath=spath+'/src:'+spath+'/build/classes:'+spath+'/build/test'
            cmd='javac -cp %s -XMutator=all.mml.bin -d major/class %s'%(classpath,mutant_path)
            #print(cmd)

        try:
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            print('ok')
        except Exception as e:

            continue
        try:
            subprocess.Popen(['mv', 'mutants.log', log_path+'/%smutants.log'%(savename)])
        except Exception as e:

            continue

for i in range(0,1):
    generate('Chart',i)  

# projects = ['Chart', 'Closure', 'Lang', 'Math', 'Mockito', 'Time', 'Cli', 'Codec', 'Csv', 'Gson', 'JacksonCore', 'Jsoup']
# pro_ids = [26, 133, 65, 85, 38, 27, 40, 18, 16, 18, 26, 93]
# for project,project_id in zip(projects,pro_ids):
#     generate(project,project_id)