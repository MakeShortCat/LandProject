from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import os
import datetime as dt

driver = webdriver.Chrome('C:/Users/pgs66/Desktop/GoogleDrive/python/Project1/data/driver/chromedriver.exe')

urls = 'https://portal.kfb.or.kr/compare/loan_household_new.php'

driver.get(urls)
driver.find_elements_by_xpath('//*[@id="BankAll"]')[0].click()

for i in range(1,13):

    driver.find_elements_by_xpath(f'//*[@id="month"]/option[{i}]')[0].click()

    driver.find_elements_by_xpath('//*[@id="all_show_2"]')[0].click()

    driver.find_elements_by_xpath('//*[@id="opt_1_1"]')[0].click()

    driver.find_elements_by_xpath('//*[@id="Content"]/div[3]/form/div/div[5]/span/a')[0].click()
    time.sleep(2)
    driver.find_elements_by_xpath('//*[@id="SearchResult"]/div[1]/ul/li[2]/span/a')[0].click()
    today = dt.datetime(2013, i, 1).strftime('%Y_%m')
    time.sleep(1)
    os.rename('C:/Users/pgs66/Downloads/가계대출금리[2015년 8월 이전](분할상환방식 주택담보대출(만기 10년 이상) 신용등급별 금리현황 )_20230211.xlsx', f'Project1/data/income/{today}.xlsx')

os.rename('C:/Users/pgs66/Downloads/가계대출금리(분할상환방식 주택담보대출(만기 10년 이상) 신용등급별 금리현황 )_20230211.xlsx', 'Project1/data/income/123123.xlsx')

