#!/usr/bin/env python3

__author__ = 'Adam Marciniak'
__version__ = '0.1.0'
__license__ = 'MIT'
        
import tkinter as tk
import gphoto2 as gp
from captureImage import captureImage
from tkinter.font import Font
import random
import threading
from gpiozero import Button
from PIL import Image, ImageOps, ImageTk
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import logging

logger = logging.getLogger(__name__)

class PhotoBox():
    PHRASES = []
    CAPTURE_DELAY   = 4
    VIEW_TIME       = 6
    UPLOAD_SCREEN   = 6
    UPLOAD          = True
    AUTO_UPLOAD     = True
    HASHTAG         = "#lärmundliebe"
    SHARE_SCREEN_TIME = 3
    IMAGE_WIDTH     = 6000  #Check in Camera
    IMAGE_HEIGHT    = 3368  #Check in Camera
    ACCESS_TOKEN    = "tVHhWyFKDpQAAAAAAAAAAb8g7DrQHiH3g6_OvGp7e5d6-vY0_ULhzArV82oJBPqY"
    
    
    def __init__(self):
        self.load_phrases()
        self.ci = captureImage()
        self.tk = tk.Tk()
        self.button = Button(26, pull_up=True, bounce_time=0.3) #Taster an Pin 26 und Gnd ("die beiden Pins vorne rechts"
        self.tk.title("PhotoBox by Adam Marciniak (Gerpo)")
        self.tk['background'] = "#232b2b"
        self.font = Font(family="Arial", size=72)
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.attributes("-fullscreen", True)
        self.fullScreenState = False
        self.activeTrigger = False
        self.image_factor = (self.IMAGE_WIDTH / self.IMAGE_HEIGHT)
        self.calculated_height = int(1280 / self.image_factor)
     
    def start(self):
        self.content = tk.Label(self.tk, text="Starting PhotoBox", bg="#232b2b", fg="#F1F1F1", font=self.font)
        self.content.pack(expand=1, fill=tk.BOTH)
        
       
#         self.button = tk.Button(self.tk, text="Click me", command=self._triggerCapture).pack()
#         self.button = tk.Button(self.tk, text="Upload me", command=self._uploadPicture).pack()

        self.reset()
        self.button.when_pressed = self._triggerCapture  #Taster an Pin 26 und Gnd ("die beiden Pins vorne rechts" 
        #GPIO.add_event_detect(21, GPIO.RISING, callback=self._uploadPicture, bouncetime=300)

        self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.tk.mainloop()

    def on_closing(self):
        self.ci.dispose()

    def load_phrases(self):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "phrases.txt"), "r") as file:
            self.PHRASES = [line.strip().replace("\\n", "\n") for line in file if line.strip()]

    def toggle_fullscreen(self, event=None):
        self.fullScreenState = not self.fullScreenState  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.fullScreenState)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullScreenState = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def reset(self):
        self._changeText("Hit the black button! \n\n #bierfest2025 \n #lärmundliebe \n #H136 ")
        self.content['image'] = ""
        self.uploadable = False
        self.activeTrigger = False

    def _triggerCapture(self, channel=0):
        logger.debug("Button pressed")
        if not self.activeTrigger:
            self.activeTrigger = True
            self._countdown(self.CAPTURE_DELAY, self._takePicture)
    
#     def _addWatermark(self, path): 
#         img = Image.open(path)
#         
#         #Creating draw object
#         draw = ImageDraw.Draw(img) 
# 
#         #Creating text and font object
#         text = "HolyPython.com"
#         #font = ImageFont.truetype('arial.ttf', 82)
# 
#         #Positioning Text
#         textwidth, textheight = draw.textsize(text)#, font)
#         width, height = img.size  
#         x=width/2-textwidth/2
#         y=height-textheight-300
# 
#         #Applying text on image via draw object
#         draw.text((x, y), text)#, font=font) 
# 
#         #Saving the new image
#         img.save(path)
    

#     def _addWatermark(self, input_image_path, output_image_path, watermark_image_path, position):
#         
#         base_image = Image.open(input_image_path)
#         base_image_crop = ImageOps.contain(base_image, (1200, 673))
#         watermark = Image.open(watermark_image_path)
#         #watermark.convert('RGBA')
#         #watermark.putalpha(70)
#         
#         width, height = (800, 600)
#         print('1')
#         transparent = Image.new('RGBA', (width, height), (0,0,0,0))
#         print('2')
#         transparent.paste(base_image_crop, (0,0))
#         print('3')
#         transparent.paste(watermark, position, mask=watermark)
#         #transparent.show()
#         print('5')
#         transparent.save(output_image_path)
#         print('6')
    
    def _takePicture(self):
        path = ""
        #counter = 0
        try:
            #path = '/home/pi/Pictures/IMG_0816.JPG'
            path = self.ci.capture()
            #counter += 1
        
#             if counter == 1:
#                 self._changeText(str(gp.GPhoto2Error))#"Oh, an error occurred. \n\n Just try again later.")
#                 self._changeText("Photobox startet neu...")
#                 self.tk.after(500)
#                 self.tk.destroy()
        
        except gp.GPhoto2Error:
            logger.exception("GPhoto2Error")
            self._changeText("Oh, an error occurred. \n\n Inform a WG member.")
            self.tk.after(2000, self.tk.destroy)

#             self._changeText("Photobox startet neu...")
#             photoBox.start()
            return
        


#         self._addWatermark(path, path+'bla.png', 'watermark.png', (500 , 0))
#         print('pic')
#        self._connectToGoogle()
        print (path)
        thread = threading.Thread(target = self._uploadPicture, args=(path, ))
        thread.start()
        
        #comment out for offline version
        
        image = Image.open(path)
        image = ImageOps.fit(image, size=(1280, self.calculated_height), centering=(0.5, 0.5))
        #für Bildgröße 6000x3368 (Faktor 1,7814) bei Raspi Auflösung 1280 x 1024
        self.image_source = ImageTk.PhotoImage(image)
        #print("fotogemacht")
        #self.croppedImagePath = path.replace('.JPG', '_cropped.JPG')
        #croppedImage.save(self.croppedImagePath)
        
        self.content['image'] = self.image_source
        
        #label = tk.Label(self.content, text="HURRA", bg="#232b2b", fg="#F1F1F1", font=self.font)
        #label.pack()
        
        self.tk.after(self.VIEW_TIME * 1000, self.reset)
#        thread.join()
#         self._changeText(counter)
#         self.tk.after(self.VIEW_TIME * 1000, self.reset)
        

#     def _uploadScreen(self):
#         if self.uploadable and self.image_source is not None:
#             self._changeText("Want to share? \n\n Press the red button!")
#             self.content['image'] = ""
#             self.tk.after(self.UPLOAD_SCREEN * 1000, self.reset)

# Function for Google API Connection
#         def _connectToGoogle(self):
#             scopes=['https://www.googleapis.com/auth/photoslibrary.appendonly']
# 
#             creds = None
# 
#             if os.path.exists('_secrets_/token_append.json'):
#                 creds = Credentials.from_authorized_user_file('_secrets_/token_append.json', scopes)
#                 
#             if not creds or not creds.valid:
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())
#                 else:
#                     flow = InstalledAppFlow.from_client_secrets_file(
#                         '_secrets_/client_secret.json', scopes)
#                     creds = flow.run_local_server()
#                 print(creds)
#                 # Save the credentials for the next run
#                 with open('_secrets_/token_append.json', 'w') as token:
#                     token.write(creds.to_json())
#                 
#             from google.auth.transport.requests import AuthorizedSession
#             authed_session = AuthorizedSession(creds)

        
    def _uploadPicture(self, file_from):
        scopes=['https://www.googleapis.com/auth/photoslibrary.appendonly']
        creds = None
        if os.path.exists('_secrets_/token_append.json'):
            creds = Credentials.from_authorized_user_file('_secrets_/token_append.json', scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
#             if not creds or not creds.valid:
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())
                flow = InstalledAppFlow.from_client_secrets_file(
#                    'Documents/WG-Github/Raspberry_Pi_5/_secrets_/client_secret.json', scopes)
                    '_secrets_/client_secret.json', scopes)
                creds = flow.run_local_server()
            print(creds)
            # Save the credentials for the next run
#            with open('Documents/WG-Github/Raspberry_Pi_5/_secrets_/token_append.json', 'w') as token:
            with open('_secrets_/token_append.json', 'w') as token:
                token.write(creds.to_json())
        from google.auth.transport.requests import AuthorizedSession
        authed_session = AuthorizedSession(creds)
#             if not creds or not creds.valid:
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())port AuthorizedSession
        authed_session = AuthorizedSession(creds)
        # read image from file
        with open(file_from, "rb") as f:
            image_contents = f.read() 
        # Set file image name
        file_name = file_from.split('/')[-1]
        # upload photo and get upload token
#             if not creds or not creds.valid:
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())
        response = authed_session.post(
            "https://photoslibrary.googleapis.com/v1/uploads", 
            headers={},
            data=image_contents)
        upload_token = response.text 
        # use batch create to add photo and description
        response = authed_session.post(
                'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate',
#             if not creds or not creds.valid:
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())pis.com/v1/mediaItems:batchCreate', 
                headers = { 'content-type': 'application/json' },
                json={
                    "albumId": "APc8FD7ApQQ-FvKFPD-DjFxw-Thzs9P-ss8T8R2hkOLRt7wnaUHdIjJmBfSmF7ccEvGiPXEKgeON",
                    "newMediaItems": [{
                        "description": "L&L 2025",
                        "simpleMediaItem": {
                            "uploadToken": upload_token,
#             if not creds or not creds.valid:
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())oad_token,
                            "fileName": file_name
                        }
                    }]
                }
        )
        print(response.text)
        

    def _changeText(self, textInput):
        self.content['text'] = textInput

    def _countdown(self, remaining = None, callback = lambda: True):
        if remaining is not None:
            self.remaining = remaining
        
        if remaining is not None:
            self.countdown_callback = callback

        if self.remaining < 0:
            self.countdown_callback()
        else:
            if self.remaining == 0:
                self._changeText(str(random.choice(self.PHRASES)))
            else:
                self._changeText(str(self.remaining))

            self.remaining = self.remaining - 1
            self.tk.after(1000, self._countdown)
        

   # def __del__(self):
   #     GPIO.remove_event_detect(26)
   #     GPIO.cleanup()

def _startMain():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    #from gpiozero import Button
    photoBox = PhotoBox()
    photoBox.start()
    #del photoBox
    #GPIO.remove_event_detect(26)
    #GPIO.cleanup()
    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #_startMain()

if __name__ == '__main__':
    try:
#             if not creds or not creds.valid:
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())
        _startMain()
    except KeyboardInterrupt:
        print('Bye')
       # GPIO.cleanup()
    #except RuntimeError:
    #    print('Bye')
#             if not creds or not creds.valid:
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())