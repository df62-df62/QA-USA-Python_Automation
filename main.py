import data
import helpers
import time
from helpers import retrieve_phone_code
from pages import UrbanRoutesPage  # Import the POM class
from selenium import webdriver

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.routes_page = UrbanRoutesPage(cls.driver)
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")
        cls.driver.get(data.URBAN_ROUTES_URL)

    def test_set_route(self):
        from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        assert from_text == data.ADDRESS_FROM
        to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        assert to_text == data.ADDRESS_TO

    def test_select_plan(self):
        #from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        #assert from_text == data.ADDRESS_FROM
        #to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        #assert to_text == data.ADDRESS_TO

        self.routes_page.click_call_a_taxi()
        sup_plan_element = self.routes_page.click_supportive_plan()
        assert "active" in sup_plan_element
        time.sleep(3)

    def test_fill_phone_number(self):
        self.routes_page.click_enter_phone_number()
        self.routes_page.enter_phone_number(data.PHONE_NUMBER)
        self.routes_page.click_next()
        sms_num = retrieve_phone_code(self.driver)
        self.routes_page.enter_the_sms(sms_num)
        self.routes_page.click_confirm()
        assert self.driver.find_element(*self.routes_page.PHONE_NUMBER_LOCATOR).text == data.PHONE_NUMBER
        time.sleep(3)


    def test_fill_card(self):
        self.routes_page.click_payment_method()
        self.routes_page.click_add_card()
        self.routes_page.enter_card_number(data.CARD_NUMBER)
        self.routes_page.enter_cc_code(data.CARD_CODE)
        assert "button full" in self.driver.find_element(*self.routes_page.LINK_BUTTON_LOCATOR).get_attribute("class")
        self.routes_page.click_link_button()
        self.routes_page.click_exit_cc()
        assert "Card" in self.driver.find_element(*self.routes_page.PM_TEXT_LOCATOR).text

    def test_comment_for_driver(self):
        driver_message = self.routes_page.enter_message_to_driver(data.MESSAGE_FOR_DRIVER)
        assert driver_message == data.MESSAGE_FOR_DRIVER
        time.sleep(3)

    def test_order_blanket_and_handkerchiefs(self):
        self.routes_page.blanket_and_handkerchiefs_order()
        time.sleep(3)

    def test_order_2_ice_creams(self):
        num_of_icecream = self.routes_page.ordering_ice_cream()
        assert num_of_icecream == 2

    def test_car_search_model_appears(self):
        self.routes_page.order_finalized()
        time.sleep(30)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()