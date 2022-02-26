import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

api_key = os.getenv('APIKEY_2CAPTCHA', '4bf17e2c6736e7f978960b424720a607')

solver = TwoCaptcha(api_key)

def gcapresponse():

    try:
        result = solver.solve_captcha(
            '6Ld-Kg8UAAAAAK6U2Ur94LX8-Agew_jk1pQ3meJ1',
            'https://row1.vfsglobal.com/GlobalAppointment/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/LOSRShyD1pxcML5QC8esmWZOlCfzkBP8joxvSe0zuqEDa7b66mSROQzF6E9izpGMg==')

    except Exception as e:
        sys.exit(e)

    else:
        # sys.exit('solved: ' + str(result))
        return result