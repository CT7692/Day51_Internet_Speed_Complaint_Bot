from selenium import webdriver
from selenium.webdriver.common.by import By
from twilio.rest import Client
from tkinter import messagebox
import time
import os

class CheckInternetSpeed:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net")
        go  = self.driver.find_element(By.CLASS_NAME, value="start-text")
        go.click()
        time.sleep(50)
        str_download_speed = (
            self.driver.find_element(
                By.XPATH,
                value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span')).text
        self.down = float(str_download_speed)
        str_upload_speed = (
            self.driver.find_element(
                By.XPATH,
                value='//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span')).text
        self.up = float(str_upload_speed)


    def notify(self, download, upload):
        some_num = os.environ.get("SOME_NUM")

        promised_speeds = {
            "download": download,
            "upload": upload
        }

        if self.down < promised_speeds["download"] or self.up < promised_speeds["upload"]:
            twilio_sid = os.environ.get("TWILIO_SID")
            auth_token = os.environ.get("AUTH_TOKEN")
            some_num = os.environ.get("SOME_NUM")
            twi_client = Client(twilio_sid, auth_token)
            message = (f"FYI: Your current download speed is {self.down} Mbps with an upload speed of {self.up} Mbps"
                       f" when you're paying for a download speed of {promised_speeds['download']} and an upload speed"
                       f"of {promised_speeds['upload']}. What's up with that?")
            message = twi_client.messages.create(body=message, from_=some_num, to="+16362845670")
            messagebox.showinfo(title="Complete", message="Notification sent.")

        else:
            messagebox.showinfo(title="Complete", message="Internet speed functioning as expected.")
