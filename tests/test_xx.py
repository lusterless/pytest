import pytest
from selenium import webdriver

from selenium.webdriver.firefox.service import Service as Firefox_Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    """
    setup of browser, to be passed in for each ui test
    """
    # setup
    options = Options()
    options.headless = True # False for non-headless
    s = Firefox_Service(GeckoDriverManager().install())
    browser = webdriver.Firefox(service=s, options=options)
    
    # return when completed
    yield browser


def test_http(browser):
    # setup
    """
    PLACEHOLDER / TO BE DELETED
    """
    wait = WebDriverWait(browser, 10)
    browser.get("http://apptest:5000")
#     wait.until(EC.title_is("127.0.0.1:5000"))

    # check for https connection
    assert "http" in browser.current_url
    browser.close()

# def test_https(browser):
#     # setup
#     wait = WebDriverWait(browser, 10)
#     browser.get("http://apptest:5000")
#     wait.until(EC.title_is("Home - BAGATEA"))
#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn")))
#     verify = browser.find_element(By.CSS_SELECTOR, ".btn")

#     # check for https connection
#     assert "https" in browser.current_url
#     assert 'Signup' in verify.text
#     browser.close()

# def test_otp_bruteforce(browser):
#     # setup
#     wait = WebDriverWait(browser, 10)
#     browser.get("http://apptest:5000/en/account/login")
#     browser.implicitly_wait(3)
#     wait.until(EC.presence_of_element_located((By.ID, "email")))
#     wait.until(EC.presence_of_element_located((By.ID, "password")))
#     wait.until(EC.presence_of_element_located((By.ID, "submit")))

#     #fill up login form with legitimate credentials
#     username = browser.find_element(By.ID, 'email')
#     password = browser.find_element(By.ID, 'password')

#     username.send_keys("test.bagatea2021@gmail.com")
#     password.send_keys("B@8aTe@SIT1346798250")
#     submit = browser.find_element(By.ID, 'submit')
#     submit.click()

#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert")))
#     something = browser.find_element(By.CSS_SELECTOR, ".alert")
#     otp_timeout = int(settings.OTP_LOGIN_MAX_TIMEOUT / 60)
#     if 'Authentication Failed.' in something.text:
#         with pytest.raises(Exception):
#             raise Exception('Testing account is banned. Test is invalid.')

#     elif f'OTP has been sent to your email. Please key in within {otp_timeout} minutes' in something.text:
#         # enter the wrong otp for 5 times
#         try:
#             i = 1
#             while i < 6:
#                 wait.until(EC.presence_of_element_located((By.ID, "otp")))
#                 otp = browser.find_element(By.ID, "otp")
#                 otp.send_keys("AAAAAAAA")
#                 otpsubmit = browser.find_element(By.ID, 'submit')
#                 otpsubmit.click()
#                 i += 1

#             # assert that user is banned
#             result = browser.find_element(By.CSS_SELECTOR, ".alert")
#             assert 'User has reached max tries for OTP generation and is banned.' in result.text
#             browser.close()
#         except Exception as e:
#             print(str(e) + "Testing account is banned.")
#             browser.close()
