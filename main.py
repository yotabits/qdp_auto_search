from selenium import webdriver
from selenium.webdriver.support.ui import Select
import selenium
import time
import re


class Cst:
    search_uri = 'https://qpldocs.dla.mil/search/'
    manufacturer_per_page = 5


class Distributor:
    def __init__(self, name, mfr_designation, country, cage, color):
        self.name = name
        self.mfr_designation = mfr_designation
        self.country = country
        self.cage = cage
        self.color = color

    def print_info(self):
        print("Mfr designation: " + self.mfr_designation)
        print("Name: " + self.name)
        print("Country: " + self.country)
        print("Cage: " + self.cage)
        print("Color: " + self.color)


class SearchResult:
    def __init__(self, distributor_list, search):
        self.dist_list = distributor_list
        self.search_str = search

    def pretty_print(self):
        print('#####################################')
        print('-----------> ' + self.search_str)
        print('#####################################')
        if not self.dist_list:
            print("NOT FOUND")
        for dist in self.dist_list:
            print('////////////////////////////////')
            dist.print_info()

class Searcher:
    def __init__(self, target_uri):
        self._driver = webdriver.Chrome(executable_path='/home/tkostas/chromedriver')
        self._driver.implicitly_wait(3)
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

    def select_first_search_result(self):
        a = self._driver.find_element_by_xpath("//*[@id=\"search_list_DG\"]/tbody/tr[2]/td[1]/a")
        a.click()
        self._driver.implicitly_wait(2)

    def select_firt_govt_designation(self):
        a = self._driver.find_element_by_xpath("//*[@id=\"Lu_gov_DG_ctl03_btnGovPartNo\"]")
        a.click()
        self._driver.implicitly_wait(2)

    def loop_in_results(self):
        distributor_list = []
        part_count = self.get_part_count()
        for i in range(0, int(part_count / Cst.manufacturer_per_page)):
            distributor_list += self.get_one_page_content(Cst.manufacturer_per_page)
            next_btn = self._driver.find_element_by_id("Lu_man_Datagrid_navigation1_btnNext")
            next_btn.click()
        distributor_list += self.get_one_page_content(part_count % Cst.manufacturer_per_page)

        return distributor_list

    def get_one_page_content(self, nb_lines):
        distributor_list = []
        start_index = 3
        prefix = "Lu_man_DG_ctl0"
        mfr_design_indexed = lambda index: prefix + str(index) +\
                                           "_lblMfgPart"
        company_indexed = lambda index: prefix + str(index) +\
                                           "_lblCompany"
        country_indexed = lambda index: prefix + str(index) +\
                                           "_lblCountry"
        cage_indexed = lambda index: prefix + str(index) +\
                                           "_lblCAGECode"
        status_img_indexed = lambda index: prefix + str(index) +\
                                           "_imgCompanyStatus"

        text_for_id = lambda id: self._driver.find_element_by_id(id).text

        for i in range(start_index, start_index + nb_lines):
            mfr = text_for_id(mfr_design_indexed(i))
            company = text_for_id(company_indexed(i))
            country = text_for_id(country_indexed(i))
            cage = text_for_id(cage_indexed(i))

            status_img = self._driver.find_element_by_id(status_img_indexed(i))
            img_path = status_img.get_attribute('src')
            color = re.search('Green|Red|Yellow|no_shipping', img_path).group(0)

            to_add = Distributor(company, mfr, country, cage, color)
            distributor_list.append(to_add)

        return distributor_list

    def get_part_count(self):
        pcount_str = self._driver.find_element_by_id("Lu_man_lblCnt")
        found = re.search("[0-9]+", pcount_str.text)
        if found is not None:
            print("Available manufacturers " + found.group(0))
        return int(found.group(0))

    def build_search_result(self, to_search):
        self.search(to_search)
        try:
            self.select_first_search_result()
        except selenium.common.exceptions.NoSuchElementException:
            return SearchResult([], to_search)

        self.select_firt_govt_designation()
        res_list = self.loop_in_results()
        return SearchResult(res_list, to_search)


def main():

    to_search_list = [
        #"MS90335-3",
        #"M12883/51-003",
        #"MS27718-26-1",
        #"MS90311-711",
        #"M39029/58-364",
        #"MS27488-16-2",
        #"MS3320-20",
        "M83536/6-022M",
        "MS24523-22",
        "M12883/51-002"
    ]

    reslist = []
    for str_s in to_search_list:
        s = Searcher(Cst.search_uri)
        res = s.build_search_result(str_s)
        reslist.append(res)
        res.pretty_print()



main()