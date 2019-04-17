
'''
        注册模块信息
        register_crawl()

        # 股东信息
        partner_crawl()

        # 对外投资
        invest_crawl()

        # 法律诉讼
        law_crawl()
'''

import os
import traceback
from datetime import datetime
import json
import logging
import random
import re
import time
from lxml import etree
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class XpathErr(Exception):
    def __init__(self, err='xpath 获取失败'):
        Exception.__init__(self, err)
class CookieErr(Exception):
    def __init__(self, err='cookie获取失败。请重新执行set_cookie.py文件获取cookie'):
        Exception.__init__(self, err)

class Driver_xpathErr(Exception):
    def __init__(self, err='driver_xpath 找不到，路径出错'):
        Exception.__init__(self, err)


class ErrLog(object):
    def __init__(self, url, errtype, com_name, err_msg):
        with open('{dir_path}'.format(**globals()) + r'\log\fail\{}.txt'.format(str(datetime.now().strftime('%Y%m%d'))),
                  'a+', encoding='utf-8') as f:
            f.write(
                "{}<f>{}<f>{}<f>{}<f>{}<f>{}\n".format(str(datetime.now().strftime('%Y%m%d%H%M%S')), com_name, err_msg,
                                                       errtype, url,
                                                       ''.join(
                                                           traceback.format_exc().splitlines())))
            f.close()


# 文本处理
def delete_htmltag(html, start_tag, end_tag):
    html = str(html).replace('\n', '').replace('\r', '')
    results = re.findall("%s(.*?)%s" % (start_tag, end_tag), html)
    for result in results:
        html = html.replace(result, '')

    # 去除链接
    all_url = re.findall(r'href="(.*?)"', html)
    # all_src = re.findall(r'src="(.*?)"', html)
    # for url in all_url:
    #     html = html.replace('href="{}"'.format(url), 'href="{}"'.format('javascript:void(0)'))
    # for src in all_src:
    #     html_string = html.replace('src="{}"'.format(src), 'src="{}"'.format('#'))

    return html


def process_delete_htmltag(str_content_html, rubbish_start_tag, rubbish_end_tag):
    start_tag = rubbish_start_tag
    end_tag = rubbish_end_tag
    if isinstance(start_tag, list) and isinstance(end_tag, list):
        if len(start_tag) == len(end_tag):
            for i in range(len(start_tag)):
                str_content_html = delete_htmltag(html=str_content_html,
                                                  start_tag=start_tag[i],
                                                  end_tag=end_tag[i])
        return str_content_html
    elif not isinstance(start_tag, list) and not isinstance(end_tag, list):
        str_content_html = delete_htmltag(html=str_content_html,
                                          start_tag=start_tag,
                                          end_tag=end_tag)
        return str_content_html
    else:
        raise SyntaxError


# 随机时间
def tm1():
    times1 = [0.6, 0.8, 0.9, 1, 1.2, 1.3]
    index = random.randint(0, len(times1) - 1)
    return times1[index]


def tm2():
    times2 = [1.7, 1.9, 2, 2.2, 2.3]
    index = random.randint(0, len(times2) - 1)
    return times2[index]


def tm3():
    times3 = [2, 2.5, 2.8, 3, 3.3, 3.5]
    index = random.randint(0, len(times3) - 1)
    return times3[index]


# 随机模拟执行/防识别

def time_event(driver):
    random_num1 = random.randint(1, 5)
    if random_num1 == 1:
        time.sleep(tm1())
        ActionChains(driver).key_down(Keys.PAGE_UP).perform()
        time.sleep(tm2())
    elif random_num1 == 2:
        time.sleep(tm1())
        loop_num = random.randint(1, 3)
        for i in range(loop_num):
            ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
            time.sleep(tm1())
        time.sleep(tm1())
    elif random_num1 == 3:
        time.sleep(tm1())
        ActionChains(driver).key_down(Keys.PAGE_UP).perform()
        time.sleep(tm1())
        ActionChains(driver).key_down(Keys.PAGE_UP).perform()
        time.sleep(tm1())
    else:
        time.sleep(tm2())


# 验证码处理
def code():
    driver1 = webdriver.Firefox()
    # driver1 = webdriver.Chrome()
    driver1.get('https://www.baidu.com')

    kw = input('请在浏览器输入验证码后，在本页面按enter建继续')
    if driver1:
        driver1.close()


search = 0


def proc(company, driver):
    # 不同页面搜索
    register_name = '注册资本'
    partner_name = '股东信息'
    invest_name = '对外投资'
    change_name = '变更记录'
    law_name = '法律诉讼'
    com_name = company
    # start_url = web_url + url
    rubbish_start_tag = ['<div class="inner">', '<div class="info">', '<img']
    rubbish_end_tag = ['</div>', '</div>', '>']
    key = 1

    global search
    if key == 1:
        # 执行不同的搜索页/防识别
        if search == 0:
            try:
                driver.find_element_by_id('home-main-search').send_keys(company)
                # time.sleep(tm1())
                driver.find_element_by_xpath('//div[@tab="js-company"]/div[1]/div').click()
                time.sleep(tm2())

            except:
                try:
                    # 当前页 搜索
                    driver.find_element_by_xpath('//div[@class="search"]//img').click()
                    # time.sleep(tm1())
                    driver.find_element_by_id('header-company-search').send_keys(company)
                    driver.find_element_by_xpath('//div[@class="input-group-btn btn -sm btn-primary"]').click()
                    time.sleep(tm2())
                except:
                    ErrLog(driver.current_url, 1, company, err_msg='搜索界面出错')

        else:
            try:
                # 当前页 搜索
                driver.find_element_by_xpath('//div[@class="search"]//img').click()
                # time.sleep(tm1())
                driver.find_element_by_id('header-company-search').send_keys(company)
                driver.find_element_by_xpath('//div[@class="input-group-btn btn -sm btn-primary"]').click()
                time.sleep(tm2())

            except:
                try:
                    # 重新 从首页进入，搜索
                    driver.find_element_by_xpath('//a[@class="logo-header"]').click()
                    time.sleep(tm2())
                    driver.find_element_by_id('home-main-search').send_keys(company)
                    # time.sleep(tm1())
                    driver.find_element_by_xpath('//div[@tab="js-company"]/div[1]/div').click()
                    time.sleep(tm2())
                except:
                    ErrLog(driver.current_url, 1, company, err_msg='搜索界面出错')

        try:
            # 点击第一个公司
            driver.find_element_by_xpath(
                '//div[@class="result-list sv-search-container"]/div[1]/div/div[3]/div[1]/a').click()
        except:

            Driver_xpathErr()

        # 直接访问公司页面
        time.sleep(tm2())
        windows = driver.window_handles
        driver.close()
        try:
            driver.switch_to.window(windows[1])
        except:
            pass
        # 判断公司获取是否正确
        tree_company = etree.HTML(driver.page_source)
        company_name = tree_company.xpath('//div[@class="content"]/div[@class="header"]/h1/text()')
        try:
            if company != company_name[0]:
                if company_name[0] not in company:
                    if company not in company_name[0]:
                        ErrLog(driver.current_url, 1, company,
                               err_msg='请检查该公司全称<原：%s---现：%s>' % (company, company_name[0]))
                        return
        except:
            # 等待输入验证码
            code()

        # 模拟js滑动
        k = random.randint(150, 300)
        driver.execute_script('var q=document.documentElement.scrollTop=%d' % k)

        # 获取导航栏  公司背景|司法风险|经营风险|公司发展|经营状况|知识产权|历史信息
        # try:
        #     navigations = driver.find_element_by_xpath(
        #         '//div[@class="navigation"]//div[@class="item-container"][1]/a')
        #     # navigations 公司背景  下面鼠标悬浮
        #     ActionChains(driver).move_to_element(navigations).perform()
        #     # time.sleep(tm1())
        #     navigations.click()
        #     time.sleep(tm1())
        # except:
        #     try:
        #         navigations = driver.find_element_by_xpath('//div[@class="item-container"][1]/a')
        #     except:
        #         navigations = None
        #     ErrLog(driver.current_url, 0, com_name, 'cookie 信息出错或者导航栏driver_xpath出错')

        # 注册模块信息
        tree_regiser = etree.HTML(driver.page_source)
        try:
            register_content = tree_regiser.xpath('//table[@class="table -striped-col -border-top-none"]')[0]
            register = etree.tostring(register_content, encoding='utf-8', pretty_print=True,
                                      method='html', ).decode('utf-8')
        except:
            register = ''
            XpathErr(err='register_content xpath路径出错')

        register = process_delete_htmltag(register, rubbish_start_tag, rubbish_end_tag)
        '''注册信息文本调试点'''
        # 防识别(延时）
        # time_event(driver)

        # 股东信息
        try:
            # driver.execute_script('var q=document.documentElement.scrollTop=100')
            # try:
            #     ActionChains(driver).move_to_element(navigations).perform()
            # except:
            #     Driver_xpathErr()
            time.sleep(tm1())
            try:
                partner_buttom = driver.find_element_by_xpath(
                    '//div[@class="navigation"]//div[@class="item-container"][1]/div/div[6]')
                # partner_buttom = driver.find_element_by_link_text('变更记录')
                partner_buttom.click()
            except:
                Driver_xpathErr()
            time.sleep(tm2())
            tree_partner = etree.HTML(driver.page_source)
            try:
                partner_content = tree_partner.xpath('//div[@id="_container_holder"]')[0]
                partner = etree.tostring(partner_content, encoding='utf-8', pretty_print=True,
                                         method='html').decode('utf-8')
            except:
                partner = ''
                XpathErr()

            partner = process_delete_htmltag(partner, rubbish_start_tag, rubbish_end_tag)
        except:
            partner = ''
        '''股东信息调试点'''

        # 对外投资
        try:
            invest_partner = etree.HTML(driver.page_source)
            try:
                invest_content = invest_partner.xpath('//div[@id="_container_invest"]')[0]
                invest = etree.tostring(invest_content, encoding='utf-8', pretty_print=True, method='html').decode(
                    'utf-8')
            except:
                invest = ''
                XpathErr()

            invest = process_delete_htmltag(invest, rubbish_start_tag, rubbish_end_tag)
            '''对外投资文本调试点'''
        except:
            invest = ''

        # 变更记录
        try:
            time.sleep(tm1())

            # 模拟 鼠标浮动
            # try:
            #     ActionChains(driver).move_to_element(navigations).perform()
            # except:
            #     Driver_xpathErr()
            # time.sleep(tm1())
            # driver.execute_script('var q=doument.documentElement.scrollTop=0')
            try:
                driver.find_element_by_xpath(
                    '//div[@class="navigation"]//div[@class="item-container"][1]/div/div[last()-3]').click()
            except:
                Driver_xpathErr()

            change = ''
            # 默认为20页，找不到下一页会自动停止
            for i in range(19):
                time.sleep(tm2())
                tree_change = etree.HTML(driver.page_source)
                try:
                    change_content = tree_change.xpath('//div[@id="_container_changeinfo"]/table[1]')[0]
                    change1 = etree.tostring(change_content, encoding='utf-8', pretty_print=True,
                                             method='html').decode('utf-8')
                except:
                    change1 = ''
                change1 = process_delete_htmltag(change1, rubbish_start_tag, rubbish_end_tag)
                change = change + change1
                try:
                    next_page = driver.find_element_by_xpath(
                        '//div[@id="_container_changeinfo"]/div/ul/li/a[@class="num -next"]')
                except:
                    try:
                        ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                        next_page = driver.find_element_by_xpath(
                            '//div[@id="_container_changeinfo"]/div/ul/li/a[@class="num -next"]')
                    except:
                        try:
                            ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                            ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                            next_page = driver.find_element_by_xpath(
                                '//div[@id="_container_changeinfo"]/div/ul/li/a[@class="num -next"]')
                        except:
                            try:
                                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                                next_page = driver.find_element_by_xpath(
                                    '//div[@id="_container_changeinfo"]/div/ul/li/a[@class="num -next"]')
                            except:
                                next_page = None

                if next_page:
                    try:
                        next_page.click()
                    except:
                        Driver_xpathErr(err='找不到路径，无法点击，增加延时后再试')
                else:
                    break
        except:
            change = ''
        '''变更记录文本调试点'''

        # 防识别（延时）
        # time_event(driver)

        # 法律诉讼
        try:
            # try:
            #     ActionChains(driver).move_to_element(navigations).perform()
            # except:
            #     Driver_xpathErr()
            time.sleep(tm1())
            try:
                driver.find_element_by_xpath(
                    '//div[@class="navigation"]//div[@class="item-container"][2]/div/div[3]').click()
            except:
                Driver_xpathErr()
            time.sleep(tm1())
            law = ''
            # 默认为20页，找不到下一页会自动停止
            for i in range(19):
                time.sleep(tm2())
                tree_law = etree.HTML(driver.page_source)
                try:
                    law_content = tree_law.xpath('//div[@id="_container_lawsuit"]/table')[0]
                    law1 = etree.tostring(law_content, encoding='utf-8', pretty_print=True, method='html').decode(
                        'utf-8')
                except:
                    law1 = ''

                law1 = process_delete_htmltag(law1, rubbish_start_tag, rubbish_end_tag)
                law = law + law1
                # 下一页
                try:
                    next_page = driver.find_element_by_xpath(
                        '//div[@id="_container_lawsuit"]/div/ul/li/a[@class="num -next"]')
                except:
                    try:
                        ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                        next_page = driver.find_element_by_xpath(
                            '//div[@id="_container_lawsuit"]/div/ul/li/a[@class="num -next"]')
                    except:
                        try:
                            ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                            ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                            next_page = driver.find_element_by_xpath(
                                '//div[@id="_container_lawsuit"]/div/ul/li/a[@class="num -next"]')
                        except:
                            try:
                                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()
                                next_page = driver.find_element_by_xpath(
                                    '//div[@id="_container_lawsuit"]/div/ul/li/a[@class="num -next"]')
                            except:
                                next_page = None

                if next_page:
                    try:
                        next_page.click()
                    except Exception:
                        Driver_xpathErr(err='找不到路径，无法点击，增加延时后再试')
                else:
                    break
        except:
            law = ''
        '''法律诉讼文本调试点'''
        # 如果全部为空，继续下次循环
        if register == partner == invest == change == law == '':
            try:
                ErrLog(driver.current_url, 1, company_name[0], err_msg='文本值全为空')
            except:
                ErrLog(driver.current_url, 1, company, err_msg='文本值全为空')
                # 等待输入验证码
                code()

        # 文本处理
        msg = '{}<f>{}<f>{}<f>{}<f>{}<f>{}<f>{}<f>{}<f>{}<f>{}<f>{}<f>{}'.format(company_name[0],
                                                                                 driver.current_url,
                                                                                 register_name,
                                                                                 register, partner_name,
                                                                                 partner,
                                                                                 invest_name, invest,
                                                                                 change_name, change, law_name,
                                                                                 law)
        now_day = datetime.now().strftime('%Y-%m-%d')
        result_file_name = r'{dir_path}'.format(**globals()) + r'/data/{}'.format(now_day) + '.txt'
        try:
            with open(result_file_name, 'a+', encoding='utf-8') as f:
                f.write('{}+\n'.format(msg))
                f.close()

        except Exception:
            XpathErr(err='文件写入错误')

        # 保存cookie
        dict_ = {}
        dict_['cookie'] = driver.get_cookies()
        # num1 = random.randint(1, 10)
        num1 = 1
        file_name1 = r'{dir_path}\cookies\cookie_'.format(**globals()) + str(num1) + '.json'
        with open(file_name1, 'w')as fp:
            fp.write(json.dumps(dict_))

        # 执行不同的搜索页/防识别
        time.sleep(tm1())
        next_num = random.randint(1, 3)
        if next_num == 1:
            search = 0
            try:
                driver.find_element_by_xpath('//a[@class="logo-header"]').click()
            except:
                Driver_xpathErr(err='logo路径错误')
        elif next_num == 2:
            search = 1
            time.sleep(tm2())
        else:
            search = 0
            try:
                driver.find_element_by_xpath('//a[@class="logo-header"]').click()
            except:
                Driver_xpathErr(err='logo路径错误')
        time.sleep(tm3())
        # time.sleep(tm3())
        # time.sleep(tm3())


# 获取中断的公司
def seek():
    try:
        with open(r'{dir_path}\log\exception_log.log'.format(**globals()), 'rb')as f:
            # f.read()
            offset = -50
            while True:
                f.seek(offset, 2)
                lines = f.readlines()
                if len(lines) > 1:
                    last = lines[-1].decode('utf-8')

                    break
                offset *= 2
        com = last.split('<f>')[0]
        try:
            seek_index = companys.index(com)
        except:
            seek_index = 0
    except:
        seek_index = 0

    return seek_index


def start_requests():
    global dir_path
    global excel_name
    global companys
    web_url = 'https://www.tianyancha.com'

    err_num = 0

    # 路径
    io = r'{dir_path}\excel\{excel_name}'.format(**globals())
    # 获取数据列表
    data = pd.read_excel(io=io, header=None).values.tolist()
    companys = [da[0] for da in data]
    # options = webdriver.FirefoxOptions()
    # options.add_argument('--headless')  # 无界面模式、无头模式
    # options.add_argument('--disable-gpu')  # 禁用GPU加速
    # options.add_argument('--user-agent=""')  # 设置请求头
    # options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片，提升速度
    # options.add_argument('--incognito')  # 无痕模式
    # options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动话程序控制
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Firefox()
    # driver = webdriver.Chrome()

    driver.get(web_url)
    time.sleep(tm1())
    # driver.maximize_window()
    driver.delete_all_cookies()
    # 获取登陆的cookie 并导入
    num = 1
    file_name = r'{dir_path}\cookies\cookie_'.format(**globals()) + str(num) + '.json'
    try:
        cookie = json.load(open(file_name, 'r'))
        list_data = cookie['cookie']
    except:
        driver.close()
        raise CookieErr

    for i in list_data:
        driver.add_cookie(i)
    driver.refresh()
    time.sleep(tm1())
    # 中断公司
    seek_index = seek()


    for company in companys[seek_index::]:
        # 写入log.txt
        with open(r'{dir_path}\log\exception_log.log'.format(**globals()), 'a+', encoding='utf-8') as f:
            f.write('{}<f>{}\n'.format(company, driver.current_url))

        proc(company, driver)

    if driver:
        driver.quit()


# 获取TYC的绝对路径 并设置全局变量
path_g = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(os.path.realpath(path_g))

logging.basicConfig(level=logging.INFO,
                    filename=r'{dir_path}\log\err_log.log'.format(**globals()),
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger(__file__)

excel_name = 'companys.xlsx'
start_requests()
