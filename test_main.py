import data
import helpers
import time
from helpers import retrieve_phone_code
from pages import UrbanRoutesPage  # Import the POM class
from selenium import webdriver


class TestUrbanRoutes:
    @classmethod
    def setup_method(cls):
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

    # Setting the addresses
    def test_set_route(self):
        from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        assert from_text == data.ADDRESS_FROM
        to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        assert to_text == data.ADDRESS_TO

    def test_select_plan(self):
        from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        self.routes_page.click_call_a_taxi()
        sup_plan_element = self.routes_page.click_supportive_plan()
        assert "Supportive" in sup_plan_element

    def test_fill_phone_number(self):
        from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        self.routes_page.click_call_a_taxi()
        sup_plan_element = self.routes_page.click_supportive_plan()
        self.routes_page.click_enter_phone_number()
        self.routes_page.enter_phone_number(data.PHONE_NUMBER)
        self.routes_page.click_next()
        sms_num = retrieve_phone_code(self.driver)
        self.routes_page.enter_the_sms(sms_num)
        self.routes_page.click_confirm()
        phone_value = self.routes_page.get_current_phone_number()
        assert phone_value == data.PHONE_NUMBER

    def test_fill_card(self):
        from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        self.routes_page.click_call_a_taxi()
        sup_plan_element = self.routes_page.click_supportive_plan()
        self.routes_page.click_payment_method()
        self.routes_page.click_add_card()
        self.routes_page.enter_card_number(data.CARD_NUMBER)
        self.routes_page.enter_cc_code(data.CARD_CODE)
        assert "button full" in self.routes_page.link_button_active()
        self.routes_page.click_link_button()
        self.routes_page.click_exit_cc()
        assert "Card" in self.routes_page.pm_text_fetch()

    def test_comment_for_driver(self):
        from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        self.routes_page.click_call_a_taxi()
        sup_plan_element = self.routes_page.click_supportive_plan()
        driver_message = self.routes_page.enter_message_to_driver(data.MESSAGE_FOR_DRIVER)
        assert driver_message == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        self.routes_page.click_call_a_taxi()
        sup_plan_element = self.routes_page.click_supportive_plan()
        time.sleep(1)
        b_and_h_prop = self.routes_page.blanket_and_handkerchiefs_order()
        assert b_and_h_prop

    def test_order_2_ice_creams(self):
        from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        self.routes_page.click_call_a_taxi()
        sup_plan_element = self.routes_page.click_supportive_plan()
        time.sleep(1)
        num_of_icecream = self.routes_page.ordering_ice_cream()
        assert num_of_icecream == 2

    def test_car_search_model_appears(self):
        from_text = self.routes_page.set_from_location(data.ADDRESS_FROM)
        to_text = self.routes_page.set_to_location(data.ADDRESS_TO)
        self.routes_page.click_call_a_taxi()
        sup_plan_element = self.routes_page.click_supportive_plan()
        self.routes_page.click_enter_phone_number()
        self.routes_page.enter_phone_number(data.PHONE_NUMBER)
        self.routes_page.click_next()
        sms_num = retrieve_phone_code(self.driver)
        self.routes_page.enter_the_sms(sms_num)
        self.routes_page.click_confirm()
        driver_message = self.routes_page.enter_message_to_driver(data.MESSAGE_FOR_DRIVER)
        order_modal = self.routes_page.order_finalized()
        assert order_modal

    @classmethod
    def teardown_method(cls):
        cls.driver.quit()
