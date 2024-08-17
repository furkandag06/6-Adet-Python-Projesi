enaz=int(input("Min: "))
enfazla=int(input("Max: "))

for sayi in range(enaz, enfazla - 1):
    toplam = 0
    for n in range(1,sayi - 1):
        if sayi % n==0:
            toplam = toplam + n
    if (toplam==sayi):
        print("%d " %sayi)
        