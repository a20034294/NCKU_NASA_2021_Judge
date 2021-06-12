import re
from subprocess import STDOUT, check_output
from os import getenv as env
import re

students = {}
with open(env('STUDENT_PATH'), 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        word = line.split(',')
        students[word[0]] = (word[0], word[1], word[2])


def chk_1a(ip):
    ssh = f"ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no ncku-nasa@{ip} -t "
    script = f"{ssh}'snmpwalk -v 2c 127.0.0.1 -c \"public\" .1.3.6.1.4.1.2021.4'"
    try:
        result = check_output(
            script, stderr=STDOUT, timeout=10, shell=True).decode('utf-8')
    except:
        result = ''
    if result.find('Counter64') > 0:
        return True
    return False


def chk_2a(ip):
    ssh = f"ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no ncku-nasa@{ip} -t "
    script = f"{ssh}'sudo netstat -tunlp'"
    try:
        result = check_output(
            script, stderr=STDOUT, timeout=10, shell=True).decode('utf-8')
    except:
        result = ''
    print(result)
    if re.search('[^\n]+:80\s.*nginx', result) is not None:
        return True
    return False


def judge_create_task(student_id, password):
    result_data = {}
    result_data['result'] = {}
    ip = students[student_id][2]

    score = 0
    result_data['result']['1a'] = 0
    if chk_1a(ip):
        result_data['result']['1a'] = 10
        score = score + 10

    result_data['result']['2a'] = 0
    if chk_2a(ip):
        result_data['result']['2a'] = 5
        score = score + 5

    result_data['score'] = score
    return result_data
