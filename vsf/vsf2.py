import random
import threading
from multiprocessing import Process

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from proxylist import get_free_proxy # list of freeproxy

#for dropdown selection
from selenium.webdriver.support.ui import Select

# for email otp
from otp import GmailOtp

import time
# for recaptcha solution
# import urllib
# import os
import requests

from capsolution import CapSolution


# for file reading and writing
# import pandas
# import csv
# inputfile = 'vsfinput.csv' # all these things goes to external file
from reading import ReadWrite #to read inputed file
from output import write_result



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
    # options = Options()
    # # ua = UserAgent()
    # # userAgent = ua.random
    # userAgent = 'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    # options.add_argument(f'user-agent={userAgent}')

    service_obj = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service_obj)
    # driver = None
    def __init__(self):
        # self.driver = webdriver.Chrome(service=self.service_obj)
        pass


    def delay(self):
        time.sleep(random.randint(2, 4))

    def wait60sec(self):
        self.driver.implicitly_wait(60)

    def write_output(self, data):
        output = write_result(data)
        return output

    # def read_csv(self):
    #     read = ReadWrite()
    #     self.user_list = read.data_list
    #     read.read_data()

    def solution_cap(self):
        capsul = CapSolution()
        capsul.capthasolution(self.driver)

    def gmail_otp(self):
        '''this method supposed to fetch otp from gmail'''
        otp = GmailOtp()
        return otp.gmail_authenticate()




    def primary_selection(self, centre, appointment_category):
        '''This method for selection center, appointment category'''
        #need to select visiting country and residence

        # starting selection of Center and Appointment category
        self.delay()
        center_selection = Select(self.driver.find_element(By.XPATH, "//select[@id='LocationId']"))
        center_selection.select_by_value(centre)
        self.wait60sec()
        self.delay()
        category_selection = Select(self.driver.find_element(By.XPATH, "//select[@id='VisaCategoryId']"))
        category_selection.select_by_value(appointment_category)

        #click on continue button
        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, "//input[@id='btnContinue']").click()
        self.delay()
        #next page loading
        # now click on Add Customer button
        self.wait60sec()
        self.driver.find_element(By.XPATH, "//a[@class='submitbtn']").click()
        self.driver.implicitly_wait(3)

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
                     email):
                     # housenumber,
                     # streetAddress1,
                     # streetAddress2,
                     # postalcode):
        '''this method working to add all information in the page of add customer'''
        self.reference_number = ''
        self.driver.implicitly_wait(10)
        self.delay()
        self.driver.find_element(By.XPATH, "//input[@id='PassportNumber']").send_keys(passport)
        #There is no passport form element regarding otp
        # self.driver.find_element(By.XPATH, "//input[@id='ConfirmPassportNumber']").send_keys(confirmpassport)
        self.driver.find_element(By.XPATH, "//input[@id='DateOfBirth']").send_keys(birthdate)
        self.driver.find_element(By.XPATH, "//input[@id='PassportExpiryDate']").send_keys(passportexpiration)

        # select nationality
        Select(self.driver.find_element(By.XPATH, "//select[@id='NationalityId']")).select_by_value(nationality)

        #input name
        first_name = self.driver.find_element(By.XPATH, "//input[@id='FirstName']")
        first_name.clear()
        first_name.send_keys(firstname)
        last_name = self.driver.find_element(By.XPATH, "//input[@id='LastName']")
        last_name.clear()
        last_name.send_keys(lastname)


        #select gender
        Select(self.driver.find_element(By.XPATH, "//select[@id='GenderId']")).select_by_value(gender)

        #input phone and email
        country_code = self.driver.find_element(By.XPATH, "//input[@class='form-control phcode-input_field']")
        country_code.clear()
        country_code.send_keys('+' + countrycode)
        mobile_number = self.driver.find_element(By.XPATH, "//input[@id='Mobile']")
        mobile_number.clear()
        mobile_number.send_keys(mobile)
        email_field = self.driver.find_element(By.XPATH, "//input[@id='validateEmailId']")
        email_field.clear()
        email_field.send_keys(email)


        #below things are for without otp part
        #qurier address filling
        # self.driver.find_element(By.XPATH, "//input[@id='HouseNumber']").send_keys(housenumber)
        # self.driver.find_element(By.XPATH, "//input[@id='StreetAddress1']").send_keys(streetAddress1)
        # self.driver.find_element(By.XPATH, "//input[@id='StreetAddress2']").send_keys(streetAddress2)
        # self.driver.find_element(By.XPATH, "//input[@id='PostalCode']").send_keys(postalcode)

        #click on submit button
        self.delay()
        self.driver.find_element(By.XPATH, "//input[@id='submitbuttonId']").click()

        # click on alert popup
        self.wait60sec()
        self.delay()
        time.sleep(2)
        self.driver.switch_to.alert.accept()

        #from here it will goes to OTP .. now take reference numbar and click on sent OTP button

        self.driver.switch_to.default_content()
        self.driver.implicitly_wait(10)
        self.delay()
        # reference number
        self.reference_number += self.driver.find_element(By.XPATH, "//div[@class='mandatory-txt']/label/b").text.strip()
        print(self.reference_number)
        self.driver.find_element(By.XPATH, "//input[@type='submit']").click() #sent otp button click

        # now time to get otp from email via otp module
        print('Waiting for OTP')
        time.sleep(90)
        self.wait60sec()
        try:
            otp = self.gmail_otp()
            if otp == False:
                print('Trying to resent otp')
                time.sleep(3)
                self.driver.find_element(By.XPATH, "//input[@value='Regenerate OTP']").click()  # click to resent button
                otp = self.gmail_otp()
                return otp
            else:
                print(otp)
                return otp
        except:
            print('Customer just added')
            return False
            # NOte: I have move to other row of excel if otp verification is not done( from next row to sent otp first time)




    def email_otp_submission(self, otp):
        '''this method will submit the email otp'''
        otp_input = self.driver.find_element(By.XPATH, "//input[@id='OTPe']")
        otp_input.send_keys(otp)  # otp input is done here
        # now submit
        time.sleep(10)
        self.driver.find_element(By.XPATH, "//input[@value='Verify OTP and Continue']").click()


    def pick_date(self):
        self.picked_date = ''
        self.delay(3)
        # take the reference number
        reference_number = self.driver.find_element(By.XPATH, "//div[@class='mandatory-txt']/label/b").text.strip()
        # click on continue button from value added service page
        self.driver.find_element(By.XPATH, "//input[@id='btnContinueService']").click() #clicked on continue button
        # go further
        self.driver.implicitly_wait(5)

        # now time to select date
        # date selection
        self.delay()
        available_date_list = self.driver.find_elements(By.XPATH, "//td[@style='background-color: rgb(188, 237, 145); cursor: pointer;']")[0]
        available_date_list.click()
        self.picked_date += available_date_list

        # click on time schedule
        time.sleep(1)
        schedule_list = self.driver.find_elements(By.XPATH, "//div[@id='TimeBandsDiv']/table/tbody/tr")[1:]
        mytime = schedule_list[0]
        mytime.click()
        time.sleep(1)


        #click on confirm button
        self.driver.find_element(By.XPATH, "//input[@id='btnConfirm']").click()
        self.delay()

        # click on alert prompt
        self.wait60sec()
        self.driver.switch_to.alert.accept()

        # loaded a new page
        # select yes check box
        time.sleep(5)
        self.delay()
        self.driver.switch_to.default_content()
        self.driver.find_element(By.XPATH, "//input[@id='ReachVFS']").click()
        #select accept check box
        self.driver.find_element(By.XPATH, "//input[@id='IAgree']").click()

        # click on confirm and pay button to continue
        self.driver.find_element(By.XPATH, "//input[@id='btnConfirm']")
        # click on alert prompt
        self.wait60sec()
        self.driver.switch_to.alert.accept()


    def paynow(self, cardnumber, expirationmonth, expirationyear, cvvnumber):
        self.delay()
        self.driver.switch_to.default_content()

        # input card number
        card_number = self.driver.find_element(By.XPATH, "//input[@id='creditcard_cardNumber']")
        card_number.send_keys(cardnumber)

        # select card expiration
        # month
        card_expiration_month = Select(self.driver.find_element(By.XPATH, "//select[@id='creditcard_expiryMonth']"))
        card_expiration_month.select_by_value(expirationmonth)
        # year
        card_expiration_year = Select(self.driver.find_element(By.XPATH, "//select[@id='creditcard_expiryYear']"))
        card_expiration_year.select_by_value(expirationyear)

        # input cvv
        self.driver.find_element(By.XPATH, "//input[@id='CVV']").send_keys(cvvnumber)

        # Here need to add I agree check box to check
        # then the pay now
        self.driver.find_element(By.XPATH, "//button[@id='paySubmit']").click()



    def login(self, user_name, pass_word):
        '''This method is suppose to solve login and login captcha problem'''
        email = self.driver.find_element(By.XPATH, "//input[@id='EmailId']")
        # email.send_keys('waislam67@gmail.com')
        email.send_keys(user_name)
        password = self.driver.find_element(By.XPATH, "//input[@id='Password']")
        # password.send_keys('H!PBb!@B4CxjQN5')
        password.send_keys(pass_word)

        #form data mission country name
        mission = self.driver.find_element(By.XPATH, "//input[@id='Mission']")
        self.driver.execute_script("arguments[0].setAttribute('value','GJZ8UZVM+guclLYeCIytdQ==')", mission)
        print(mission.get_attribute('value'))
        country = self.driver.find_element(By.XPATH, "//input[@id='Country']")
        self.driver.execute_script("arguments[0].setAttribute('value', 'LuPeffehutdAFt+0k6EVBw==')", country)
        print(country.get_attribute('value'))

        self.delay()
        self.driver.implicitly_wait(5)


        #cusome default captcha
        # image_src = self.driver.find_element(By.XPATH, "//img[@id='CaptchaImage']").get_attribute('src')
        # print(image_src)
        # self.default_cap_solution(image_src)

        #google captcha
        self.solution_cap()


    def make_schedule(self, centre, appointment_category):
        self.driver.find_element(By.XPATH, "//ul[@class='leftNav-ul']/descendant::li[1]/a").click()
        self.driver.implicitly_wait(2)
        time.sleep(3)
        self.primary_selection(centre, appointment_category)


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
                                      email):
        # for line in self.user_list:
        #     user_name = line['User Name'].strip()
        #     pass_word = line['Password'].strip()
        #     centre = line['Centre'].strip()
        #     appointment_category = line['Appointment Category'].strip()
        #     passport = line['passport'].strip()
        #     # confirmpassport = line['passport'].strip()  # there is no confirm passport option regarding otp
        #     birthdate = line['birthdate'].strip()
        #     passportexpiration = line['passportexpiration'].strip()
        #     nationality = line['nationality'].strip()
        #     firstname = line['firstname'].upper().strip()
        #     lastname = line['lastname'].upper().strip()
        #     gender = line['gender'].strip()
        #     countrycode = line['countrycode'].strip()
        #     mobile = line['mobile'].strip()
        #     email = line['email'].strip()

            # before this an OTP will be sent. and below things for without OtP
            # housenumber = line['housenumber'].strip()
            # streetAddress1 = line['streetAddress1'].strip()
            # streetAddress2 = line['streetAddress2'].strip()
            # postalcode = line['postalcode'].strip()

            # self.driver.get('https://row1.vfsglobal.com/GlobalAppointment/Home/Index')
        try:
            self.wait60sec()
            self.driver.get('https://row1.vfsglobal.com/GlobalAppointment/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/LOSRShyD1pxcML5QC8esmWZOlCfzkBP8joxvSe0zuqEDa7b66mSROQzF6E9izpGMg==')
            self.login()
        except:
            self.wait60sec()
            self.driver.get('https://row1.vfsglobal.com/GlobalAppointment/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/LOSRShyD1pxcML5QC8esmWZOlCfzkBP8joxvSe0zuqEDa7b66mSROQzF6E9izpGMg==')
            self.login(user_name, pass_word)
        self.wait60sec()
        self.make_schedule(centre, appointment_category)

        self.wait60sec()
        mail_otp = self.addcustomer(passport,
                         # confirmpassport,
                         birthdate,
                         passportexpiration,
                         nationality,
                         firstname,
                         lastname,
                         gender,
                         countrycode,
                         mobile,
                         email)
        # housenumber,
        # streetAddress1,
        # streetAddress2,
        # postalcode)
        # if I use to take appointment one by one
        # if mail_otp == False:
        #     # white here a method to write csv for all those are False row
        #     continue
        #     # where to write the row for this one
        # if mail_otp == False:
        #     self.driver.refresh(30)
        #     time.sleep(3600)
        # else:
        #     self.wait60sec()
        #     self.email_otp_submission(mail_otp)

        self.wait60sec()
        self.email_otp_submission(mail_otp)

        # continue to the next step ( later will split this method to another big method)
        self.wait60sec()
        self.pick_date()
        reference_number = self.reference_number
        picked_date = self.picked_date
        data =[user_name, pass_word, reference_number,  firstname, lastname, mobile, email, passport, centre, appointment_category, birthdate, passportexpiration, nationality, picked_date ]
        # self.paynow(cardnumber, expirationmonth, expirationyear, cvvnumber)
        # will write the result
        self.write_output(data)
        self.driver.quit()




    # def run(self):
    #     self.read_csv()
    #     threads = []
    #     for line in self.user_list:
    #         user_name = line['User Name'].strip()
    #         pass_word = line['Password'].strip()
    #         centre = line['Centre'].strip()
    #         appointment_category = line['Appointment Category'].strip()
    #         passport = line['passport'].strip()
    #         # confirmpassport = line['passport'].strip()  # there is no confirm passport option regarding otp
    #         birthdate = line['birthdate'].strip()
    #         passportexpiration = line['passportexpiration'].strip()
    #         nationality = line['nationality'].strip()
    #         firstname = line['firstname'].upper().strip()
    #         lastname = line['lastname'].upper().strip()
    #         gender = line['gender'].strip()
    #         countrycode = line['countrycode'].strip()
    #         mobile = line['mobile'].strip()
    #         email = line['email'].strip()
    #
    #         # threads = []
    #         # starting here
    #
    #         t = threading.Thread(target=self.from_csvreading_to_sent_token, args=(user_name, pass_word, centre, appointment_category, passport,
    #                                            birthdate, passportexpiration, nationality, firstname, lastname, gender, countrycode,
    #                                            mobile, email))
    #         t.start()
            # threads.append(t)









#=============== run the script =====#
if __name__ =='__main__':
    bot = Appointment()
    # bot.run()
    read = ReadWrite()
    read.read_data()
    reading_list = read.data_list
    threads = []
    for line in reading_list:
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


        # starting here
        # mybot = bot.from_csvreading_to_sent_token(user_name, pass_word, centre, appointment_category, passport,
        #                            birthdate, passportexpiration, nationality, firstname, lastname, gender, countrycode,
        #                            mobile, email)
        # t = threading.Thread(target=mybot)
        # t.start()
        t = threading.Thread(target=bot.from_csvreading_to_sent_token,
                             args=(user_name, pass_word, centre, appointment_category, passport,
                                   birthdate, passportexpiration, nationality, firstname, lastname, gender, countrycode,
                                   mobile, email))
        threads.append(t)
        # p = Process(target=bot.from_csvreading_to_sent_token, args=(user_name, pass_word, centre, appointment_category, passport,
        #                             birthdate, passportexpiration, nationality, firstname, lastname, gender, countrycode,
        #                             mobile, email))
        # p.start()

    for item in threads:
        item.start()
        time.sleep(2)
