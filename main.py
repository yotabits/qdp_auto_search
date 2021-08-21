from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
# #import pandas as pd

# url = "http://gts.co.jefferson.co.us/index.aspx"
# # create a new Firefox session
# driver = webdriver.Chrome(executable_path='/home/tkostas/Downloads/chromedriver')
# driver.implicitly_wait(2)
# driver.get(url)
# driver.
# accept_button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnAcceptTerms")
# accept_button.click(

class Cst:
    search_uri = 'https://qpldocs.dla.mil/search/'


class Searcher:
    def __init__(self, target_uri):
        self._driver = webdriver.Chrome(executable_path='/home/tkostas/Downloads/chromedriver')
        self._driver.implicitly_wait(1)
        self._driver.get(target_uri)

    def set_search_type(self):
        dd = self._driver.find_element_by_id("Search_panel1_dd")
        Select(dd).select_by_visible_text("Govt Designation")

    def search(self, to_search):
        self.set_search_type()
        search_field = self._driver.find_element_by_id("Search_panel1_tbox")
        search_field.send_keys(to_search)
        search_btn = self._driver.find_element_by_id("Search_panel1_btn")
        search_btn.click()
        self._driver.implicitly_wait(2)
        #tab = self._driver.find_element_by_id('search_list_DG')

        a = self._driver.find_element_by_xpath("//*[@id=\"search_list_DG\"]/tbody/tr[2]/td[1]/a")
        a.click()


def main():
    s = Searcher(Cst.search_uri)
    s.search("M39029/58-364")
    #s.search("MS27488-16-2")
    #s.search("MS3320-20")
    time.sleep(80)



main()