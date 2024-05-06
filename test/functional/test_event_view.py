from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class TestWebAutomation(LiveServerTestCase):
    """Test suite for web automation using Selenium."""

    def _get_webdriver(self):
        """Instantiate a headless Chrome WebDriver."""
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        return webdriver.Chrome(options=options)

    def test_event_manager_end_event(self):
        """Test event manager ending an event."""
        driver = self._get_webdriver()
        driver.get('http://127.0.0.1:8000/')
        assert "Icesi Sistema Freya" in driver.title
        btn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/button[1]')
        btn.click()
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/div[3]/button')
        username.send_keys('31764131')
        password.send_keys('Ellider123')
        login.click()
        assert "http://127.0.0.1:8000/index/" in driver.current_url

        driver.get('http://127.0.0.1:8000/event-list/')
        end = driver.find_element(By.XPATH, '/html/body/div[3]/div/table/tbody/tr[1]/td[12]/form/button')
        end.click()
        assert "http://127.0.0.1:8000/event-list/" in driver.current_url

    def test_ceremony_manager(self):
        """Test ceremony manager performing tasks."""
        driver = self._get_webdriver()
        driver.get('http://127.0.0.1:8000/')
        assert "Icesi Sistema Freya" in driver.title
        btn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/button[1]')
        btn.click()
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/div[3]/button')
        username.send_keys('31764131')
        password.send_keys('Ellider123')
        login.click()
        assert "http://127.0.0.1:8000/index/" in driver.current_url

        btn = driver.find_element(By.XPATH, '//*[@id="ceremony"]/label/span')
        btn.click()

        activity = driver.find_element(By.XPATH, '//*[@id="id_title"]')
        activity.send_keys('Iniciacion de ceremonia')

        send2 = driver.find_element(By.XPATH, '/html/body/div[3]/div/form[1]/button')
        send2.click()

        act = driver.find_element(By.XPATH, '/html/body/div[3]/div/ul/li')
        assert "Planificación de Ceremonias" in driver.title

    def test_ceremony_manager_reset(self):
        """Test ceremony manager resetting ceremony."""
        driver = self._get_webdriver()
        driver.get('http://127.0.0.1:8000/')
        assert "Icesi Sistema Freya" in driver.title
        btn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/button[1]')
        btn.click()
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/form/div[3]/button')
        username.send_keys('31764131')
        password.send_keys('Ellider123')
        login.click()
        assert "http://127.0.0.1:8000/index/" in driver.current_url

        btn = driver.find_element(By.XPATH, '//*[@id="ceremony"]/label/span')
        btn.click()

        reset = driver.find_element(By.XPATH, '/html/body/div[3]/div/form[2]/button')
        reset.click()

        date = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/p[1]')
        assert "Jan. 1, 2024" in date.text
