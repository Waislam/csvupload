import csv
import os

output_file = 'result.csv'

def write_result(data):
    """Write new scrapped data to final result file"""

    headers = ['User Name', 'Password','Reference_number', 'FirstName', 'LastName', 'Mobile', 'Email', 'Passport', 'Centre', 'Appointment_category', 'Birthdate', 'PassportExpiration', 'Nationality', 'Picked Date']
    with open(output_file, 'a', newline='') as file:
        file_is_empty = os.stat(output_file).st_size == 0
        csv_writer = csv.writer(file, delimiter=',')
        if file_is_empty:
            csv_writer.writerow(headers)
        csv_writer.writerow(data)

