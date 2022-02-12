import imaplib
import re

class Realotp:
    def __init__(self):
        pass

    def outlook_otp(self, email, passw):
        # username = "waislam67@outlook.com"
        # password = "waislamoutlook22"

        # imap = imaplib.IMAP4_SSL("outlook.office365.com")
        # create an IMAP4 class with SSL
        try:
            myemail = imaplib.IMAP4_SSL("imap-mail.outlook.com")
            # authenticate
            myemail.login(email, passw)

            # connect with email
            myemail.select("INBOX")
            result, messages = myemail.search(None, '(FROM "donotreply@vfsglobal.com")' )

            message_list = []
            for message in messages[0].split():
                data = myemail.fetch(message, '(RFC822)')
                message_list.append(data)

            myneed = message_list[-1][1][0][1]

            stri = str(myneed, 'utf-8')

            l = stri.split('Regards')
            text_only_list = l[0].split('Dear')
            text = text_only_list[1]

            otp = re.findall(r'\d+', text)
            otp_text = ''.join(otp).strip()
            print('in no use '+ otp_text)
            return otp_text
        except:
            return False




