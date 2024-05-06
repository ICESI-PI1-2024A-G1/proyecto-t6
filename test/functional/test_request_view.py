from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


class LiveServerTestCase(LiveServerTestCase):

    def scrap(self):
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
        return driver

    def testRequest_correct(self):
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
        rbtn = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[1]/a')
        rbtn.click()
        titulo = driver.find_element(By.NAME, "titulo")
        descripcion = driver.find_element(By.NAME, "descripcion")
        lugar = driver.find_element(By.NAME, "lugar")
        fecha_inicio = driver.find_element(By.NAME, "fecha_inicio")
        fecha_fin = driver.find_element(By.NAME, "fecha_fin")
        presupuesto = driver.find_element(By.NAME, "presupuesto")
        alimentacion = driver.find_element(By.NAME, "alimentacion")
        transporte = driver.find_element(By.NAME, "transporte")
        profesor = Select(driver.find_element(By.NAME, "profesor"))

        titulo.send_keys('Bienes - B')
        descripcion.send_keys('Manejo de bienes')
        lugar.send_keys('Edificio B')
        fecha_inicio.send_keys('01-01-2024')
        fecha_fin.send_keys('01-02-2024')
        presupuesto.send_keys(150000)
        alimentacion.send_keys('No')
        transporte.send_keys('No')
        profesor.select_by_value('1')

        ebtn = driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div/form/button')
        ebtn.click()
        assert "http://127.0.0.1:8000/create-event-request/" in driver.current_url

    def testRequest_correct_noProfessor(self):
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
        username.send_keys('1006229942')
        password.send_keys('Redrobin5')
        login.click()
        assert "http://127.0.0.1:8000/index/" in driver.current_url
        rbtn = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[1]/a')
        rbtn.click()
        titulo = driver.find_element(By.NAME, "titulo")
        descripcion = driver.find_element(By.NAME, "descripcion")
        lugar = driver.find_element(By.NAME, "lugar")
        fecha_inicio = driver.find_element(By.NAME, "fecha_inicio")
        fecha_fin = driver.find_element(By.NAME, "fecha_fin")
        presupuesto = driver.find_element(By.NAME, "presupuesto")
        alimentacion = driver.find_element(By.NAME, "alimentacion")
        transporte = driver.find_element(By.NAME, "transporte")

        titulo.send_keys('Bienes - B')
        descripcion.send_keys('Manejo de bienes')
        lugar.send_keys('Edificio B')
        fecha_inicio.send_keys('01-01-2024')
        fecha_fin.send_keys('01-02-2024')
        presupuesto.send_keys(150000)
        alimentacion.send_keys('No')
        transporte.send_keys('No')

        ebtn = driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div/form/button')
        ebtn.click()
        assert "http://127.0.0.1:8000/create-event-request/" in driver.current_url

    def testRequest_Noprofessor_BadTime(self):
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
        username.send_keys('1006229942')
        password.send_keys('Redrobin5')
        login.click()
        assert "http://127.0.0.1:8000/index/" in driver.current_url
        rbtn = driver.find_element(By.XPATH, '//*[@id="sidebar"]/ul/li[1]/a')
        rbtn.click()
        titulo = driver.find_element(By.NAME, "titulo")
        descripcion = driver.find_element(By.NAME, "descripcion")
        lugar = driver.find_element(By.NAME, "lugar")
        fecha_inicio = driver.find_element(By.NAME, "fecha_inicio")
        fecha_fin = driver.find_element(By.NAME, "fecha_fin")
        presupuesto = driver.find_element(By.NAME, "presupuesto")
        alimentacion = driver.find_element(By.NAME, "alimentacion")
        transporte = driver.find_element(By.NAME, "transporte")

        titulo.send_keys('Bienes - B')
        descripcion.send_keys('Manejo de bienes')
        lugar.send_keys('Edificio B')
        fecha_inicio.send_keys('01-01-2024')
        fecha_fin.send_keys('01-01-2023')
        presupuesto.send_keys(150000)
        alimentacion.send_keys('No')
        transporte.send_keys('No')

        ebtn = driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div/form/button')
        ebtn.click()
        error = driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div/form/ul/li')
        print(error.text)
        assert error.is_displayed

    def testRequestManager_aprove(self):
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

        driver.get('http://127.0.0.1:8000/event-requests/')

        estado = Select(driver.find_element(
            By.XPATH, '/html/body/div[4]/div/table/tbody/tr[1]/td[12]/form/select'))

        estado.select_by_value('Aprobada')

        ebtn = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/table/tbody/tr[1]/td[12]/form/button')
        ebtn.click()
        assert "http://127.0.0.1:8000/event-requests/" in driver.current_url

    def testRequestManager_deny(self):
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

        driver.get('http://127.0.0.1:8000/event-requests/')

        estado = Select(driver.find_element(
            By.XPATH, '/html/body/div[4]/div/table/tbody/tr[1]/td[12]/form/select'))

        estado.select_by_value('Rechazada')

        ebtn = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/table/tbody/tr[1]/td[12]/form/button')
        ebtn.click()
        assert "http://127.0.0.1:8000/event-requests/" in driver.current_url

    def testRequestManager_pend(self):
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

        driver.get('http://127.0.0.1:8000/event-requests/')

        estado = Select(driver.find_element(
            By.XPATH, '/html/body/div[4]/div/table/tbody/tr[1]/td[12]/form/select'))

        estado.select_by_value('Pendiente')

        ebtn = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/table/tbody/tr[1]/td[12]/form/button')
        ebtn.click()
        assert "http://127.0.0.1:8000/event-requests/" in driver.current_url
