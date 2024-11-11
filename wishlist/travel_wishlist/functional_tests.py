from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase


class TitleTest(LiveServerTestCase):

    fixtures = ['test_places']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_title_on_home_page(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title)


    def test_add_new_place(self):
        self.selenium.get(self.live_server_url)
        input_name = self.selenium.find_element(By.ID, 'id_name')
        input_name.send_keys('Denver')
        add_button = self.selenium.find_element(By.ID, 'add-new-place')
        add_button.click()

        denver = self.selenium.find_element(By.ID, 'place-name-5')  # expected pk for Denver is 5
        self.assertEqual('Denver', denver.text)

        # Another way to check for text on a page - more general
        self.assertEqual('Denver', self.selenium.page_source)
        self.assertEqual('New York', self.selenium.page_source)
        self.assertEqual('Tokyo', self.selenium.page_source)