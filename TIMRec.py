import subprocess as sp
import json
import config
import os
import sys
import time

def replace(f):
    a = os.listdir(f"{sys.path[0]}/amr")
    cmd = ["termux-dialog"]
    cmd.append(config.dialog)
    cmd.append("-t")
    cmd.append("请选择要替换的录音")
    cmd.append("-v")
    s = ""
    for i in a:
        if i[-4:] == ".amr":
            s = s + i + ","
    cmd.append(s)
    popen = sp.Popen(cmd,stdout=sp.PIPE)
    out = popen.communicate()
    j = json.loads(out[0])
    t = j["text"]
    os.system(f"cp {sys.path[0]}/amr/{t} {f}")

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
        print(f"[{time.time()}] : {cmd}")
        popen = sp.Popen(cmd,stdout=sp.PIPE)
        out = popen.communicate()
        j = json.loads(out[0])
        if j["code"] == -1:
            replace(j["text"])
        LOCK = False
        diff = []
    f1 = f2
    time.sleep(1)


