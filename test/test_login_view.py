from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class LiveServerTestCase(LiveServerTestCase):

    def scrap(self):
        service = Service(ChromeDriverManager().install())
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--enable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
        return driver

    def testLoginAcademic_correct(self):
        driver = self.scrap()
        driver.get('http://127.0.0.1:8000/')
        assert "Icesi Sistema Freya" in driver.title
        btn = driver.find_element(
            By.XPATH, '/html/body/div/div/div/div[3]/button[2]')
        btn.click()
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/form/div[3]/button')
        username.send_keys('1109185587')
        password.send_keys('Contraseña1')
        login.click()
        assert "http://127.0.0.1:8000/index/" in driver.current_url

    def testLoginCcsa_correct(self):
        driver = self.scrap()
        driver.get('http://127.0.0.1:8000/')
        assert "Icesi Sistema Freya" in driver.title
        btn = driver.find_element(
            By.XPATH, '/html/body/div/div/div/div[3]/button[1]')
        btn.click()
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/form/div[3]/button')
        username.send_keys('31764131')
        password.send_keys('Ellider123')
        login.click()
        assert "http://127.0.0.1:8000/index/" in driver.current_url

    def testLoginAcademic_incorrect(self):
        driver = self.scrap()
        driver.get('http://127.0.0.1:8000/')
        assert "Icesi Sistema Freya" in driver.title
        btn = driver.find_element(
            By.XPATH, '/html/body/div/div/div/div[3]/button[2]')
        btn.click()
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/form/div[3]/button')
        username.send_keys('1110')
        password.send_keys('C')
        login.click()
        assert "Inicio Sesión" in driver.title

    def testLoginCcsa_incorrect(self):
        driver = self.scrap()
        driver.get('http://127.0.0.1:8000/')
        assert "Icesi Sistema Freya" in driver.title
        btn = driver.find_element(
            By.XPATH, '/html/body/div/div/div/div[3]/button[1]')
        btn.click()
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(
            By.XPATH, '/html/body/div/div/div[2]/form/div[3]/button')
        username.send_keys('1110')
        password.send_keys('C')
        login.click()
        assert "Inicio Sesión" in driver.title
