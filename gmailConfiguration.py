# -*- coding: utf-8 -*-
from time import sleep
import traceback
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

__author__ = 'Jasper'


class GmailConfiguration:
    def __init__(self, accounts):
        self.accounts = accounts
        self.driver = None

    def run(self):
        self.before()
        for account in self.accounts:
            self.act(account)
        self.after()

    def before(self):
        agent_options = GmailConfiguration.select_agent()
        self.initialize_driver(agent_options)

    def act(self, account):
        if self.login(account):
            self.configure_settings()
            self.logout()
        self.clear_chrome_history()
        sleep(8)

    def after(self):
        self.driver.quit()

    @staticmethod
    def select_agent():
        agents = [
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
            "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
            "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"]
        # pick one element of agents
        agent = random.choice(agents)
        options = Options()
        options.add_argument("""user-agent=""" + agent)
        return options

    def initialize_driver(self, options):
        wait_time = 5  # TODO
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(wait_time)

    def login(self, account):
        try:
            email = account[0]
            password = account[1]
            gmail_login_URL = """https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1&lp=1&hl=zh-CN#identifier"""

            self.driver.get(gmail_login_URL)
            self.driver.find_element_by_id("Email").send_keys(email)
            self.driver.find_element_by_id("next").send_keys(Keys.ENTER)
            self.driver.find_element_by_id("Passwd").send_keys(password)
            self.driver.find_element_by_id("signIn").send_keys(Keys.ENTER)
            sleep(30)
            return True
        except Exception as error:
            print error

        return False

    def configure_settings(self):
        try:
            self.go_to_setting()
            self.change_language()
            self.configure_POP_IMAP()
            self.save_changes()
            sleep(30)
            self.enable_insecure_app()

            return True
        except Exception as error:
            print traceback.format_exc()

        return False

    def go_to_setting(self):
        self.driver.get("""https://mail.google.com/mail/#inbox""")
        sleep(30)
        elements = self.driver.find_elements_by_id(":2m")
        if not elements:
            self.driver.get("""https://mail.google.com/mail/#inbox""")
            sleep(30)
            elements = self.driver.find_elements_by_id(":2m")
        elements[0].send_keys(Keys.ENTER)
        self.driver.find_element_by_id("ms").click()

    def change_language(self):
        language_selector = Select(self.driver.find_element_by_class_name("a5p"))
        # first_selected_option is present selected value
        if language_selector.first_selected_option.get_attribute("value") is "zh-CN":
            return
        language_selector.select_by_value("zh-CN")

    def configure_POP_IMAP(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'#settings/fwdandpop')]").click()

        # 勾選"对所有邮件启用POP（包括已经下载的邮件）"
        POP_btn = self.driver.find_element_by_xpath("//input[@type='radio'][@name='bx_pe'][@value='3']")
        if not POP_btn.is_selected():
            POP_btn.click()

        # Xpath的index是從1開始; ex:td[1], td[2], 而沒有td[0]
        # 選擇"删除Gmail的副本"
        POP_selector = Select(
            self.driver.find_element_by_xpath("//div[@class='nH Tv1JD']/div/table/tbody/tr[2]/td[2]/div[2]/select"))
        if POP_selector.first_selected_option.get_attribute("value") is "2":
            return
        POP_selector.select_by_value("2")

        # 勾選"启用 IMAP"
        IMAP_btn = self.driver.find_element_by_xpath("//input[@type='radio'][@name='bx_ie'][@value='1']")
        if not IMAP_btn.is_selected():
            IMAP_btn.click()

    def save_changes(self):
        self.driver.find_element_by_xpath("//div[@class='nH Tv1JD']/div/table/tbody/tr[4]/td/div/button[1]").click()

    def enable_insecure_app(self):
        self.driver.get("https://myaccount.google.com/security?utm_source=OGB")
        elements = self.driver.find_elements_by_xpath("//div[@class='W qe  H']")
        if elements:
            sleep(5)
            return
        self.driver.find_element_by_xpath("//div[@jsaction='JIbuQc:gupWTd']/div").click()
        sleep(5)

    def logout(self):
        self.driver.get("https://accounts.google.com/Logout?service=accountsettings")
        sleep(10)

    def clear_chrome_history(self):
        try:
            self.driver.get("chrome://settings/clearBrowserData")
            sleep(5)
            self.driver.switch_to.frame("settings")
            clear_data = self.driver.find_element_by_id("clear-browser-data-time-period")
            select = Select(clear_data)
            select.select_by_value("4")
            sleep(5)
            checkboxes = self.driver.find_element_by_id("clear-data-checkboxes")
            all_inputs = checkboxes.find_elements_by_tag_name("input")
            for input in all_inputs:
                if not input.is_selected():
                    input.click()
                    sleep(2)
            self.driver.find_element_by_id("clear-browser-data-commit").send_keys(Keys.ENTER)
            sleep(5)
        except Exception as error:
            print traceback.format_exc()


def main():
    accounts = [["cheng6dindin@gmail.com", "c7654321"],
                ["symboliz30670@gmail.com", "wuay1fjnxi7"],
                ["Ola.42887914@gmail.com", "wt4tn2ipvimo"]
                ]

    gmail_config_obj = GmailConfiguration(accounts)
    gmail_config_obj.run()


if __name__ == '__main__':
    main()


# self.driver.get('http://www.google.com')
# self.driver.quit()

# 自己申請新帳號測試
