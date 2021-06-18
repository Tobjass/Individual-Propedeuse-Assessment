import tkinter as tk
from PIL import ImageTk, Image

def run(window, bovenste_kaart_stok, aantal_kaarten_stok, aantal_kaarten_hand):
    window.configure(background="#d6e0f5")

    for speler in range(1, 4):
        window.rowconfigure(speler, weight=1, minsize=50)

        stapels_aanmaken(window, speler, bovenste_kaart_stok, aantal_kaarten_stok, 7 + aantal_kaarten_hand, 1, 9, 1)

    window.mainloop()

def stapels_aanmaken(window, speler, bovenste_kaart_stok, aantal_kaarten_stok, aantal_kaarten_hand, start, stop, step):
    for stapel in range(start, stop, step):
        window.columnconfigure(stapel, weight=1, minsize=75)

        temp_stapel = stop - stapel if (speler != 3) else stapel

        if temp_stapel == 1 or temp_stapel == 7 or temp_stapel == 8:
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                background="#d6e0f5"
            )
            frame.grid(row=speler, column=stapel, padx=5, pady=40, ipadx=82.5, ipady=118.5,
                       sticky="n" if (speler == 1) else (None if (speler == 2) else "s"))
            continue

        if speler == 2 and stapel == 7:
            image = ImageTk.PhotoImage(Image.open("Images/Trekstapel.png"))

            label = tk.Label(window, image=image, background="#d6e0f5")
            label.image = image
            label.grid(row=speler, column=stapel, padx=100)
        elif speler != 2 and temp_stapel == 2:
            image = Image.open("Images/{}/{} ({}).png".format(bovenste_kaart_stok, bovenste_kaart_stok,
                                                      5 if (aantal_kaarten_stok > 5) else aantal_kaarten_stok))
            image = ImageTk.PhotoImage(image.rotate(180 if (speler == 1) else 0))

            label = tk.Label(window, image=image, background="#d6e0f5")
            label.image = image
            label.grid(row=speler, column=stapel, padx=100, pady=40,
                       sticky="n" if (speler == 1) else (None if (speler == 2) else "s"))
        else:
            image = Image.open("Images/{}/{} ({}).png".format(1, 1, 1))
            image = ImageTk.PhotoImage(image.rotate(180 if (speler == 1) else 0))

            label = tk.Label(window, image=image, background="#d6e0f5")
            label.image = image
            label.grid(row=speler, column=stapel, padx=5, pady=40,
                       sticky="n" if (speler == 1) else (None if (speler == 2) else "s"))

run(tk.Tk(className=' Skip-Bo'), 6, 30, 0)
