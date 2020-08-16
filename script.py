from selenium import webdriver
from src.bankPageDownloader import Page


if __name__ == '__main__':
    print('is main')
    driver = webdriver.Chrome()
    page = Page(driver)
    page.start()
    