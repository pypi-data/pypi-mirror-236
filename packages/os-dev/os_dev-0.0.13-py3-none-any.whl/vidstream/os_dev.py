import time
import os
GUI = "No GUI selected..."
GUI2 = "noth"
users_cpu = "Intel Core i9-12900K"
users_ram = "CORSAIR Vengeance RGB 64GB (4 x 16GB) 288-Pin PC RAM DDR5 5600 (PC5 44800) Desktop Memory Model CMH64GX5M4B5600C36"
def boot(usercpu, userram):
    print("Booting using CPU: " + usercpu)
    time.sleep(2)
    print("Botting Using RAM: " + userram)
    time.sleep(3)
    print("Booted!")
    time.sleep(0.5)
    if GUI == "Windows 10":
        print("Booting from windows 10 GUI...")
        time.sleep(3)
        os.system("cls")
        print("              Welcome to Windows 10!")
        print("             No GUI left...")
    else:
        print("GUI: " + GUI + " Error: No GUI to boot from.")
        time.sleep(100)
    
    var = input(">> ")
    if var == "EXIT" or "exit":
        exit()