# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 17:10:13 2021

@author: Taner
"""

import cv2
import numpy as np
import time
from collections import deque

# nesne merkezini depolayacak veri tipi
#kaç tane merkez noktası hatırlayacağı
buffer_size = 32
# pts bahsedilen meqrkezlerin noktalari  
pts = deque(maxlen = buffer_size) 

def empty(a): pass

#Algılayacağı renklerin aralığı
colorLower=(0,0,0)
colorUpper=(0,0,0)

#İstediğimiz renkleri algılaması trackbar koyuyoruz
cv2.namedWindow("Sonuc")
cv2.resizeWindow("Sonuc", 650, 350)
cv2.createTrackbar("hueMax", "Sonuc", 0, 255, empty)
cv2.createTrackbar("hueLow", "Sonuc", 0, 255, empty)
cv2.createTrackbar("satMax", "Sonuc", 0, 255, empty)
cv2.createTrackbar("satLow", "Sonuc", 0, 255, empty)
cv2.createTrackbar("valueMax", "Sonuc", 0, 255, empty)
cv2.createTrackbar("valueLow", "Sonuc", 0, 255, empty)


#videolar arası geçiş yaparken kodları bir daha yapmasın diye fonksiyon içerisinde
def videos(video):
    
    #işleyeceği videoyu alıyor
    capture=cv2.VideoCapture(video)
    while True:
    
        #videonun çalışıp çalışmadığı ve gelen kareleri değişkene atılıyor
        success,orginalFrame=capture.read()
        
        #trackbar dan gelen değerleri değişkenlere atıyoruz
        hueMax=cv2.getTrackbarPos("hueMax", "Sonuc")
        hueLow=cv2.getTrackbarPos("hueLow", "Sonuc")
        satMax=cv2.getTrackbarPos("satMax", "Sonuc")
        satLow=cv2.getTrackbarPos("satLow", "Sonuc")
        valMax=cv2.getTrackbarPos("valueMax", "Sonuc")
        valLow=cv2.getTrackbarPos("valueLow", "Sonuc")
        colorUpper=(hueMax,satMax,valMax)
        colorLower=(hueLow,satLow,valLow)
        
        #eğer video oynuyorsa işlemleri yapıyor
        if success:
            
            # videoyu daha yavaş bir şekilde oynatılması için bekleniyor ve video oynatılıyor
            time.sleep(0.01)
            cv2.imshow("Orginal Video",orginalFrame)
            
            #renk ayrımını renk aralığından kolay bir şekilde  yapılabilmesi için  hsv formatına çevriliyor
            orginalHsv=cv2.cvtColor(orginalFrame, cv2.COLOR_BGR2HSV)
            cv2.imshow("Orginal hsv",orginalHsv)
            
            #hsvde çıkan bazı gürültüleri yok etmek için blur uygulanıyor
            blurred= cv2.GaussianBlur(orginalFrame, (15,15), 0)
            blurredHsv=cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            cv2.imshow("Blurred hsv",blurredHsv)
            
            #Seçilen renk aralığında maske yapılıyor
            mask=cv2.inRange(blurredHsv,colorLower,colorUpper)
            cv2.imshow("Blurred hsv Mask",mask)
            
            #maskedeki bazı kusurları düzeltilmesi için erosion ve dilation işlemleri yapılıyor
            mask=cv2.erode(mask,None,iterations=4)
            mask=cv2.dilate(mask,None,iterations=4)
            cv2.imshow("erode + dilate mask",mask)
            
            #Maske görüntüsünde oluşan kenarlara göre kontur buluyor
            (contours,_)=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            center=None
            
            #eğer kontur varsa içine girilir
            if len(contours)>0:
                # ekrandaki en büyük konturu c değişkenine atılıyor
                c=max(contours,key=cv2.contourArea)
                
                #konturdan gelen görüntüyü oluşturabileceği en küçük dikdörtgeni özelliklerini rect değişkenine atıyor
                rect=cv2.minAreaRect(c)
                
                #Oluşan dikdörtgenin pozisyon ve boyut değerlerini ekrana yazdırmak için değişkenlere atıyoruz
                ((x,y), (width,height), rotation) = rect
                s = "x: {}, y: {}, width: {}, height: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
                cv2.putText(orginalFrame, s, (25,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255,255,255), 2)

                #gelen değerler ile bir kutu şekli yapıyor
                box=cv2.boxPoints(rect)    
                box=np.int64(box)  
                
                #oluşan konturları görüntüye çiziyor
                cv2.drawContours(orginalFrame, [box], 0, (255,0,0),thickness=2)
                
                #Konturdaki orta noktayı buluyoruz ve bir nokta çiziyoruz
                M = cv2.moments(c)
                center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
                cv2.circle(orginalFrame, center, 5, (255,0,255),-1)
            
            #Orta noktaları arkasında bir çizgi şeklinde iz bırakması için bir deque atılıyor
            pts.appendleft(center)    
            for i in range(1, len(pts)):
                #eğer bir önceki veya şuanki nokta yoksa birşey yapılmıyor
                if pts[i-1] is None or pts[i] is None: continue
                cv2.line(orginalFrame, pts[i-1], pts[i],(0,255,0),3) 
            
            #oluşan konturlu görüntüyü gösteriliyor
            cv2.imshow("Contour",orginalFrame)
        
        key=cv2.waitKey(1)
            
        
        if key==ord("q") or key==ord("n") or key==ord("b"):break
    capture.release()
    cv2.destroyAllWindows()        
    #n tuşuna basıldığı zaman penVideo1 üzerinde işlem yapıyor 
    if key==ord("n"):
        videos("penVideo1.mp4")
        
    #b tuşuna basıldığı zaman penVideo üzerinde işlem yapıyor
    if key==ord("b"):
        videos("penVideo.mp4")
    
    
videos(0)

