# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 09:25:33 2021

@author: Taner
"""

import cv2

#Yüz tanıma için cascade mizi okuyoruz
faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#Kameradan gelen görüntüyü almak için değişkenimize atıyoruz
capture=cv2.VideoCapture(0)
while True:
    #kameradan görüntü bilgisini değişkenlere atıyoruz
    success,frame=capture.read()
    
    #eğer kameradan görüntü geliyorsa işlemlerimizi yapıyoruz
    if success:
        
        #Gelen görüntüyü yüz yaklaması için cascade veriyoruz
        faceRect=faceCascade.detectMultiScale(frame,minNeighbors=7)
        
        #cascade den gelen yüz etrafına bir dikdörtgen çizdiriyoruz
        for (x,y,w,h) in faceRect:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)
        cv2.imshow("Face detection",frame)
        
    #klavyeden bir tuşa basılırsa değişkene atıyoruz ve q harfine basılırsa kameradan görüntü almayı durdurup oluşturduğumuz ekranları kapıyoruz
    key=cv2.waitKey(1)
    if key==ord("q"):break
    
capture.release()
cv2.destroyAllWindows()