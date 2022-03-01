import csv
import os

output_file = os.path.join('app/static/output/result.csv')
input_file = os.path.join('app/static/csv/input.csv')

def write_result(data):
    """Write new scrapped data to final result file"""

    headers = ['User Name', 'Password','Reference_number', 'FirstName', 'LastName', 'Mobile', 'Email', 'Passport', 'Centre', 'Appointment_category', 'Birthdate', 'PassportExpiration', 'Nationality', 'Picked Date', 'Status']
    with open(output_file, 'a', newline='') as file:
        file_is_empty = os.stat(output_file).st_size == 0
        csv_writer = csv.writer(file, delimiter=',')
        if file_is_empty:
            csv_writer.writerow(headers)
        csv_writer.writerow(data)



def write_origin(data):
    """Write new scrapped data to final result file"""

    headers = ['User Name', 'Password','Reference_number', 'FirstName', 'LastName', 'Mobile', 'Email', 'Passport', 'Centre', 'Appointment_category', 'Birthdate', 'PassportExpiration', 'Nationality', 'Picked Date', 'Status']
    with open(input_file, 'w', newline='') as file:
        file_is_empty = os.stat(output_file).st_size == 0
        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(headers)
        for d in data:
            for key, value in d.items():
                writer.writerow([value,])

