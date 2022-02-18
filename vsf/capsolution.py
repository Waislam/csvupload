import os
import random
import time
# for recaptcha solution
# import urllib
# import os
import requests
import speech_recognition # pip install SpeechRecognition
import pydub  # to convert mp3 to wav file
import ffmpy  # pip install ffmpy (and dependency with pydub also need to install sudo apt install ffmpeg (dorkar nai))

from selenium.webdriver.common.by import By



class CapSolution:
    def __init__(self):
        # self.driver = driver
        pass

    def delay(self):
        time.sleep(random.randint(2, 4))

    def download_audio(self, src):
        '''method to download audio from google captcha and read that'''
        rq = requests.get(src)
        filename = 'vsf/audio.mp3'
        with open(filename, 'wb') as f:
            f.write(rq.content)

    def multiple_captcha(self, browser):
        try:
            self.delay()
            time.sleep(3)
            multiple = browser.find_element(By.XPATH, "//div[@class='rc-audiochallenge-error-message']").text.strip()
            print(multiple)
            if multiple == 'Multiple correct solutions required - please solve more.':
                return True
        except:
            return False

    def play_to_verify(self, browser):
        # from here play button started
        time.sleep(4)
        self.delay()

        play_button = browser.find_element(By.XPATH, "//div[@class='rc-audiochallenge-play-button']/button")
        play_button.click()

        # get the audio which recorded after clicking on play button
        time.sleep(2)
        self.delay()
        audio_src = browser.find_element(By.XPATH, "//audio[@id='audio-source']").get_attribute('src')

        # function to download audio from the above source
        self.download_audio(audio_src)

        # convert mp3 to wav file

        audio = pydub.AudioSegment.from_mp3(os.path.join("vsf/audio.mp3"))
        audio.export(os.path.join("vsf/audio.wav"), format="wav")
        current_audio = speech_recognition.AudioFile(os.path.join("vsf/audio.wav"))
        recognizer = speech_recognition.Recognizer()
        with current_audio as source:
            audio = recognizer.record(source)

        data = recognizer.recognize_google(audio)

        # now it is time to input the data to audio response key
        time.sleep(3)
        self.delay()
        browser.find_element(By.XPATH, "//input[@id='audio-response']").send_keys(data.lower())
        time.sleep(2)
        verify_button = browser.find_element(By.XPATH, "//button[@id='recaptcha-verify-button']")
        self.delay()
        time.sleep(3)
        verify_button.click()




    def capthasolution(self, browser):
        # get the captha frame
        self.delay()
        iframe = browser.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
        browser.switch_to.frame(iframe)
        self.delay()
        time.sleep(2)
        # get the checkbox and click
        browser.find_element(By.XPATH, "//span[@id='recaptcha-anchor']").click()

        try:
            #switch to deafault
            browser.switch_to.default_content()
            self.delay()
            challengeframe = browser.find_element(By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']")
            self.delay()
            # switch to audio frame
            browser.switch_to.frame(challengeframe)
            self.delay()
            click_audio = browser.find_element(By.XPATH, "//button[@class='rc-button goog-inline-block rc-button-audio']")
            self.delay()
            click_audio.click()  # clicked to audio challenge

            # switch to recaptcha audio control default_content
            # self.driver.switch_to.default_content()
            # from here play button started
            self.play_to_verify(browser)

            # for the multiple captcha solution
            try:
                multip = self.multiple_captcha(browser)
                while multip:
                    self.delay()
                    self.play_to_verify(browser)
            except:
                print('no multiplication')


            # clicking here to submit
            self.delay()
            browser.switch_to.default_content()
            time.sleep(3)
            browser.find_element(By.XPATH, "//div[@class='frm-button']/input").click()  # clicked on continue
        except:
            # clicking here to the submit
            self.delay()
            browser.switch_to.default_content()
            time.sleep(3)
            browser.find_element(By.XPATH, "//div[@class='frm-button']/input").click()  # clicked on continue

