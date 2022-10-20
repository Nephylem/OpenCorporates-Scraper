from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType, Proxy

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import config

import os, time, re, random
from datetime import datetime
import pandas as pd



BASE_PATH = os.path.dirname(os.path.abspath("__main__"))

output = {
        'Term' : [],
        'OC1' : [],
        'OC2' : [], 
        'OC_Score' : [],
        'OC_US': [],
        'OC_West' : [],
            }

default_url = "https://opencorporates.com/users/sign_in"


def initialize_browser(username, password, proxy_port, headless=True, **kwargs):

    for key, value in kwargs:
        setattr(key, value)

    def sign_in_credentials(username, password, driver):
        wait = WebDriverWait(driver, 5)

        driver.get(default_url)
        
        usernamefield = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="user_email"]')))
        passwordfield = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="user_password"]')))
        submitbutton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-primary"]')))

        usernamefield.send_keys(username)
        passwordfield.send_keys(password)
        submitbutton.click()
        
    proxy = Proxy()
    capabilities = DesiredCapabilities.CHROME
    options = Options()

    #random userAgent
    ua = UserAgent()
    userAgent = ua.random

    options.add_argument(f"user-agent={userAgent}")
    service = Service(os.path.join(BASE_PATH, 'chromedriver.exe'))

    #suppress "usb_device_handle_win.cc:1048"
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #headless browsing
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    if proxy_port:
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = proxy_port
        proxy.ssl_proxy = proxy_port
        proxy.ftp_proxy = proxy_port
        proxy.no_proxy = ''
        proxy.add_to_capabilities(capabilities=capabilities)
        # print(f"\nrunning with proxy -> {proxy_port}")
    
    else:
        print("running without proxy...")

    driver = Chrome(desired_capabilities=capabilities, options=options, service=service)
    sign_in_credentials(username, password, driver)
      
    return driver

def result_for_OC1(term, driver):
    
    #for oc1_good_search_results
    def good_results(term, elements):
        container = []
        if 'the ' in term.lower():
            pattern = re.compile(r'\A\b%s\b|\A%s\b,' %(term, term), re.IGNORECASE)
        else:
            pattern = re.compile(r'\A\b%s\b|\A\bThe %s\b,' %(term, term), re.IGNORECASE)                    
        for element in elements:
            if pattern.search(string=element.get_text()):
                container.append(element.get_text())
        return len(container)

    #for WEST results
    def west_result(elements):
        container = []
        pattern = config.west_pattern
        for element in elements:
            if re.search(pattern=pattern, string=element.get_text()):
                west_element = element.select_one('span[class="count"]').get_text().replace(",","")
                container.append(int(west_element))
        return sum(container)

    #for US results
    def us_result(elements):
        container = []
        for element in elements:
            if "(US)" in element.get_text():
                us_element = element.select_one('span[class="count"]').get_text().replace(",","")
                container.append(int(us_element))

        return sum(container)
  
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # oc1 number of found companies
    oc1_results_element = soup.select_one(config.num_companies_selector)
    oc1_results = int(re.findall(string=oc1_results_element.get_text(), pattern=config.oc_results_pattern)[0].replace(',', ""))

    # number of items in the page
    item_results_elements = soup.select(config.items_page_selector)

    # jurisdiction filter side panel results
    sidepanel_all_results = soup.select(config.jurisdiction_filter_selector)
    
    oc1_us_results = us_result(sidepanel_all_results)
    oc1_west_results = west_result(sidepanel_all_results)

    oc1_page1_good_results = good_results(term, item_results_elements)
    oc1_page1_results = int(len(item_results_elements))
    try:
        oc1_percentage = oc1_page1_good_results/oc1_page1_results       
    
    except ZeroDivisionError:
        oc1_percentage = 0
        
    return (oc1_results, oc1_percentage, oc1_us_results, oc1_west_results)


def result_for_OC2(term, driver):

    #for oc2_good_search_results
    def good_results(term, elements):
        container = []
        pattern = re.compile(r'\b%s\b' %(term), re.IGNORECASE)
        for element in elements:
            if pattern.search(string=element.get_text().lower()):
                container.append(element.get_text())
        return len(container)

    #for WEST results
    def west_result(elements):
        container = []
        pattern = config.west_pattern
        for element in elements:
            if re.search(string=element.get_text(), pattern=pattern):
                west_element = element.select_one('span[class="count"]').get_text().replace(",","")
                container.append(int(west_element))
        return sum(container)

    #for US results
    def us_result(elements):
        container = []
        for element in elements:
            if "(US)" in element.get_text():
                us_element = element.select_one('span[class="count"]').get_text().replace(",","")
                container.append(int(us_element))

        return sum(container)


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # oc2 number of found companies
    oc2_results_element = soup.select_one(config.num_companies_selector)
    oc2_results = int(re.findall(string=oc2_results_element.get_text(), pattern=config.oc_results_pattern)[0].replace(',', ""))

    # number of items in the page
    item_results_elements = soup.select(config.items_page_selector)

    # jurisdiction filter side panel results
    sidepanel_all_results = soup.select(config.jurisdiction_filter_selector)

    oc2_us_results = us_result(sidepanel_all_results)
    oc2_west_results = west_result(sidepanel_all_results)

    oc2_page1_good_results = good_results(term, item_results_elements)
    oc2_page1_results = int(len(item_results_elements))

    try:
        oc2_percentage = oc2_page1_good_results/oc2_page1_results
    
    except ZeroDivisionError:
        oc2_percentage = 0

    return (oc2_results, oc2_percentage, oc2_us_results, oc2_west_results)


def search(driver, terms=[]):     

    for term in terms:
        
        delay = random.uniform(.2, config.MAX_DELAY)
        time.sleep(delay)

        KEYWORD_OC1 = "".join(term.split(" "))
        OC1_RESULT_URL = f'https://opencorporates.com/companies?utf8=%E2%9C%93&q={KEYWORD_OC1}&commit=Go&jurisdiction_code=&utf8=%E2%9C%93&commit=Go&controller=searches&action=search_companies&inactive=false&mode=best_fields&search_fields%5B%5D=name&branch=false&nonprofit=&order=incorporation_date'
        oc1_term = KEYWORD_OC1
        driver.get(OC1_RESULT_URL)

        # show_all_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="facets"]/div[1]/a[1]')))
        # show_all_button.click()
        (oc1_results, oc1_percentage, oc1_us_results, oc1_west_results) = result_for_OC1(oc1_term, driver)

        if 'the ' in term.lower():
            KEYWORD_v2OC1 = "+".join(term.split(" "))
            v2OC1_RESULT_URL = f'https://opencorporates.com/companies?utf8=%E2%9C%93&q={KEYWORD_v2OC1}&commit=Go&jurisdiction_code=&utf8=%E2%9C%93&commit=Go&controller=searches&action=search_companies&inactive=false&mode=best_fields&search_fields%5B%5D=name&branch=false&nonprofit=&order=incorporation_date'
            
            driver.get(v2OC1_RESULT_URL)

            (v2oc1_results, v2oc1_percentage, v2oc1_us_results, v2oc1_west_results) = result_for_OC1(term, driver)

            oc1_results += v2oc1_results
            oc1_percentage += v2oc1_percentage
            oc1_us_results += v2oc1_us_results
            oc1_west_results += v2oc1_west_results

        KEYWORD_OC2 = "+".join(term.split(" "))
        OC2_RESULT_URL = f"https://opencorporates.com/companies?utf8=%E2%9C%93&q={KEYWORD_OC2}&commit=Go&jurisdiction_code=&utf8=%E2%9C%93&commit=Go&controller=searches&action=search_companies&inactive=false&mode=phrase_prefix&branch=false&nonprofit=&order=incorporation_date"
        
        driver.get(OC2_RESULT_URL)

        (oc2_results, oc2_percentage, oc2_us_results, oc2_west_results) = result_for_OC2(term, driver)

        OC1 = oc1_results*oc1_percentage
        OC2 = oc2_results*oc2_percentage

        OC_Score = oc1_us_results*oc1_percentage + oc2_us_results*oc2_percentage + 0.5*(oc1_west_results*oc1_percentage + oc2_west_results*oc2_percentage)
        try:
            OC_US = (oc1_us_results + oc2_us_results) / (oc1_results +  oc2_results)
        
        except ZeroDivisionError:
            OC_US = 0
        
        try:
            OC_West = (oc1_west_results + oc2_west_results) / (oc1_results +  oc2_results)
        
        except ZeroDivisionError:
            OC_West = 0

        output['Term'].append(term)
        output['OC1'].append(format(OC1, '.2f')) 
        output['OC2'].append(format(OC2, '.2f')) 
        output['OC_Score'].append(format(OC_Score, '.2f'))
        output['OC_US'].append(format(OC_US, '.2f'))
        output['OC_West'].append(format(OC_West, '.2f'))
  
    return output
    

def save_output(output_dict):
    
    current_time = datetime.now().strftime("(%H%M%S)")
    dataframe = pd.DataFrame(output_dict)
    dataframe.to_csv(f'output{current_time}.csv', index=False)





