from selenium import webdriver
import time
from options import options_control
from PIL import Image
from chaojiying import ChaojiyingClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 打开浏览器
driver = webdriver.Firefox()
driver.implicitly_wait(10)


def define_yzm():
    try:
        inpu = driver.find_elements_by_css_selector('#yucinput')[0]
        inpu.click()
        time.sleep(0.5)
        return True
    except:
        print("此页面无验证码！")
        return False


def captchaCode():
    # 截取整个网页
    driver.save_screenshot('wholeWeb.png')
    # 定位验证码位置
    left = 882
    top = 946
    right = 1022
    bottom = 986

    im = Image.open('wholeWeb.png')
    im = im.crop((left, top, right, bottom))
    im.save('captcha.png')


def identify():
    '''
    验证码识别
    :return: 验证码
    '''
    chaojiying = ChaojiyingClient('超级鹰账号', '密码', '秘钥ID')
    im = open('captcha.png', 'rb').read()
    pic_str = chaojiying.PostPic(im, 1902)['pic_str']
    return pic_str


for k in range(233, 243):
    # 加载网页
    driver.get("https://www.wjx.cn/jq/46226271.aspx")
    time.sleep(1)

    xpath1, xpath2, xpath3, xpath4, xpath5, xpath6, xpath7, xpath8, xpath9, xpath10, xpath11, xpath12, xpath13 = options_control(k)

    # 点击各个选项
    driver.find_element_by_xpath(xpath1).click()
    driver.find_element_by_xpath(xpath2).click()
    driver.find_element_by_xpath(xpath3).click()
    driver.find_element_by_xpath(xpath4).click()
    driver.find_element_by_xpath(xpath5).click()
    driver.find_element_by_xpath(xpath6).click()
    driver.find_element_by_xpath(xpath7).click()
    driver.find_element_by_xpath(xpath8).click()
    driver.find_element_by_xpath(xpath9).click()
    driver.find_element_by_xpath(xpath10).click()
    driver.find_element_by_xpath(xpath11).click()
    driver.find_element_by_xpath(xpath12).click()
    driver.find_element_by_xpath(xpath13).click()

    # 判断页面是否有验证码
    yzm = define_yzm()
    if yzm:
        captchaCode()
        code = identify()
        print('验证码：%s' % code)
        inpu = driver.find_elements_by_id('yucinput')[0]
        inpu.send_keys(code)

    # 提交
    driver.find_element_by_id("submit_button").click()

    time.sleep(2)
    try:
        finished = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#ctl01_ContentPlaceHolder1_lbDefault"))
        )
        print('————————第%d页已完成————————' % k)
    except:
        print('————————第%d页失败！————————' % k)

# 关闭浏览器
driver.quit()
