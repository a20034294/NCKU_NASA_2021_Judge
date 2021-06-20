import re
from subprocess import STDOUT, check_output
from os import getenv as env
import re
from selenium import webdriver
import time

students = {}
result_data = {}
driver_opt = webdriver.ChromeOptions()
driver_opt.add_argument('--headless')
driver_opt.add_argument('--disable_gpu')
driver_opt.add_argument('--no-sandbox')
driver_opt.add_argument('ignore-certificate-errors')
driver_opt.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36')
driver = webdriver.Chrome('chromedriver', chrome_options=driver_opt)


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
    chk_2c(ip, student_id, password)
    try:
        driver.close()
    except:
        pass
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


@chk_wrap(10, '2c')
def chk_2c(ip, student_id, password):
    try:
        driver.get('http://' + str(ip))
        user_field = driver.find_element_by_xpath('//*[@id="username"]')
        user_field.send_keys(student_id)
        pass_field = driver.find_element_by_xpath('//*[@id="password"]')
        pass_field.send_keys(password)
        driver.find_element_by_xpath('//*[@id="login"]').click()
        time.sleep(1)
        check_point = driver.find_element_by_xpath(
            '//*[@id="navHeaderCollapse"]/ul/li/a/span/small').get_attribute('innerHTML')
        if check_point != student_id:
            return False
    except:
        return False
    return True
