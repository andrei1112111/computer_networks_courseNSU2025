from selenium import webdriver


driver_path = '/path/to/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)
driver.get('https://www.example.com/form')

username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')
submit_button = driver.find_element_by_xpath('//button[@type="submit"]')

username.send_keys('my_username')
password.send_keys('my_password')
submit_button.click()
