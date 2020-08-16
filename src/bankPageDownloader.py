
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

import src.secrets as secrets
import src.selected_cards as selected_cards


class Page:

    def __init__(self, webdriver):
        self.browser = webdriver
        self.__cards_indexes = []
    

    def start(self):
        self.open_page()
        session_started = self.init_sesion()

        if session_started:
            self.check_promos_popup()
            self.iterate_over_cards()
            self.close_sesion()
            self.stop_browser()

        else:
            self.stop_browser()


    def open_page(self):
        self.browser.get('https://bancanet.banamex.com/MXGCB/JPS/portal/LocaleSwitch.do')
        sleep(5)
    

    def init_sesion(self):
        self.check_first_popup()

        if self.enter_credentials_pass() and self.no_other_session_active():
            return True
        else:
            return False
        

    
    def check_first_popup(self):
        try:
            popupclose = self.browser.find_element_by_xpath('//*[@id="splash-207555-close-button"]')
            popupclose.click()
            return True
        except:
            return True

    def check_promos_popup(self):
        try:
            sleep(15)
            popup = page.browser.find_element_by_xpath('//*[@id="outerContainer"]/div[2]')
            popup.click()
            return True
        except:
            print('no promos hoy')
            return True
    

    def enter_credentials_pass(self):
        userinput = self.browser.find_element_by_xpath('//*[@id="textCliente"]')
        userinput.send_keys( secrets.username )
        self.browser.find_element_by_xpath('//*[@id="loginCustomerBox"]/div[3]/a').click()
        user_name = self.browser.find_element_by_xpath('//*[@id="content3"]/div[3]/div[1]')
        
        if secrets.user_hint in user_name.text:
            pwd_input = self.browser.find_element_by_xpath('//*[@id="textFirma"]')
            pwd_input.send_keys( secrets.pwd )
            self.browser.find_element_by_xpath('//*[@id="enterId"]').click()
            return True
        else:
            return False



    def no_other_session_active(self):
        sleep(3)
        if 'Solo puedes tener' in self.browser.page_source and 'activa' in self.browser.page_source:
            return False
        else:
            return True


    def obtain_cards_indexes(self):
        table = self.browser.find_element_by_xpath('//*[@id="accountsPanelInnerContainer"]/div[1]/table')
        tbodies = table.find_elements(By.TAG_NAME, 'tbody')
        
        indexes = []

        for body_index in range( len(tbodies) ):
            trs = tbodies[body_index].find_elements(By.TAG_NAME, 'tr')

            for tr_index in range( len(trs) ):
                tr = trs[tr_index]
                tds = tr.find_elements(By.TAG_NAME, 'td')

                if len(tds) > 2 and tds[1].text in selected_cards.card_names and tds[1].text:
                    index = { 'tbody_index': body_index, 'tr_index': tr_index, 'card_name': tds[1].text }
                    indexes.append(index)

        self.__cards_indexes = indexes

    
    def iterate_over_cards(self):
        self.obtain_cards_indexes()

        for index in self.__cards_indexes:
            table = self.browser.find_element_by_xpath('//*[@id="accountsPanelInnerContainer"]/div[1]/table')
            tbody = table.find_elements(By.TAG_NAME, 'tbody')[ index['tbody_index'] ]
            tr = tbody.find_elements(By.TAG_NAME, 'tr')[ index['tr_index'] ]
            tds = tr.find_elements(By.TAG_NAME, 'td')
            
            if tds[1].text == index['card_name']:
                htmla = tds[0].find_elements(By.TAG_NAME, 'a')
                htmla[0].click()
                print('downloading for card:')
                print(index['card_name'])
                sleep(5)
                self.donwload_csv()
                
            else:
                print('Something changed names not match')


    def donwload_csv(self):
        export = self.browser.find_element_by_xpath('//*[@id="cmlink_DownloadActivityLink"]')
        export.click()
        sleep(2)
        download = self.browser.find_element_by_xpath('//*[@id="DownLoadActivity_Next"]')
        download.click()
        sleep(2)
        confirm = self.browser.find_element_by_xpath('//*[@id="DownLoadActivity_Process"]')
        confirm.click()
        sleep(10)
        close = self.browser.find_element_by_xpath('//*[@id="DownLoadActivity_Complete"]')
        close.click()
        back = self.browser.find_element_by_xpath('//*[@id="link_lkMyAccounts"]')
        back.click()

        self.check_promos_popup()

    def stop_browser(self):
        self.browser.close()
        print('pendejo')


    def close_sesion(self):
        self.browser.find_element_by_xpath('//*[@id="link_logout"]').click()


# driver = webdriver.Chrome()
# page = Page(driver)
# page.start()
if __name__ == '__main__':
    print('is main')
    