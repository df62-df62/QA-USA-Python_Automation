from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
import time
import re

class UrbanRoutesPage:
    FROM_LOCATOR = (By.ID,'from')
    TO_LOCATOR = (By.ID,'to')
    CALL_A_TAXI_LOCATOR = (By.XPATH, '//button[text()="Call a taxi"]')
    SUPPORTIVE_PLAN_LOCATOR = (By.XPATH, '//div[contains(@class, "tcard-title") and text()="Supportive"]/..')
    SUPPORTIVE_PLAN_PRICE_LOCATOR = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-price"]')
    PHONE_NUMBER_LOCATOR = (By.XPATH, '//div[@class="np-text"]')
    ENTER_PHONE_NUMBER_LOCATOR = (By.ID, "phone")
    NEXT_LOCATOR = (By.XPATH, '//button[text()="Next"]')
    SMS_LOCATOR = (By.ID, 'code')
    CONFIRM_LOCATOR = (By.XPATH, '//button[text()="Confirm"]')
    PAYMENT_METHOD_LOCATOR = (By.XPATH, '//div[@class="pp-text"]')
    PM_TEXT_LOCATOR = (By.XPATH, '//div[@class="pp-value-text"]')
    ADD_CARD_LOCATOR = (By.XPATH, '//div[text()="Add card"]')
    CARD_NUMBER_LOCATOR = (By.ID, 'number')
    CC_CODE_LOCATOR = (By.ID, 'code')
    CC_CLICK_LOCATOR = (By.XPATH, '//div[@class="card-code-input"]')
    LINK_BUTTON_LOCATOR = (By.XPATH, '//button[text()="Link"]')
    EXIT_CC_LOCATOR = (By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    MESSAGE_TO_DRIVER_LOCATOR = (By.ID, 'comment')
    BLANKET_AND_HANDKERCHIEF_LOCATOR = (By.XPATH, '//div[@class="r-sw-container"]//div[@class="r-sw"]')
    BLANKET_AND_HANDKERCHIEF_CHECK = (By.XPATH, '//div[@class="r-sw-container"]//div[@class="r-sw"]//input[@type="checkbox"]')
    ICE_CREAM_LOCATOR = (By.XPATH, '//div[@class="r-counter-container"]//div[@class="r-counter-label"][text()="Ice cream"]/following-sibling::div[@class="r-counter"]//div[@class="counter-plus"]')
    ICE_CREAM_COUNTER = (By.XPATH, '//div[@class="r-counter-container"]//div[@class="r-counter-label"][text()="Ice cream"]/following-sibling::div[@class="r-counter"]//div[@class="counter-value"]')
    ORDER_LOCATOR = (By.XPATH, '//button[@class="smart-button"]')
    CAR_SEARCH_MODAL_LOCATOR = (By.XPATH, '//div[@class="order-body"]')

    def __init__(self, driver):
        self.driver = driver  # Initialize the driver

    def set_from_location(self, from_text):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "from"))
        )
        self.driver.find_element(*self.FROM_LOCATOR).send_keys(from_text)
        from_value = self.driver.find_element(*self.FROM_LOCATOR).get_attribute("value")
        return from_value

    def set_to_location(self, to_text):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "to"))
        )
        self.driver.find_element(*self.TO_LOCATOR).send_keys(to_text)
        to_value = self.driver.find_element(*self.TO_LOCATOR).get_attribute("value")
        return to_value

    def click_call_a_taxi(self):
        self.driver.find_element(*self.CALL_A_TAXI_LOCATOR).click()

    def click_supportive_plan(self):
        supp_plan_element = self.driver.find_element(*self.SUPPORTIVE_PLAN_LOCATOR)
        supp_plan_element.click()
        supp_plan_attr = supp_plan_element.get_attribute("class")
        return supp_plan_attr

    def click_enter_phone_number(self):
        self.driver.find_element(*self.PHONE_NUMBER_LOCATOR).click()

    def enter_phone_number(self, phone_text):
        self.driver.find_element(*self.ENTER_PHONE_NUMBER_LOCATOR).send_keys(phone_text)

    def click_next(self):
        self.driver.find_element(*self.NEXT_LOCATOR).click()

    def enter_the_sms(self, sms_code):
        self.driver.find_element(*self.SMS_LOCATOR).send_keys(sms_code)

    def click_confirm(self):
        self.driver.find_element(*self.CONFIRM_LOCATOR).click()

    def click_payment_method(self):
        self.driver.find_element(*self.PAYMENT_METHOD_LOCATOR).click()

    def click_add_card(self):
        self.driver.find_element(*self.ADD_CARD_LOCATOR).click()

    def enter_card_number(self, card_number):
        self.driver.find_element(*self.CARD_NUMBER_LOCATOR).send_keys(card_number, Keys.TAB)

    def enter_cc_code(self, cc_code):
        #WebDriverWait(self.driver, 10).until(
        #    EC.element_to_be_clickable((By.ID, 'code'))
        #)
        #self.driver.find_element(*self.CC_CODE_LOCATOR).click()
        active_field =self.driver.switch_to.active_element
        active_field.send_keys(cc_code)
        active_field.send_keys(Keys.TAB)
        time.sleep(1)
        #arguments[0].value = arguments[1];", element, cc_code)
        #self.driver.execute_script("arguments[0].blur();", element)

    def click_link_button(self):
        self.driver.find_element(*self.LINK_BUTTON_LOCATOR).click()

    def click_exit_cc(self):
        #exit_cc = WebDriverWait(self.driver, 10).until(
        #    EC.element_to_be_clickable((By.XPATH, '//button[@class="close-button section-close"]'))
        #)
        self.driver.find_element(*self.EXIT_CC_LOCATOR).click()
        time.sleep(3)
        #self.driver.execute_script("arguments[0].click();", exit_element)

    def enter_message_to_driver(self, driver_message_text):
        self.driver.find_element(*self.MESSAGE_TO_DRIVER_LOCATOR).send_keys(driver_message_text)
        message_for_driver = self.driver.find_element(*self.MESSAGE_TO_DRIVER_LOCATOR).get_attribute("value")
        return message_for_driver

    def blanket_and_handkerchiefs_order(self):
            self.driver.find_element(*self.BLANKET_AND_HANDKERCHIEF_LOCATOR).click()
            assert self.driver.find_element(*self.BLANKET_AND_HANDKERCHIEF_CHECK).get_property('checked')

    def ordering_ice_cream(self):
        for i in range(2):
            self.driver.find_element(*self.ICE_CREAM_LOCATOR).click()
            print(f"Ice cream order {i + 1}")
            time.sleep(1)

        ice_cream_counter = self.driver.find_element(*self.ICE_CREAM_COUNTER).text
        ice_cream_amount = int(ice_cream_counter)
        return ice_cream_amount

    def order_finalized(self):
        self.driver.find_element(*self.ORDER_LOCATOR).click()
        assert self.driver.find_element(*self.CAR_SEARCH_MODAL_LOCATOR).is_displayed()