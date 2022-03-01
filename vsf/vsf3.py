import random
import threading
from multiprocessing import Process
# import undetected_chromedriver.v2 as uc
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#from proxylist import get_free_proxy # list of freeproxy

#for dropdown selection
from selenium.webdriver.support.ui import Select

# for email otp
#from otp import GmailOtp
#from .otp_outlook import Realotp

import time
# for recaptcha solution
# import urllib
# import os
import requests

from .capsolution import CapSolution


# for file reading and writing
# import pandas
# import csv
# inputfile = 'vsfinput.csv' # all these things goes to external file
from .reading import ReadWrite #to read inputed file
from .output import write_result, write_origin

# for solution of hcaptcha
from .hcapsol import HcapSolution

# gcapsol with 2captch
from .test import gcapresponse



class Appointment():
    # for proxy
    # proxy_list = get_free_proxy()
    # PROXY = random.choice(proxy_list)
    # PROXY = '115.42.0.186:53281'
    # PROXY = '198.229.231.13:8080'
    # print(PROXY)
    # webdriver.DesiredCapabilities.CHROME['proxy'] = {
    #     "httpProxy": PROXY,
    #     "sslProxy": PROXY,
    #     "proxyType": "MANUAL",
    #
    # }





    # options = uc.ChromeOptions()
    service_obj = Service(ChromeDriverManager().install())
    options = Options()

    # ua = UserAgent()
    # userAgent = ua.random
    # userAgent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    # options.add_argument(f'user-agent={userAgent}')
    # options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"')

    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # one
    options.add_experimental_option('useAutomationExtension', False)  # two
    options.add_argument('--disable-blink-features=AutomationControlled')  # three  these three option is called "Removing Navigator.Webdriver Flag"
    options.add_argument('--disable-notifications')  # one this is to stop showing notificationn like "Save password" (working)
    prefs = {"profile.default_content_setting_values.notifications": 2}  # two
    options.add_experimental_option("prefs",prefs)  # three above three lines of code ignoring the "Save password" popup from chrome (called browser notifictaion)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--user-data-dir=C:\\Users\\City\\AppData\\Local\\Google\\Chrome\\User Data") # this will open browser from your default browser


    def __init__(self):
        # self.driver = webdriver.Chrome(service=self.service_obj)
        pass


    def delay(self):
        time.sleep(random.randint(2, 4))

    def wait60sec(self, driver):
        driver.implicitly_wait(60)


    def write_output(self, data):
        output = write_result(data)
        return output

    def update_orgin(self):
        data = self.user_list
        write_origin(data)


    def read_csv(self):
        read = ReadWrite()
        self.user_list = read.data_list
        read.read_data()

    def solution_cap(self, driver):
        capsul = CapSolution()
        capsul.capthasolution(driver)

    
    # def gcapsol(self):
    #     result = gcapresponse()
    #     return result

    # def gmail_otp(self, email, passw):
    #     '''this method supposed to fetch otp from gmail'''
    #     otp = Realotp()
    #     otp_int = otp.outlook_otp(email, passw)
    #     print('in first f '+ otp_int)
    #     return otp_int


    def click_on_image(self, driver, header_text):
        ''' this method supposed  to click on hcaptcha images'''
        wrapper_list = driver.find_elements(By.XPATH, "//div[@class='task-image']")

        for wrapper in wrapper_list:
            img_url = wrapper.find_element(By.XPATH, ".//div[@class='image-wrapper']/div[@class='image']")  # .value_of_css_property('background'))
            absolute_url = img_url.value_of_css_property('background').lstrip('url(&quot;').rstrip(';) 50% 50% / 123.333px 123.333px no-repeat;')
            ls = absolute_url.lstrip('gba(0, 0, 0, 0) url("')
            rs = ls.rstrip('") no-repeat scroll 50% 50% / 123.333px 123.333px padding-box border-b')
            if header_text == 'bus' or header_text == 'river':
                if '==' in rs:
                    wrapper.click()
                    time.sleep(3)
            else:
                if '=' not in rs:
                    wrapper.click()
                    time.sleep(3)


    def hcapsolution(self, driver):
        '''this is the method to solve hcaptcha'''
        # capsol = HcapSolution()
        # capsol.runhcap(driver)
        self.delay()
        driver.implicitly_wait(2)
        iframe = driver.find_element(By.XPATH, "//div[@id='cf-hcaptcha-container']/div/following-sibling::div/iframe[@title='widget containing checkbox for hCaptcha security challenge']")
        driver.switch_to.frame(iframe)
        self.delay()
        time.sleep(2)
        check_box = driver.find_element(By.XPATH, "//div[@id='checkbox']")
        check_box.click() # clicked on the check box of hcaptcha
        time.sleep(5)
        # switch to iframe of hcaptcha image content(main content)
        driver.switch_to.default_content()
        iframe_image = driver.find_elements(By.XPATH, "//iframe[@title='Main content of the hCaptcha challenge']")[1]
        driver.switch_to.frame(iframe_image) # switched to the captcha image content
        driver.implicitly_wait(5)
        self.delay()
        header_text = driver.find_element(By.XPATH, "//div[@class='prompt-text']").text.strip().split(' ')[-1].strip()
        print(header_text)
        self.delay()
        self.click_on_image(driver, header_text)

        #value_of_css_property("background-image")
        # bg_url = div.value_of_css_property('background-image')  # 'url("https://i.xxxx.com/img.jpg")'
        # # strip the string to leave just the URL part
        # bg_url = bg_url.lstrip('url("').rstrip('")')
        # https://i.xxxx.com/img.jpg

        time.sleep(3)
        next_challenge = driver.find_element(By.XPATH, "//div[@title='Next Challenge']")
        next_challenge.click()
        driver.implicitly_wait(5)
        self.delay()
        self.click_on_image(driver, header_text)
        driver.implicitly_wait(5)
        self.delay()
        verify_button = driver.find_element(By.XPATH, "//div[@title='Submit Answers']")
        verify_button.click()
        time.sleep(5)


        # Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36


    def primary_selection(self, centre, appointment_category, driver):
        '''This method for selection center, appointment category'''
        #need to select visiting country and residence

        # starting selection of Center and Appointment category
        self.delay()
        # here you will get a pop up to save pass if it is seems a browser with no detection
        # driver.switch_to.alert.dismiss() # not working because that was not a alert button rather a popup
        # driver.switch_to_alert().dismiss()
        time.sleep(2)

        center_selection = Select(driver.find_element(By.XPATH, "//select[@id='LocationId']"))
        center_selection.select_by_value(centre)
        self.wait60sec(driver)
        self.delay()
        time.sleep(2)
        category_selection = Select(driver.find_element(By.XPATH, "//select[@id='VisaCategoryId']"))
        category_selection.select_by_value(appointment_category)

        #click on continue button
        driver.implicitly_wait(10)
        time.sleep(3)
        driver.find_element(By.XPATH, "//input[@id='btnContinue']").click() #this is the continue button in the first page
        # now if field validation needed
        try:
            time.sleep(2)
            field_valid = driver.find_elements(By.XPATH, "//span[@class='field-validation-error']")[-1].text.strip()
            driver.find_element(By.XPATH, "//input[@id='btnContinue']").click()  # this is the continue button in the first page
        except:
            print('no field validation error')
        self.delay()
        #next page loading
        # now click on Add Customer button
        self.wait60sec(driver)
        driver.find_element(By.XPATH, "//a[@class='submitbtn']").click() #this is the the add customer button
        driver.implicitly_wait(3)

        # now it is time to solve hcaptcha
        while True:
            driver.implicitly_wait(5)
            self.delay()
            try:
                self.hcapsolution(driver)
            except:
                print('captcha solved')
                break;

        driver.switch_to.default_content()
        # after this step go to add customer form fill


    def addcustomer(self, passport,
                     # confirmpassport,
                     birthdate,
                     passportexpiration,
                     nationality,
                     firstname,
                     lastname,
                     gender,
                     countrycode,
                     mobile,
                     email, driver):
                     # housenumber,
                     # streetAddress1,
                     # streetAddress2,
                     # postalcode):
        '''this method working to add all information in the page of add customer and will click to continue button'''
        self.reference_number = ''
        driver.implicitly_wait(10)
        self.delay()
        driver.find_element(By.XPATH, "//input[@id='PassportNumber']").send_keys(passport)
        #There is no passport form element regarding otp
        # self.driver.find_element(By.XPATH, "//input[@id='ConfirmPassportNumber']").send_keys(confirmpassport)
        driver.find_element(By.XPATH, "//input[@id='DateOfBirth']").send_keys(birthdate)
        driver.find_element(By.XPATH, "//input[@id='PassportExpiryDate']").send_keys(passportexpiration)

        # select nationality
        Select(driver.find_element(By.XPATH, "//select[@id='NationalityId']")).select_by_value(nationality)

        #input name
        first_name = driver.find_element(By.XPATH, "//input[@id='FirstName']")
        first_name.clear()
        first_name.send_keys(firstname)
        last_name = driver.find_element(By.XPATH, "//input[@id='LastName']")
        last_name.clear()
        last_name.send_keys(lastname)


        #select gender
        Select(driver.find_element(By.XPATH, "//select[@id='GenderId']")).select_by_value(gender)

        #input phone and email
        country_code = driver.find_element(By.XPATH, "//input[@class='form-control phcode-input_field']")
        country_code.clear()
        country_code.send_keys('+' + countrycode)
        mobile_number = driver.find_element(By.XPATH, "//input[@id='Mobile']")
        mobile_number.clear()
        mobile_number.send_keys(mobile)
        email_field = driver.find_element(By.XPATH, "//input[@id='validateEmailId']")
        email_field.clear()
        email_field.send_keys(email)


        #click on submit button
        self.delay()
        driver.find_element(By.XPATH, "//input[@id='submitbuttonId']").click()

        # click on alert popup
        self.wait60sec(driver)
        self.delay()
        time.sleep(2)
        driver.switch_to.alert.accept()

        #from here it will goes to OTP .. now take reference numbar and click on sent OTP button

        # february 2022... at the beginning otp option has gone so below code should dow something else

        driver.switch_to.default_content()
        driver.implicitly_wait(10)
        self.delay()
        # reference number
        self.reference_number += driver.find_element(By.XPATH, "//div[@class='mandatory-txt']/label/b").text.strip()
        print(self.reference_number)

        # submit button to click to move forward
        driver.find_element(By.XPATH, "//input[@type='submit']").click()


        # driver.find_element(By.XPATH, "//input[@type='submit']").click() #sent otp button click
        #
        # # now time to get otp from email via otp module
        # print('Waiting for OTP')
        # time.sleep(60)
        # self.wait60sec(driver)
        # try:
        #     otp = self.gmail_otp(email, passw)
        #     if otp == False:
        #         print('Trying to resent otp')
        #         time.sleep(3)
        #         driver.find_element(By.XPATH, "//input[@value='Regenerate OTP']").click()  # click to resent button
        #         otp = self.gmail_otp(email, passw)
        #         return otp
        #     else:
        #         print('before apply '+ otp)
        #         return otp
        # except:
        #     print('Customer just added')
        #     return False
            # NOte: I have move to other row of excel if otp verification is not done( from next row to sent otp first time)




    # def email_otp_submission(self, otp, driver):
    #     '''this method will submit the email otp'''
    #     otp_input = driver.find_element(By.XPATH, "//input[@id='OTPe']")
    #     otp_input.send_keys(otp)  # otp input is done here
    #     # now submit
    #     time.sleep(10)
    #     driver.find_element(By.XPATH, "//input[@value='Verify OTP and Continue']").click()


    def pick_date(self, month_1, month_2, month_3, driver):
        self.picked_date = ''
        self.delay()
        # take the reference number
        reference_number = driver.find_element(By.XPATH, "//div[@class='mandatory-txt']/label/b").text.strip()


        #do here
        # click on continue button from value added service page
        driver.find_element(By.XPATH, "//input[@id='btnContinueService']").click() #clicked on continue button
        # go further
        driver.implicitly_wait(5)
        time.sleep(2)
        # month = driver.find_element(By.XPATH, "//input[@id='EarliestAllotedMonth']")
        # driver.execute_script("arguments[0].setAttribute('value', '3')", month)

        # month value from csv file
        # month_1 = 'June 2022'
        # month_2 = 'July 2022'
        # month_3 = 'August 2022'
        month_4 = 'September 2022'



        # now time to select date
        # date selection
        # day_number = available_date_list.find_element(By.XPATH, "/div/div[@class='fc-day-number']").text.strip()
        self.delay()



        month_value = driver.find_element(By.XPATH, "//span[@class='fc-header-title']").text.strip()
        if month_value == month_1 or month_value == month_2 or month_value == month_3 or month_value == month_4:
            available_date_list = driver.find_elements(By.XPATH, "//td[@style='background-color: rgb(188, 237, 145); cursor: pointer;']")[0]
            available_date_list.click()
        else:
            print('No matching for month')
            time.sleep(10)
            # driver need to reload from here again
            # will write origin as False status




        # click on time schedule
        time.sleep(2)
        schedule_list = driver.find_elements(By.XPATH, "//div[@id='TimeBandsDiv']/table/tbody/tr/td")[0]
        schedule_list.click()
        time.sleep(2)


        #click on confirm button
        driver.find_element(By.XPATH, "//input[@id='btnConfirm']").click()
        self.delay()

        # click on alert prompt
        self.wait60sec(driver)
        driver.switch_to.alert.accept()

        # loaded a new page
        # select yes check box
        time.sleep(5)
        self.delay()
        driver.switch_to.default_content()
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH, "//input[@id='ReachVFS']").click() # yes check
        #select accept check box
        driver.find_element(By.XPATH, "//input[@id='IAgree']").click()

        # click on confirm and pay button to continue
        driver.find_element(By.XPATH, "//input[@id='btnConfirm']").click()
        # click on alert prompt
        self.wait60sec(driver)
        driver.switch_to.alert.accept()
        time.sleep(60)


    def paynow(self, zip_code, street, city, state, country, cardholder, cardnumber, expirationmonth, expirationyear, cvvnumber, driver):
        self.delay()
        driver.switch_to.default_content()
        # fill street zip code
        driver.find_element(By.XPATH, "//input[@id='billing_zip']").send_keys(zip_code)
        # fill street address
        driver.find_element(By.XPATH, "//textarea[@id='billing_address1']").send_keys(street)
        # fill street city
        driver.find_element(By.XPATH, "//input[@id='billingcity']").send_keys(city)
        # fill street state
        driver.find_element(By.XPATH, "//input[@id='billingstate']").send_keys(state)
        # select country
        billing_country = Select(driver.find_element(By.XPATH, "//select[@id='billingcountry']"))
        billing_country.select_by_value(country)

        # input card holder Name
        card_holder_name = driver.find_element(By.XPATH, "//input[@id='nameOnCard']")
        card_holder_name.clear()
        card_holder_name.send_keys(cardholder)
        # input card number
        card_number = driver.find_element(By.XPATH, "//input[@id='creditcard_cardNumber']")
        card_number.clear()
        card_number.send_keys(cardnumber)

        # select card expiration
        # month
        card_expiration_month = Select(driver.find_element(By.XPATH, "//select[@id='creditcard_expiryMonth']"))
        card_expiration_month.select_by_value(expirationmonth)
        # year
        card_expiration_year = Select(driver.find_element(By.XPATH, "//select[@id='creditcard_expiryYear']"))
        card_expiration_year.select_by_value(expirationyear)

        # input cvv
        driver.find_element(By.XPATH, "//input[@id='CVV']").send_keys(cvvnumber)

        # here we need to add zip code, address and some more field to forward /  continue payment action
        # Here need to add I agree check box to check (there is no check box like this.. )
        # Now it is time to sleep for 59 minutes
        time.sleep(3540)

        # driver.find_element(By.XPATH, "//button[@id='paySubmit']").click()



    def login(self, user_name, pass_word, driver):
        '''This method is suppose to solve login and login captcha problem'''
        driver.implicitly_wait(2)
        time.sleep(2)
        email = driver.find_element(By.XPATH, "//input[@id='EmailId']")
        print(user_name)
        # email.send_keys('waislam67@gmail.com')
        time.sleep(2)
        email.send_keys(user_name)
        time.sleep(2)
        password = driver.find_element(By.XPATH, "//input[@id='Password']")
        # password.send_keys('H!PBb!@B4CxjQN5')
        time.sleep(2)
        password.send_keys(pass_word)

        #form data mission country name
        mission = driver.find_element(By.XPATH, "//input[@id='Mission']")
        driver.execute_script("arguments[0].setAttribute('value','GJZ8UZVM+guclLYeCIytdQ==')", mission)
        print(mission.get_attribute('value'))
        country = driver.find_element(By.XPATH, "//input[@id='Country']")
        driver.execute_script("arguments[0].setAttribute('value', 'LuPeffehutdAFt+0k6EVBw==')", country)
        print(country.get_attribute('value'))

        self.delay()
        driver.implicitly_wait(5)


        # custom default captcha
        # image_src = self.driver.find_element(By.XPATH, "//img[@id='CaptchaImage']").get_attribute('src')
        # print(image_src)
        # self.default_cap_solution(image_src)

        #google captcha
        # time.sleep(2)
        # textarea = driver.find_element(By.XPATH, "//textarea[@id='g-recaptcha-response']")
        # verify_key = driver.execute_script("arguments[0].style.display = 'inline';", textarea)
        # time.sleep(10)
        # capsol_key = self.gcapsol()
        # textarea.send_keys(capsol_key)
        #
        # time.sleep(2)
        # # now click on submit button
        # submit_button = driver.find_element(By.XPATH, "//div[@class='frm-button']/input")
        # driver.execute_script("arguments[0].style.position = 'absolute';", submit_button)
        # time.sleep(2)
        # submit_button.click()
        # driver.find_element(By.XPATH, "//div[@class='frm-button']/input").click()

        self.solution_cap(driver) # this one is for solving gcapcha done by developer



    def make_schedule(self, centre, appointment_category, driver):
        '''this method is the parent of primary selection'''
        time.sleep(3)
        driver.find_element(By.XPATH, "//ul[@class='leftNav-ul']/descendant::li[1]/a").click() #schedule an appointment
        driver.implicitly_wait(2)
        time.sleep(3)
        self.primary_selection(centre, appointment_category, driver)


    def from_csvreading_to_sent_token(self,
                                      user_name,
                                      pass_word,
                                      centre,
                                      appointment_category,
                                      passport,
                                      birthdate,
                                      passportexpiration,
                                      nationality,
                                      firstname,
                                      lastname,
                                      gender,
                                      countrycode,
                                      mobile,
                                      email, month_1, month_2, month_3,
                                      zip_code, street, city, state, country, cardholder, cardnumber, expirationmonth, expirationyear, cvvnumber):
        '''this method initiated and quite the driver'''
        # driver = webdriver.Chrome(self.service_obj.path, options=self.options)
        # driver.maximize_window()
        # driver = uc.Chrome(options=self.options)
        driver = uc.Chrome()
        driver.maximize_window()

            # self.driver.get('https://row1.vfsglobal.com/GlobalAppointment/Home/Index')

        try:
            self.wait60sec(driver)
            driver.get('https://row1.vfsglobal.com/GlobalAppointment/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/LOSRShyD1pxcML5QC8esmWZOlCfzkBP8joxvSe0zuqEDa7b66mSROQzF6E9izpGMg==')
            # driver.add_cookie({"ASP.NET_SessionId": "41pyiclvcsdz40dvsi4s5pmr", "_culture": "en-US", "_Role": "Individual", })
            self.wait60sec(driver)
            driver.implicitly_wait(5)
            self.login(user_name, pass_word, driver)
            # driver.get_cookies()
            # driver.session_id
            # driver.execute_script('browserstack_executor: {"action": "getSessionDetails"}')
            # driver.add_cookie({'cookie': my_cookie})

        except:
            self.wait60sec(driver)
            driver.get('https://row1.vfsglobal.com/GlobalAppointment/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/LOSRShyD1pxcML5QC8esmWZOlCfzkBP8joxvSe0zuqEDa7b66mSROQzF6E9izpGMg==')
            self.wait60sec(driver)
            driver.implicitly_wait(5)
            self.login(user_name, pass_word, driver)
            # driver.get_cookies()
            # driver.session_id
            # driver.execute_script('browserstack_executor: {"action": "getSessionDetails"}')
            # driver.add_cookie({'cookie': my_cookie})


        self.wait60sec(driver)
        self.make_schedule(centre, appointment_category, driver)

        self.wait60sec(driver)
        # addcustomer method here added to the mail_otp variable if it is in term of otp case
        self.addcustomer(passport,
                         # confirmpassport,
                         birthdate,
                         passportexpiration,
                         nationality,
                         firstname,
                         lastname,
                         gender,
                         countrycode,
                         mobile,
                         email, driver)

        # if I use to take appointment one by one
        # if mail_otp == False:
        #     # white here a method to write csv for all those are False row
        #     continue
        #     # where to write the row for this one


        # if mail_otp == False:
        #     reference_number = False
        #     picked_date = False
        #     data = [user_name, pass_word, reference_number, firstname, lastname, mobile, email, passport, centre,
        #             appointment_category, birthdate, passportexpiration, nationality, picked_date]
        #     self.write_output(data)
        #     driver.quit()
        # else:
        #     self.wait60sec(driver)
        #     self.email_otp_submission(mail_otp, driver)

        # self.wait60sec(driver)
        # self.email_otp_submission(mail_otp, driver)

        # continue to the next step ( later will split this method to another big method)
        self.wait60sec(driver)
        self.pick_date(month_1, month_2, month_3, driver)
        reference_number = self.reference_number
        picked_date = self.picked_date
        data =[user_name, pass_word, reference_number,  firstname, lastname, mobile, email, passport, centre, appointment_category, birthdate, passportexpiration, nationality, picked_date ]
        self.paynow(zip_code, street, city, state, country, cardholder, cardnumber, expirationmonth, expirationyear, cvvnumber, driver)
        # will write the result
        self.write_output(data)
        driver.quit()




    def run(self):
        self.read_csv()
        threads = []
        for line in self.user_list:
            status = line["Status"]
            if status == '1':
                print("finished...")
                continue
            user_name = line['User Name'].strip()
            pass_word = line['Password'].strip()
            centre = line['Centre'].strip()
            appointment_category = line['Appointment Category'].strip()
            passport = line['passport'].strip()
            # confirmpassport = line['passport'].strip()  # there is no confirm passport option regarding otp
            birthdate = line['birthdate'].strip()
            passportexpiration = line['passportexpiration'].strip()
            nationality = line['nationality'].strip()
            firstname = line['firstname'].upper().strip()
            lastname = line['lastname'].upper().strip()
            gender = line['gender'].strip()
            countrycode = line['countrycode'].strip()
            mobile = line['mobile'].strip()
            email = line['email'].strip()
            #for pick date function
            month_1 = line['month1'].strip()
            month_2 = line['month2'].strip()
            month_3 = line['month3'].strip()
            # for paynow
            zip_code = line['zipcode'].strip()
            street = line['street'].strip()
            city = line['city'].strip()
            state = line['state'].strip()
            country = line['country'].strip()
            cardholder = line['cardholder'].strip()
            cardnumber = line['cardnumber'].strip()
            expirationmonth = line['expirationmonth'].strip()
            expirationyear = line['expirationyear'].strip()
            cvvnumber = line['cvvnumber'].strip()


            # threads = []
            # starting here
            # t = threading.Thread(target=self.from_csvreading_to_sent_token, args=(user_name, pass_word, centre, appointment_category, passport,
            #                                 birthdate, passportexpiration, nationality, firstname, lastname, gender, countrycode,
            #                                 mobile, email, month_1, month_2, month_3,
            #                                     zip_code, street, city, state, country, cardholder, cardnumber, expirationmonth, expirationyear, cvvnumber))
            # # time.sleep(3)
            # t.start()
            # time.sleep(5)
            line["Status"] = 1
        self.update_orgin()
                



#=============== run the script =====#
# if __name__ =='__main__':
#     bot = Appointment()
#     bot.run()


