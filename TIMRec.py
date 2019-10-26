import subprocess as sp
import json
import config
import os
import time

def replace(f):
    source = "/data/data/com.termux/files/home/TIMRec/amr"
    a = os.listdir(source)
    cmd = ["termux-dialog"]
    cmd.append(config.dialog)
    cmd.append("-t")
    cmd.append("请选择要替换的录音")
    cmd.append("-v")
    s = ""
    for i in a:
        s = s + i + ","
    cmd.append(s)
    popen = sp.Popen(cmd,stdout=sp.PIPE)
    out = popen.communicate()
    j = json.loads(out[0])
    t = j["text"]
    os.system(f"cp {source}/{t} {f}")
    #print(f + ">>>" + j["text"])

LOCK = False

os.chdir(config.path)
popen = sp.Popen(["find","-regex",".+stream.+amr"], stdout=sp.PIPE)
out = popen.communicate()
f1 = (str(out[0],encoding = "utf-8").split("\n"))

diff = []
while True:
    popen = sp.Popen(["find","-regex",".+stream.+amr"], stdout=sp.PIPE)
    out = popen.communicate()
    f2 = (str(out[0],encoding = "utf-8").split("\n"))
    for i in f2:
        if i not in f1:
            # 新文件
            diff.append(i)
            LOCK = True
    if LOCK:
        cmd = ["termux-dialog"]
        cmd.append(config.dialog)
        cmd.append("-t")
        cmd.append("请选择要替换的录音")
        cmd.append("-v")
        s = ""
        for i in diff:
            s = s + i + ","
        cmd.append(s)
        print(cmd)
        popen = sp.Popen(cmd,stdout=sp.PIPE)
        out = popen.communicate()
        j = json.loads(out[0])
        replace(j["text"])
        LOCK = False
        diff = []
    f1 = f2
    time.sleep(1)


