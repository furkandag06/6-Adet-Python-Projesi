print("Boy kilo endeksi programi")


boy=float(input("Boy (m): "))

kilo=float(input("Kilo(Kg): "))

endeks=kilo/(boy*boy)
print("Endeksiniz:",endeks)

if endeks <= 18:
    print("Zayif")
elif endeks >18 and endeks <=25:
    print("Normal")
elif endeks >25 and endeks <=30:
    print("Kilolu")
elif endeks >30:
    print("Obez")
    


    

