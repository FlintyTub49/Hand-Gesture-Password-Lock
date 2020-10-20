#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import cv2
import numpy as np
import pandas as pd
import matplotlib as plt
import pickle as pk
import webbrowser
from cryptography.fernet import Fernet

from sklearn.preprocessing import StandardScaler
from keras.models import load_model


# In[6]:


i = 0
vault = 'https://drive.google.com/drive/folders/1CW79vzAX3ec5ROaL6jbBA3HezuihxSpP?usp=sharing'
outputs = ['fist', 'thumbs', 'yo', 'five', 'two', 'blank']
password = ['fist', 'thumbs', 'five', 'two']
userInput = []

pca_reload = pk.load(open("pca_400.pkl",'rb'))
new_model = load_model('best_model_PCA_400.hdf5')



# Open the device at the ID 0
cap = cv2.VideoCapture(0)

# Check whether user selected camera is opened successfully.
sc = StandardScaler()
if not (cap.isOpened()):
T    print("Could not open video device")

# To set the resolution
cap.set(3, 480)
cap.set(4, 640)

while(True):
    # Capture frame-by-frame
    _, frame = cap.read()
    temp = np.array(frame)
    
    ''' ---------- Drawing a Rectangle ---------- '''
    cv2.rectangle(temp, (320, 0), (639, 320), (255, 255, 255), 1)
    
    

    
    ''' ---------- Getting the Subframe ---------- '''
    sub = temp[0:320, 320:640, :].copy()
    
    
    
    
    ''' ---------- Preprocessing The Hand Gesture Sub Frame ---------- '''
    colorSep = cv2.cvtColor(sub, cv2.COLOR_BGR2HSV)         
    
    # Define range of skin color in HSV
    skinLowRange = np.array([0, 20, 70], dtype = np.uint8)
    skinUpRange = np.array([20, 255, 255], dtype = np.uint8)
    
    # Creating a mask image with only skil colour, rest all images become 0
    skin = cv2.inRange(colorSep, skinLowRange, skinUpRange)
    
    # Blurring the image to reduce noise
    skin = cv2.GaussianBlur(skin, (3, 3), 100)
    skin = cv2.GaussianBlur(skin, (3, 3), 100)
#     cv2.imshow('Sub', skin)
    

    
    ''' ---------- Detecting The Hand Gesture ---------- '''
    out = np.array(skin).reshape((1, 320*320))
    
    out = pca_reload.transform(out)
    pred_out = new_model.predict(out)
    
    if pred_out[0][0] >= 0.90: text_out = outputs[0]
    
    elif pred_out[0][1] >= 0.90: text_out = outputs[1]
    elif pred_out[0][2] >= 0.90: text_out = outputs[2]
    elif pred_out[0][3] >= 0.90: text_out = outputs[3]
    elif pred_out[0][4] >= 0.90: text_out = outputs[4]
    elif pred_out[0][5] >= 0.90: text_out = outputs[5]
    
    # To show what is being read 
    cv2.rectangle(temp, (320, 320), (639, 380),(0, 0, 0), -1)
    cv2.putText(temp, text_out, (340, 360),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_4)
    cv2.putText(temp, str(25-i), (585, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_4)
    
    
    
    ''' ---------- Showing if there is a passowrd or is it empty ---------- '''
    cv2.rectangle(temp, (30, 420), (360, 460), (0, 0, 0), -1)
    if len(userInput) != 0:
        cv2.putText(temp, 'Reading', (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_4)
    elif len(userInput) == 0 and i < 5:
        cv2.putText(temp, 'Password Reset', (50, 450),cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 255, 255), 2, cv2.LINE_4)
    else:
        cv2.putText(temp, 'No Password Read', (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (255, 255, 255), 2, cv2.LINE_4)
    
    
    ''' ---------- Verifying The Password ---------- '''
    if i == 25:
        userInput.append(text_out)
        flag = 0
        if len(userInput) == len(password):
            if userInput == password:
                cv2.putText(temp, 'Correct Password', (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 255, 255), 2, cv2.LINE_4)
                webbrowser.open(vault)
                break
            else: 
                userInput = []
        
        else:
            for j in range(len(userInput)):
                if userInput[j] != password[j]: 
                    userInput = []
                    break
        i = 0
    
    

    ''' ---------- Printing the Frames ---------- '''
    # Display the Original Frame
    cv2.imshow('temp Image', temp)
    i = i+1
    
    # Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

