import csv

inputfile = 'input.csv'

class ReadWrite:
    data_list = []
    def __init__(self):
        pass

    def read_data(self):
        """ Read data csv file """

        with open(inputfile, 'r') as csvfile:
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
                passw = item['passw']


                #below things for without otp
                # housenumber = item['housenumber']
                # streetAddress1 = item['streetAddress1']
                # streetAddress2 = item['streetAddress2']
                # postalcode = item['postalcode']

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
                                       'passw': passw})

                                       # below things are for without otp
                                       # 'housenumber': housenumber,
                                       # 'streetAddress1': streetAddress1,
                                       # 'streetAddress2': streetAddress2,
                                       # 'postalcode': postalcode})


