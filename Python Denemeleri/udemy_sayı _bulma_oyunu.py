import random
import time
print("""Sayi Bulma Oyunu
      
      1 ile 40 arasinda sayi secin
      
      
      
      
      
      """)

rastgele_sayi=random.randint(1,40)
tahmin_hakki=5
while True:
    
    
    tahmin=int(input("Tahmininiz: "))
    
    if (tahmin < rastgele_sayi):
        print("Bilgiler Dogrulaniyor......")
        time.sleep(1)
        print("Daha Yüksek Bir Sayi")
        tahmin_hakki-=1
    elif (tahmin > rastgele_sayi):
        print("Bilgiler Dogrulaniyor......")
        time.sleep(1)
        print("Daha Düşük Bir Sayi")
        tahmin_hakki-=1
    else:
        print("Bilgiler Sorgulaniyor......")
        time.sleep(1)
        print("Tebrikler!, Sayiniz: " ,rastgele_sayi)
        break
    if (tahmin_hakki==0):
        print("Tahmin Hakkiniz Bitti")
        time.sleep(1)
        print("Doğru Sayi: ",rastgele_sayi)
        break
    
