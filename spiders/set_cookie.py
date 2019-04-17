import json
import os
import time

from selenium import webdriver

# options = webdriver.FirefoxOptions()
# options.add_argument('--headless')  # 无界面模式、无头模式
# options.add_argument('--disable-gpu')  # 禁用GPU加速
# options.add_argument('--user-agent=""')  # 设置请求头
# options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片，提升速度
# options.add_argument('--incognito')  # 无痕模式
# options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
# options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动话程序控制
driver = webdriver.Firefox()
start_url = 'https://www.tianyancha.com/'
driver.get(start_url)
time.sleep(2)
try:
    driver.find_element_by_xpath('//div[@class="nav-item"]/a').click()
except:
    pass

'''60s时间内 手动 写入账号密码，然后等待程序自己关闭。若时间不够可在下面的一行更改'''
time.sleep(60)

try:
    driver.find_element_by_xpath('//div[@class="nav-item -home"]/a')
except:
    pass
else:
    dict_ = {}
    dict_['cookie'] = driver.get_cookies()
    path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.dirname(os.path.realpath(path))

    # num1 = random.randint(1, 10)
    num1 = 1
    file_name1 = r'{dir_path}\cookies\cookie_'.format(**locals()) + str(num1) + '.json'
    with open(file_name1, 'w')as fp:
        fp.write(json.dumps(dict_))
driver.close()
