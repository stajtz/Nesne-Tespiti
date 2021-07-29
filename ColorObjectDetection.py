# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 17:10:13 2021

@author: Taner
"""

import cv2
import numpy as np
import time

#Algılayacağı renklerin aralığı
colorLower=(43,95,0)
colorUpper=(145,255,255)

#videolar arası geçiş yaparken kodları bir daha yapmasın diye fonksiyon içerisinde
def videos(video):
    
    #işleyeceği videoyu alıyor
    capture=cv2.VideoCapture(video)
    while True:
    
        #videonun çalışıp çalışmadığı ve gelen kareleri değişkene atılıyor
        success,orginalFrame=capture.read()
        
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
            
            #eğer kontur varsa içine girilir
            if len(contours)>0:
                # ekrandaki en büyük konturu c değişkenine atılıyor
                c=max(contours,key=cv2.contourArea)
                
                #konturdan gelen görüntüyü oluşturabileceği en küçük dikdörtgeni özelliklerini rect değişkenine atıyor
                rect=cv2.minAreaRect(c)
    
                #gelen değerler ile bir kutu şekli yapıyor
                box=cv2.boxPoints(rect)    
                box=np.int64(box)    
                
                #oluşan konturları görüntüye çiziyor
                cv2.drawContours(orginalFrame, [box], 0, (255,0,0),thickness=2)
            
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
    
    
videos("penVideo.mp4")
