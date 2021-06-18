import tkinter as tk
from PIL import ImageTk, Image

def run(window, bovenste_kaart_stok, aantal_kaarten_stok, aantal_kaarten_hand):
    window.configure(background="#d6e0f5")

    for speler in range(1, 4):
        window.rowconfigure(speler, weight=1, minsize=50)

        stapels_aanmaken(window, speler, bovenste_kaart_stok, aantal_kaarten_stok, 7 + aantal_kaarten_hand, 1, 9, 1)

        if speler != 2:
            hand_aanmaken(window, speler, [2, 4, 6, 9, "SB"])

    window.mainloop()

def open_image(window, bestand, rotate, row, column, padx, pady, sticky):
    image = Image.open(bestand)
    image = ImageTk.PhotoImage(image.rotate(180 if (rotate) else 0))

    label = tk.Label(window, image=image, background="#d6e0f5")
    label.image = image
    label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

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
            open_image(window, "Images/Trekstapel.png", False, speler, stapel, 100, None, None)
        elif speler != 2 and temp_stapel == 2:
            open_image(window, "Images/{}/{} ({}).png".format(bovenste_kaart_stok, bovenste_kaart_stok,
                                                              5 if (aantal_kaarten_stok > 5) else aantal_kaarten_stok),
                       True if (speler == 1) else False, speler, stapel, 100, 40,
                       "n" if (speler == 1) else (None if (speler == 2) else "s"))
        else:
            open_image(window, "Images/{}/{} ({}).png".format(stapel, stapel, 1), True if (speler == 1) else False,
                       speler, stapel, 5, 40, "n" if (speler == 1) else (None if (speler == 2) else "s"))

def hand_aanmaken(window, speler, hand):
    for kaart in range(1, len(hand) + 1):
        image = Image.open("Images/{}/{} ({}).png".format(hand[kaart - 1], hand[kaart - 1], 1))
        image = ImageTk.PhotoImage(image.rotate(180 if (speler == 1) else 0))

        label = tk.Label(window, image=image, background="#d6e0f5")
        label.image = image
        label.place(x=70 * kaart if (speler == 1) else 1320 + 73 * kaart, y=40 if (speler == 1) else 780)

run(tk.Tk(className=' Skip-Bo'), 11, 30, 0)
