import re
from subprocess import STDOUT, check_output
from os import getenv as env
import re

students = {}
result_data = {}
with open(env('STUDENT_PATH'), 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        word = line.split(',')
        students[word[0]] = (word[0], word[1], word[2])


def judge_create_task(student_id, password):
    result_data['result'] = {}
    result_data['score'] = 0
    ip = students[student_id][2]

    chk_1a(ip)
    chk_2a(ip)
    return result_data


def chk_wrap(score, problem_id):
    def decorator(f):
        def wrap(*args, **kwargs):
            result_data['result'][problem_id] = 0
            if (f(*args, **kwargs)):
                result_data['result'][problem_id] = score
                result_data['score'] = result_data['score'] + score
        return wrap
    return decorator


@chk_wrap(10, '1a')
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


@chk_wrap(5, '2a')
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
