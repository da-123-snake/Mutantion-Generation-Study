import subprocess
import os
import json


def generate_mutant_all(project,project_id):
    id=str(project_id+1)
    print("..............................................................",project,id,"......................................................................")
    folder_path = 'defects4j/framework/projects/%s/patches/' % (project)#遍历patches
    all_files = os.listdir(folder_path)
    patch_files = [file for file in all_files if file.endswith('src.patch')]
    dd=0
    for patch_file in patch_files:
        dd+=1
        patch_path=os.path.join(folder_path, patch_file)
        print(dd,"****************************",patch_path)
        try:
            with open(patch_path, 'r',errors='ignore') as patch:
                patch_content = patch.readlines()  
        except Exception as e:
            continue
        if project=="Chart":
            mutant_class=patch_content[0].split(' ')[-1][9:].replace('/','.')[:-6]
            test_cl=mutant_class.split('.')
            test_class=""
            for i in range(len(test_cl)-1):
                test_class+=test_cl[i]+"."
            test_class+="junit."+test_cl[-1]+"Tests"

            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:defects4j_fixed/%s/%s_%s_fixed/build/:defects4j_fixed/%s/%s_%s_fixed/build-tests/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs defects4j_fixed/%s/%s_%s_fixed/ --mutators ALL --verbose true"%(project,project,id,project,project,id,savepath,mutant_class,test_class,project,project,id)
            #cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:defects4j_fixed/%s/%s_%s_fixed/build/:defects4j_fixed/%s/%s_%s_fixed/build-tests/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests%s --sourceDirs defects4j_fixed/%s/%s_%s_fixed/ --verbose true"%(project,project,id,project,project,id,savepath,mutant_class,trigger_tests,project,project,id)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                if os.path.exists(savepath): 
                    os.rmdir(savepath)
                continue
        # if project=="Lang":#1-20  ,41-65
        #     mutant_class=patch_content[0].split(' ')[-1][16:].replace('/','.')[:-6]
        #     test_class=mutant_class+"Test"

        #     savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
        #     cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:defects4j_fixed/%s/%s_%s_fixed/target/classes/:defects4j_fixed/%s/%s_%s_fixed/target/tests/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs defects4j_fixed/%s/%s_%s_fixed/ --mutators ALL --verbose true"%(project,project,id,project,project,id,savepath,mutant_class,test_class,project,project,id)
        #     #print(cmd)
        #     try:
        #         subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
        #     except Exception as e:
        #         if os.path.exists(savepath): 
        #             os.rmdir(savepath)
        #         continue
        if project=="Lang":#20-41
            mutant_class=patch_content[0].split(' ')[-1][16:].replace('/','.')[:-6]#变异类
            test_class=mutant_class+"Test"

            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:defects4j_fixed/%s/%s_%s_fixed/target/classes/:defects4j_fixed/%s/%s_%s_fixed/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs defects4j_fixed/%s/%s_%s_fixed/ --mutators ALL --verbose true"%(project,project,id,project,project,id,savepath,mutant_class,test_class,project,project,id)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                if os.path.exists(savepath): 
                    os.rmdir(savepath)
                continue 
        # if project=="Time":#1到11
        #     mutant_class=patch_content[0].split(' ')[-1][16:].replace('/','.')[:-6]
        #     class_name=mutant_class.split('.')[-1]
        #     te_class=mutant_class.replace(class_name,'Test'+class_name)
        #     test_class=te_class+','+te_class+'_Basics,'+te_class+'_Match,'+te_class+'_Properties,'+te_class+'_Constructors,'+te_class+'_Sets,'+te_class+'_Updates,'+te_class+'_Adds'
        #     path="defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
        #     savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
        #     cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s/target/classes/:%s/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src --mutators ALL --verbose true"%(path,path,savepath,mutant_class,test_class,path)
        #     #print(cmd)
        #     try:
        #         subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
        #     except Exception as e:
        #         if os.path.exists(savepath): 
        #             os.rmdir(savepath)
        #         continue
        if project=="Time":#12到27
            mutant_class=patch_content[0].split(' ')[-1][16:].replace('/','.')[:-6]
            class_name=mutant_class.split('.')[-1]
            te_class=mutant_class.replace(class_name,'Test'+class_name)
            test_class=te_class+','+te_class+'_Basics,'+te_class+'_Match,'+te_class+'_Properties,'+te_class+'_Constructors,'+te_class+'_Sets,'+te_class+'_Updates,'+te_class+'_Adds'
            path="defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s/build/classes/:%s/build/tests/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src --mutators ALL --verbose true"%(path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                if os.path.exists(savepath): 
                    os.rmdir(savepath)
                continue
        if project=="Math":
            mutant_class=patch_content[0].split(' ')[-1][16:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:defects4j_fixed/%s/%s_%s_fixed/target/classes/:defects4j_fixed/%s/%s_%s_fixed/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs defects4j_fixed/%s/%s_%s_fixed/ --mutators ALL --verbose true"%(project,project,id,project,project,id,savepath,mutant_class,test_class,project,project,id)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                if os.path.exists(savepath): 
                    os.rmdir(savepath)
                continue
        # if project=="Mockito":#1到11
        #     mutant_class=patch_content[0].split(' ')[-1][6:].replace('/','.')[:-6]
        #     test_class=mutant_class+"Test"
        #     path="defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
        #     savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
        #     cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:%s/compileLib/byte-buddy-0.6.8.jar:defects4j/framework/projects/Mockito/lib/asm-all-5.0.4.jar:defects4j/framework/projects/Mockito/lib/assertj-core-2.1.0.jar:defects4j/framework/projects/Mockito/lib/cglib-and-asm-1.0.jar:defects4j/framework/projects/Mockito/lib/cobertura-2.0.3.jar:defects4j/framework/projects/Mockito/lib/fest-assert-1.3.jar:defects4j/framework/projects/Mockito/lib/fest-util-1.1.4.jar:defects4j/framework/projects/Mockito/lib/hamcrest-all-1.3.jar:defects4j/framework/projects/Mockito/lib/hamcrest-core-1.1.jar:defects4j/framework/projects/Mockito/lib/objenesis-2.1.jar:defects4j/framework/projects/Mockito/lib/objenesis-2.2.jar:defects4j/framework/projects/Mockito/lib/powermock-reflect-1.2.5.jar:%s/build/classes/main/:%s/build/classes/test/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src/ --mutators ALL --verbose true"%(path,path,path,savepath,mutant_class,test_class,path)
        #     #print(cmd)
        #     try:
        #         subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
        #     except Exception as e:
        #         if os.path.exists(savepath): 
        #             os.rmdir(savepath)
        #         continue

        if project=="Mockito":#12到38
            mutant_class=patch_content[0].split(' ')[-1][6:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            path="defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:%s/compileLib/byte-buddy-0.6.8.jar:defects4j/framework/projects/Mockito/lib/asm-all-5.0.4.jar:defects4j/framework/projects/Mockito/lib/assertj-core-2.1.0.jar:defects4j/framework/projects/Mockito/lib/cglib-and-asm-1.0.jar:defects4j/framework/projects/Mockito/lib/cobertura-2.0.3.jar:defects4j/framework/projects/Mockito/lib/fest-assert-1.3.jar:defects4j/framework/projects/Mockito/lib/fest-util-1.1.4.jar:defects4j/framework/projects/Mockito/lib/hamcrest-all-1.3.jar:defects4j/framework/projects/Mockito/lib/hamcrest-core-1.1.jar:defects4j/framework/projects/Mockito/lib/objenesis-2.1.jar:defects4j/framework/projects/Mockito/lib/objenesis-2.2.jar:defects4j/framework/projects/Mockito/lib/powermock-reflect-1.2.5.jar:%s/target/classes/:%s/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src/ --mutators ALL --verbose true"%(path,path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                if os.path.exists(savepath): 
                    os.rmdir(savepath)
                continue
        if project=="Closure":
            mutant_class=patch_content[0].split(' ')[-1][6:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            path="/data/cmd/LLM_mutant/defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            cmd="java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s/lib/junit.jar:%s/lib/libtrunk_rhino_parser_jarjared.jar:%s/lib/protobuf_deploy.jar:%s/lib/google_common_deploy.jar:%s/lib/ant-launcher.jar:%s/lib/ant.jar:%s/lib/args4j.jar:%s/lib/caja-r4314.jar:%s/lib/guava.jar:%s/lib/jarjar.jar:%s/lib/json.jar:%s/lib/jsr305.jar:%s/lib/junit.jar:%s/lib/protobuf-java.jar:%s/build/lib/rhino.jar:%s/build/classes/:%s/build/test/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/ --mutators ALL --verbose true"%(path,path,path,path,path,path,path,path,path,path,path,path,path,path,path,path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                continue
        if project == "Codec":
            mutant_class=patch_content[0].split(' ')[-1][11:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            path="/data/cmd/LLM_mutant/defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            cmd = "java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s/target/classes/:/%s/target/tests/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src --mutators ALL --verbose true"%(path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                continue
        if project == "Csv":
            mutant_class=patch_content[0].split(' ')[-1][16:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            path="/data/cmd/LLM_mutant/defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            cmd = "java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s/target/classes/:%s/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src --mutators ALL --verbose true"%(path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                continue
        if project == "Gson":
            mutant_class=patch_content[0].split(' ')[-1][21:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            path="/data/cmd/LLM_mutant/defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            cmd = "java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s/target/classes/:%s/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src --mutators ALL --verbose true"%(path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                continue
        if project == "Gson":
            mutant_class=patch_content[0].split(' ')[-1][21:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            path="/data/cmd/LLM_mutant/defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            cmd = "java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s/target/classes/:%s/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src --mutators ALL --verbose true"%(path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                continue
        if project == "Jsoup":
            mutant_class=patch_content[0].split(' ')[-1][16:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            path="/data/cmd/LLM_mutant/defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            cmd = "java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:defects4j/framework/projects/Jsoup/lib/com/google/code/gson/gson/2.7/gson-2.7.jar:defects4j/framework/projects/Jsoup/lib/commons-lang/commons-lang/2.4/commons-lang-2.4.jar:defects4j/framework/projects/Jsoup/lib/javax/servlet/javax.servlet-api/3.1.0/javax.servlet-api-3.1.0.jar:defects4j/framework/projects/Jsoup/lib/org/eclipse/jetty/jetty-http/9.2.26.v20180806/jetty-http-9.2.26.v20180806.jar:defects4j/framework/projects/Jsoup/lib/org/eclipse/jetty/jetty-io/9.2.26.v20180806/jetty-io-9.2.26.v20180806.jar:defects4j/framework/projects/Jsoup/lib/org/eclipse/jetty/jetty-security/9.2.26.v20180806/jetty-security-9.2.26.v20180806.jar:defects4j/framework/projects/Jsoup/lib/org/eclipse/jetty/jetty-server/9.2.26.v20180806/jetty-server-9.2.26.v20180806.jar:defects4j/framework/projects/Jsoup/lib/org/eclipse/jetty/jetty-servlet/9.2.26.v20180806/jetty-servlet-9.2.26.v20180806.jar:defects4j/framework/projects/Jsoup/lib/org/eclipse/jetty/jetty-util/9.2.26.v20180806/jetty-util-9.2.26.v20180806.jar:%s/target/classes/:%s/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src --mutators ALL --verbose true"%(path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                continue
        #########################################################################
        if project == "Cli":
            mutant_class=patch_content[0].split(' ')[-1][16:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            path="/data/cmd/LLM_mutant/defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            cmd = "java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s/target/classes/:%s/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src --mutators ALL --verbose true"%(path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                continue
        if project == "JacksonCore":
            mutant_class=patch_content[0].split(' ')[-1][16:].replace('/','.')[:-6]
            test_class=mutant_class+"Test"
            savepath="pitest/Pitest_mutant/"+project+"/"+project+id+"/"+patch_path.split('/')[-1]
            path="/data/cmd/LLM_mutant/defects4j_fixed/%s/%s_%s_fixed"%(project,project,id)
            cmd = "java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s/target/classes/:%s/target/test-classes/ org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses %s --targetTests %s --sourceDirs %s/src --mutators ALL --verbose true"%(path,path,savepath,mutant_class,test_class,path)
            #print(cmd)
            try:
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
            except Exception as e:
                continue

for i in range(0,1):
    generate_mutant_all("Chart",i)
