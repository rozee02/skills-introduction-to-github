# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 14:08:56 2025

@author: MONSTER
"""

import cv2
import os
import matplotlib.pyplot as plt
import numpy as np


klasor = "plaka"
resim_adresler = os.listdir(klasor)


for resim_adi in resim_adresler:
    print(f"\n▶️ İşleniyor: {resim_adi}")
    img = cv2.imread(os.path.join(klasor, resim_adi))
    img = cv2.resize(img, (500, 500))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ir_img = cv2.medianBlur(img_gray, 5)
    ir_img = cv2.medianBlur(ir_img, 5)

    medyan = np.median(ir_img)
    low = 0.67 * medyan
    high = 1.33 * medyan
    kenarlik = cv2.Canny(ir_img, low, high)
    kenarlik = cv2.dilate(kenarlik, np.ones((3, 3), np.uint8), iterations=1)

    cnts, _ = cv2.findContours(kenarlik, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    plaka_bulundu = False

    for c in cnts:
        rect = cv2.minAreaRect(c)
        (x, y), (w, h), angle = rect

        if (w > h and w > h * 2) or (h > w and h > w * 2):
            box = cv2.boxPoints(rect)
            box = np.int64(box)

            minx = np.min(box[:, 0])
            miny = np.min(box[:, 1])
            maxx = np.max(box[:, 0])
            maxy = np.max(box[:, 1])

            muhtemel_plaka = img_gray[miny:maxy, minx:maxx].copy()
            muhtemel_medyan = np.median(muhtemel_plaka)

            kontrol1 = 100 < muhtemel_medyan < 200
            kontrol2 = h < 50 and w < 150
            kontrol3 = w < 50 and h < 150

            print(f"  ↪️ Medyan: {muhtemel_medyan:.2f}, Genişlik: {w:.2f}, Yükseklik: {h:.2f}")

            if kontrol1 and (kontrol2 or kontrol3):
                cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
                plt.title(f"✅ Plaka tespit edildi: {resim_adi}")
                plaka_bulundu = True
                break
            else:
                cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    if not plaka_bulundu:
        plt.title(f"🚫 Plaka bulunamadı: {resim_adi}")

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()
    