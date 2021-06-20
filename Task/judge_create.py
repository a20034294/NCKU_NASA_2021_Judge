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
driver = None

with open(env('STUDENT_PATH'), 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        word = line.split(',')
        students[word[0]] = (word[0], word[1], word[2])


def judge_create_task(student_id, password):
    result_data['result'] = {}
    result_data['score'] = 0
    ip = students[student_id][2]

    global driver
    driver = webdriver.Chrome('chromedriver', chrome_options=driver_opt)

    chk_1a(ip)
    chk_2a(ip)
    chk_2c(ip, student_id, password)
    chk_2e(ip)
    chk_2f(ip)
    chk_2g(ip)
    chk_3a(ip)
    try:
        driver.quit()
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


@chk_wrap(20, '2e')
def chk_2e(ip):
    try:
        driver.get('http://' + str(ip) + '/device/1')
        time.sleep(1)
        check_point = driver.find_element_by_xpath(
            '//*[@class="panel-body"]/div[4]/div[2]').get_attribute('innerHTML')

        if re.search('Ubuntu', check_point) is None:
            return False
    except:
        return False

    return True


@chk_wrap(15, '2f')
def chk_2f(ip):
    try:
        driver.get('https://' + str(ip) + '/device/1')
        time.sleep(1)
        check_point = driver.find_element_by_xpath(
            '//*[@class="panel-body"]/div[4]/div[2]').get_attribute('innerHTML')

        if re.search('Ubuntu', check_point) is None:
            return False
    except:
        return False

    return True


@chk_wrap(10, '2g')
def chk_2g(ip):
    ssh = f"ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no ncku-nasa@{ip} -t "
    script = f"{ssh}'sudo du -b /var/log/nginx/librenms.access.log'"
    try:
        result1 = check_output(
            script, stderr=STDOUT, timeout=10, shell=True).decode('utf-8')
        driver.get('http://' + str(ip))
        time.sleep(1)
        result2 = check_output(
            script, stderr=STDOUT, timeout=10, shell=True).decode('utf-8')
        print(result1, result2)
        if result1 != result2:
            return True
    except:
        pass
    return False


@chk_wrap(10, '3a')
def chk_3a(ip):
    ssh = f"ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no ncku-nasa@{ip} -t "
    script = f"{ssh}'sudo dig @127.0.0.1 librenms.finalexam.ncku'"
    try:
        result = check_output(
            script, stderr=STDOUT, timeout=10, shell=True).decode('utf-8')

        if re.search(ip, result) is not None:
            return True
    except:
        pass
    return False
