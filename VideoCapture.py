# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 15:40:38 2021

@author: Taner
"""

import cv2

# Kameradan gelen görüntüyü bir değişken atılıyor
capture = cv2.VideoCapture(0)
#kameradan gelen görüntünün boyutlarını alınıyor
width= int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width,height)

#Görüntüyü kaydetmek için dosyanın adı ve video codeci veriliyor
videoName="penVideo1.mp4"
codec=cv2.VideoWriter_fourcc(*"DIVX")

#video kaydetmek için kaydedici değişkeni oluşturuluyor
videoWriter= cv2.VideoWriter(videoName,codec,24,(width,height))

#videoyu s tuşuna basılmadan kaydedilmesini önlemek için bir değişken
record = False

#Kameradan gelen kareleri q tuşuna basana kadar göstermesi için bir sonsuz döngü
while True:
    #kameradan gelen kareleri okuyup frame değişkenine atılıyor
    #Görüntülerin hatasız bir şekilde alındığının success değişkeninde olur    
    success,frame = capture.read()
    
    #Görüntüleri Gösteriliyor
    cv2.imshow("Video",frame)
    
    #Bir tuş basıldığı zaman key değişkenine atılıyor
    key=cv2.waitKey(1) 
    
    #Eğer basılan tuş s ise videoyu kaydetmek için record değişkenini true yapılıyor
    if  key == ord('s'):
        record=True
    #Eğer basılan tuş q ise videoyu göstermeyi kapatmak için while döngüsünden çıkılıyor
    elif key == ord('q'):break
    
    #eğer record true ise gelen görüntüyü kaydediyor
    if record:
        videoWriter.write(frame)
            
#while döngüsünden çıktıktan sonra görüntüyü ve kaydediciyi kapatıp açılan görüntü ekranını kapatılıyor ve program sonlandırılıyor       
capture.release()
videoWriter.release()
cv2.destroyAllWindows()        
