import csv
import os

# inputfile = 'input.csv'

filepath = os.path.join('app/static/csv/input.csv')

class ReadWrite:
    data_list = []
    def __init__(self):
        pass

    def read_data(self):
        """ Read data csv file """

        with open(filepath) as csvfile:
            thereader = csv.DictReader(csvfile)
            # thereader = csv.reader(csvfile)
            # next(thereader, None)  # skip header
            for item in thereader:
                user_name = item['User Name']
                pass_word = item['Password']
                centre = item['Centre']
                appointment_category = item['Appointment Category']
                passport = item['passport']
                birthdate = item['birthdate']
                passportexpiration = item['passportexpiration']
                nationality = item['nationality']
                firstname = item['firstname']
                lastname = item['lastname']
                gender = item['gender']
                countrycode = item['countrycode']
                mobile = item['mobile']
                email = item['email']
                month1 = item['month1']
                month2 = item['month2']
                month3 = item['month3']
                zipcode = item['zipcode']
                street = item['street']
                city = item['city']
                state = item['state']
                country = item['country']
                cardholder = item['cardholder']
                cardnumber = item['cardnumber']
                expirationmonth = item['expirationmonth']
                expirationyear = item['expirationyear']
                cvvnumber = item['cvvnumber']


                self.data_list.append({'User Name': user_name,
                                       'Password': pass_word,
                                       'Centre': centre,
                                       'Appointment Category': appointment_category,
                                       'passport': passport,
                                       'birthdate': birthdate,
                                       'passportexpiration': passportexpiration,
                                       'nationality': nationality,
                                       'firstname': firstname,
                                       'lastname': lastname,
                                       'gender': gender,
                                       'countrycode': countrycode,
                                       'mobile': mobile,
                                       'email': email,
                                       'month1': month1,
                                       'month2': month2,
                                       'month3': month3,
                                       'zipcode': zipcode,
                                       'street': street,
                                       'city': city,
                                       'state': state,
                                       'country': country,
                                       'cardholder': cardholder,
                                       'cardnumber': cardnumber,
                                       'expirationmonth': expirationmonth,
                                       'expirationyear': expirationyear,
                                       'cvvnumber': cvvnumber})

                                       # below things are for without otp
                                       # 'housenumber': housenumber,
                                       # 'streetAddress1': streetAddress1,
                                       # 'streetAddress2': streetAddress2,
                                       # 'postalcode': postalcode})


