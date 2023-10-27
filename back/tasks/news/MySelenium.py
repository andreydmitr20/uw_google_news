from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MySelenium:
    def __init__(
        self,
        selenium_driver,
    ) -> None:
        self.__driver = selenium_driver
        self.__actions = None

    def get_driver(self):
        return self.__driver

    def get_actions(self):
        return self.__actions

    def set_actions(self, actions):
        self.__actions = actions

    # click
    def click(self, element):
        if element:
            self.__actions.move_to_element(element).click().perform()

    # findElement
    def find_element_by_css(self, element, css_selector: str):
        if element:
            try:
                return element.find_element(By.CSS_SELECTOR, css_selector)
            except Exception as exception:
                return None

    def find_elements_by_css(self, element, css_selector: str):
        if element:
            try:
                return element.find_elements(By.CSS_SELECTOR, css_selector)
            except Exception as exception:
                return []

    def find_element_by_xpath(self, element, xpath_selector: str):
        if element:
            try:
                return element.find_element(By.XPATH, xpath_selector)
            except Exception as exception:
                return None

    def find_elements_by_xpath(self, element, xpath_selector: str):
        if element:
            try:
                return element.find_elements(By.XPATH, xpath_selector)
            except Exception as exception:
                return []

    # send_keys
    def send_keys(self, element, keys):
        element.send_keys(keys)

    # current_url
    def current_url(self):
        return self.__driver.current_url

    # scroll_into_view
    def scroll_into_view(self, element):
        self.__driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def go_up_to_element_with_css(self, element, css_selector: str):
        if element is None:
            return None
        while True:
            parent = self.find_element_by_xpath(element, "..")
            if parent is None:
                return None
            result = self.find_elements_by_css(parent, css_selector)
            if len(result) > 0:
                return result[0]
            element = parent

    def switch_to_tab_index(self, tab_index: int):
        self.__driver.switch_to.window(self.__driver.window_handles[tab_index])

    def wait_tag_with_timeout(self, tag: str, timeout_in_seconds: int):
        wait = WebDriverWait(self.__driver, timeout_in_seconds)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, tag)))
