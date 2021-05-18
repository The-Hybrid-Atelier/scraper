
# Hedieh Moradi- 2021- Hybrid Atelier
#  This program will go through glazy.org/recipes page. Then it will run a selenium through chrome to
# go through each recipe page, wait for the API call and get the API link (returns a JSON)
# Then dump all the links into a JSON file.
# To run this program you need to have scrapy spider installed and add this file into the spider folder

# Packages

from selenium import webdriver
#pckg to get the network api calls
from selenium.webdriver import DesiredCapabilities

from time import sleep
import json
import scrapy
#import for wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ApiLinks(scrapy.Spider):
    name ='api_links'
    allowed_domains = ['glazy.org']
    start_urls=['https://glazy.org/recipes/23494']

    def __init__(self):
        # make chrome log requests
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {
            "performance": "ALL"}  
        self.driver = webdriver.Chrome(
            desired_capabilities=capabilities, executable_path="YOUR_LocalPath_To_ChromeDriver")
    
    def parse(self, response):
        self.driver.get(response.url)
        sleep(5)


           
        resp_url=[]
        while True:
            logs_raw = self.driver.get_log("performance")
            logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
            def log_filter(log_):
                return (
                    # is an actual response
                    log_["method"] == "Network.responseReceived"
                    # and json
                    and "json" in log_["params"]["response"]["mimeType"]
                )

            for log in filter(log_filter, logs):
                request_id = log["params"]["requestId"]
                resp_url.append(log["params"]["response"]["url"])
            
            next_page= self.driver.find_element_by_css_selector(".fa.fa-angle-right")
            try:
                next_page.click()
                sleep(5)

            except:
                break
        # dump all links into this JSON file
        with open('YOUR_FileName.json',"w") as f:
            json.dump(resp_url,f,indent=2)

        self.driver.close()


    
