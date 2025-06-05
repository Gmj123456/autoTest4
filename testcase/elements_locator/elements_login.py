from selenium.webdriver.common.by import By

class LoginElements:
    USERNAME_INPUT = (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[1]/div/div/span/input")
    PASSWORD_INPUT = (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[2]/div/div/span/input")
    CAPTCHA_INPUT = (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[3]/div[1]/div/div/div/span/span/input")
    CAPTCHA_IMAGE = (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/form/div[1]/form/div[3]/div[2]/img")
    LOGOUT_BUTTON = (By.XPATH, "//*[@id='app']/section/section/header/div/div/span[6]/a/span/span/span")
    CONFIRM_LOGOUT_BUTTON = (By.CSS_SELECTOR, "body > div:nth-child(17) > div > div.ant-modal-wrap > div > div.ant-modal-content > div > div > div.ant-modal-confirm-btns > button.ant-btn.ant-btn-primary")
    NOTIFICATION_CLOSE_BUTTON = (By.CSS_SELECTOR, "body > div.ant-notification.ant-notification-topRight > span > div > a > span > i > svg")