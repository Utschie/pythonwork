from selenium import webdriver
from selenium.common.exceptions import TimeoutException

proxylist=['58.12.12.12:80','69.12.12.12:80']
weblist=['https://www.google.com','https://www.facebook.com','https://www.yahoo.com','https://aol.com']


def test():
    temp_count_proxy = 0
    driver_opened = 0
    for url in weblist:
        if temp_count_proxy > len(proxylist):
            print("Out of proxy")
            return

        if driver_opened == 0:
            service_args = ['--proxy={}'.format(proxylist[temp_count_proxy]),'--proxy-type=socks5']
            driver = webdriver.PhantomJS('E:/phantomjs-2.1.1-windows/bin/phantomjs.exe', service_args = service_args)
            driver_opened = 1

        try:
            driver.set_page_load_timeout(2)
            driver.get(url)
        except TimeoutException as ex:
            driver.close()
            driver_opened = 0
            temp_count_proxy += 1
            continue


