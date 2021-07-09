# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 13:20:17 2021

@author: Nielsen Castelo Damasceno Dantas
"""

import cv2
import imutils
import time

def calculaDiferenca(img1, img2, img3):
  d1 = cv2.absdiff(img3, img2)
  d2 = cv2.absdiff(img2, img1)
  return cv2.bitwise_and(d1, d2)

def calculaDiferenca2(img1,img2):
    d1 = cv2.absdiff(img1, img2)

    return sum(sum(d1))


dimensao = 400

totalFrames = 0
skip_frames = 1

url = 'rtsp://admin:teste@172.25.1.1:554/Streaming/channels/2/'


cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(url)

for i in range(0, 20):
    (grabbed, frame) = cap.read()


frame = imutils.resize(frame, width=dimensao)

# Guarda as informacoes da posicao do Roi 1
bbox1 = cv2.selectROI(frame, False)
x_1, y_1, w_1, h_1 = bbox1


# Guarda as informacoes da posicao do Roi 2
bbox2 = cv2.selectROI(frame, False)
x_2, y_2, w_2, h_2 = bbox2


roi1 = frame[y_1 : y_1 + h_1, x_1 : x_1 + w_1]
roi2 = frame[y_2 : y_2 + h_2, x_2 : x_2 + w_2]

roi1_gray = cv2.cvtColor(roi1, cv2.COLOR_RGB2GRAY)
roi1_gray = cv2.GaussianBlur (roi1_gray, (21, 21), 0)

roi2_gray = cv2.cvtColor(roi2, cv2.COLOR_RGB2GRAY)
roi2_gray = cv2.GaussianBlur (roi2_gray, (21, 21), 0)


nivel_ajuste = 2000
while True:
        ret, frame = cap.read()

        if not (ret):
            print('Erro no frame')
            st = time.time()
            #cap = cv2.VideoCapture(url)
            cap = cv2.VideoCapture(0)
            print("tempo perdido devido à inicialização  : ", time.time()-st)
            continue

        if ret == True:
            if totalFrames % skip_frames == 0:
                frame = imutils.resize(frame, width=dimensao)

                # Leitura do Roi 1
                imcrop_1 = frame[int(bbox1[1]):int(bbox1[1] + bbox1[3]), int(bbox1[0]):int(bbox1[0] + bbox1[2])]
                imcrop_1_gray = cv2.cvtColor(imcrop_1, cv2.COLOR_RGB2GRAY)
                imcrop_1_gray = cv2.GaussianBlur (imcrop_1_gray, (21, 21), 0)
                
                # desenha o roi 1 no frame
                cv2.rectangle(frame, (x_1, y_1), (x_1 + w_1, y_1 + h_1), (255, 0, 0), 2)
                
                # Leitura do Roi 2
                imcrop_2 = frame[int(bbox2[1]):int(bbox2[1] + bbox2[3]), int(bbox2[0]):int(bbox2[0] + bbox2[2])]
                imcrop_2_gray = cv2.cvtColor(imcrop_2, cv2.COLOR_RGB2GRAY)
                imcrop_2_gray = cv2.GaussianBlur (imcrop_2_gray, (21, 21), 0)
                
                # desenha o roi 2 no frame
                cv2.rectangle(frame, (x_2, y_2), (x_2 + w_2, y_2 + h_2), (255, 0, 0), 2)
               
                
                # Valida o valor Roi 1
                abs_diferenca_1 = cv2.absdiff(imcrop_1_gray, roi1_gray)
                threshold_1 = cv2.threshold(abs_diferenca_1, 25, 255, cv2.THRESH_BINARY)[1]
                valor_1 = sum(sum(threshold_1))
                
                
                  # Valida o valor Roi 2
                abs_diferenca_2 = cv2.absdiff(imcrop_2_gray, roi2_gray)
            
                threshold_2 = cv2.threshold(abs_diferenca_2, 25, 255, cv2.THRESH_BINARY)[1]
                valor_2 = sum(sum(threshold_2))
                
                print(valor_1)
                print(valor_2)
            
                if valor_1 > nivel_ajuste:
                    
                    cv2.rectangle(frame, (x_1, y_1), (x_1 + w_1, y_1 + h_1), (0, 255, 0), 2)
                    print('Detecatado Doca 1 com valor: ' , valor_1)
                    
                
                if valor_2 > nivel_ajuste:
                    
                    cv2.rectangle(frame, (x_2, y_2), (x_2 + w_2, y_2 + h_2), (0, 255, 0), 2)
                    print('Detecatado Doca 2 com valor: ' , valor_2)


                cv2.imshow('Detecacao de Trunk', frame) 
                cv2.imshow('imcrop_1_gray', threshold_1) 
                cv2.imshow('imcrop_2_gray', threshold_2)   
        totalFrames += 1

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

