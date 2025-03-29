# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 19:39:06 2025

@author: MONSTER
"""

import heapq
import time

class Musteri:
    def __init__(self, isim, yas, musteri_tipi, islem_tipi):
        self.isim = isim
        self.yas = yas
        self.musteri_tipi = musteri_tipi  # "VIP", "Yaşlı", "Normal"
        self.islem_tipi = islem_tipi      # "Para Çekme", "Kredi", "Döviz"
        self.sira_numarasi = None

    def __lt__(self, other):
        """Öncelik sıralaması (VIP > Yaşlı > Normal)"""
        musteri_oncelik = {"VIP": 1, "Yaşlı": 2, "Normal": 3}
        if musteri_oncelik[self.musteri_tipi] != musteri_oncelik[other.musteri_tipi]:
            return musteri_oncelik[self.musteri_tipi] < musteri_oncelik[other.musteri_tipi]
        return self.yas > other.yas  # Aynı tipteyse yaşa göre sıralar

class BankaSiraSistemi:
    def __init__(self):
        self.kuyruk = []
        self.son_sira_numarasi = 1000  # İlk sıra numarası

    def musteri_ekle(self, musteri):
        self.son_sira_numarasi += 1
        musteri.sira_numarasi = self.son_sira_numarasi
        heapq.heappush(self.kuyruk, musteri)
        print(f"{musteri.isim} için sıra numarası: {musteri.sira_numarasi}")

    def siradaki_musteriyi_cagir(self):
        if self.kuyruk:
            musteri = heapq.heappop(self.kuyruk)
            print(f"\nSıradaki müşteri: {musteri.isim} (Sıra No: {musteri.sira_numarasi}, Tip: {musteri.musteri_tipi})")
        else:
            print("Bekleyen müşteri yok.")

# Örnek Kullanım
banka = BankaSiraSistemi()
banka.musteri_ekle(Musteri("Ahmet", 30, "Normal", "Para Çekme"))
banka.musteri_ekle(Musteri("Mehmet", 65, "Yaşlı", "Kredi Başvurusu"))
banka.musteri_ekle(Musteri("Ayşe", 40, "VIP", "Döviz"))
banka.musteri_ekle(Musteri("Zeynep", 70, "Yaşlı", "Para Çekme"))

time.sleep(1)  # Simüle etmek için küçük bir bekleme süresi

banka.siradaki_musteriyi_cagir()
banka.siradaki_musteriyi_cagir()
banka.siradaki_musteriyi_cagir()
banka.siradaki_musteriyi_cagir()
