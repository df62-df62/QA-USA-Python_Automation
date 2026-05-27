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
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")



    def test_set_route(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)
        from_text = routes_page.set_from_location(data.ADDRESS_FROM)
        to_text = routes_page.set_to_location(data.ADDRESS_TO)
        assert from_text == data.ADDRESS_FROM
        assert to_text == data.ADDRESS_TO

    def test_select_plan(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page.set_from_location(data.ADDRESS_FROM)
        routes_page.set_to_location(data.ADDRESS_TO)
        routes_page.click_call_a_taxi()
        sup_plan_element = routes_page.click_supportive_plan()
        assert "Supportive" in sup_plan_element

    def test_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page.set_from_location(data.ADDRESS_FROM)
        routes_page.set_to_location(data.ADDRESS_TO)
        routes_page.click_call_a_taxi()
        routes_page.click_supportive_plan()
        routes_page.click_enter_phone_number()
        routes_page.enter_phone_number(data.PHONE_NUMBER)
        routes_page.click_next()
        sms_num = retrieve_phone_code(self.driver)
        routes_page.enter_the_sms(sms_num)
        routes_page.click_confirm()
        phone_value = routes_page.get_current_phone_number()
        assert phone_value == data.PHONE_NUMBER

    def test_fill_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page.set_from_location(data.ADDRESS_FROM)
        routes_page.set_to_location(data.ADDRESS_TO)
        routes_page.click_call_a_taxi()
        routes_page.click_supportive_plan()
        routes_page.click_payment_method()
        routes_page.click_add_card()
        routes_page.enter_card_number(data.CARD_NUMBER)
        routes_page.enter_cc_code(data.CARD_CODE)
        routes_page.click_link_button()
        routes_page.click_exit_cc()
        assert "Card" in routes_page.pm_text_fetch()

    def test_comment_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page.set_from_location(data.ADDRESS_FROM)
        routes_page.set_to_location(data.ADDRESS_TO)
        routes_page.click_call_a_taxi()
        routes_page.click_supportive_plan()
        driver_message = routes_page.enter_message_to_driver(data.MESSAGE_FOR_DRIVER)
        assert driver_message == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page.set_from_location(data.ADDRESS_FROM)
        routes_page.set_to_location(data.ADDRESS_TO)
        routes_page.click_call_a_taxi()
        routes_page.click_supportive_plan()
        time.sleep(1)
        b_and_h_prop = routes_page.blanket_and_handkerchiefs_order()
        assert b_and_h_prop

    def test_order_2_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page.set_from_location(data.ADDRESS_FROM)
        routes_page.set_to_location(data.ADDRESS_TO)
        routes_page.click_call_a_taxi()
        routes_page.click_supportive_plan()
        time.sleep(1)
        num_of_icecream = routes_page.ordering_ice_cream()
        assert num_of_icecream == 2

    def test_car_search_model_appears(self):
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page.set_from_location(data.ADDRESS_FROM)
        routes_page.set_to_location(data.ADDRESS_TO)
        routes_page.click_call_a_taxi()
        routes_page.click_supportive_plan()
        routes_page.click_enter_phone_number()
        routes_page.enter_phone_number(data.PHONE_NUMBER)
        routes_page.click_next()
        sms_num = retrieve_phone_code(self.driver)
        routes_page.enter_the_sms(sms_num)
        routes_page.click_confirm()
        routes_page.enter_message_to_driver(data.MESSAGE_FOR_DRIVER)
        order_modal = routes_page.order_finalized()
        assert order_modal

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
