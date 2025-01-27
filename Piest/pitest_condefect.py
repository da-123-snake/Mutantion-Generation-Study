import os
import json
import openai
import os
import glob
from tqdm import tqdm
import subprocess
import json
def get_class():
    mu_list=[]
    id=0
    print("...........................................start generate..............................................................")
    folder_path = 'ConDefects-main/java2024-0306/'
    javapaths = glob.glob(os.path.join(folder_path, '**/correctVersion.java'), recursive=True)

    for javapath in javapaths:
        main_path=javapath.replace("correctVersion.java","Main.java")
        cmd = "mv "+javapath+" "+main_path
        log_test=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
        cmd1="javac "+main_path
        log_test1=subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
        #print(cmd)
# get_class()

def pitest_generat():
    mu_list=[]
    id=0
    print("...........................................start generate..............................................................")
    folder_path = 'ConDefects-main/java2024-0306/'
    classpaths = glob.glob(os.path.join(folder_path, '**/Main.class'), recursive=True)
    for classpath in tqdm(classpaths):
        dir=classpath.replace("Main.class","")
        cmd = "java -cp pitest-1.14.4/pitest/target/pitest-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-command-line/target/pitest-command-line-dev-SNAPSHOT.jar:pitest-1.14.4/pitest-entry/target/pitest-entry-dev-SNAPSHOT.jar:lib/junit-4.13.2.jar:lib/hamcrest-all-1.3.jar:%s org.pitest.mutationtest.commandline.MutationCoverageReport --reportDir %s --targetClasses Main --targetTests MainTest --sourceDirs %s --mutators ALL --verbose true"%(dir,dir+"report/",dir)
        log_test=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, start_new_session=True).communicate()
pitest_generat()


