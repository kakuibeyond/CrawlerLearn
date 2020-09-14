from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10, poll_frequency=1)

keyword = '战略合作'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
search_url = 'http://www.nbd.com.cn/'

def search(keyword,search_url):
    try:
        browser.get(search_url)
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.g-top > div > div > form > input.u-magnifier')))
        input.send_keys(keyword)
        submit.click()
        time.sleep(1)

        submit2 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.search-column1 > div.left-suffix > div > ul.label-block.js-result > li:nth-child(2)')))
        submit2.click()
        print(EC.findElement(By.cssSelector("body > div.search-column1 > div.right-content > ul > li:nth-child(1) > a > p")))
        news_num = wait.until(EC.presence_of_element_located((By.xpath,'body > div.search-column1 > div.right-content > div > p[2]')))
        return news_num.text
    except TimeoutException:
        print('搜索超时')
        return search(keyword,search_url)



if __name__ == '__main__':
    search(keyword, search_url)