import tkinter as tk
from PIL import ImageTk, Image

def run(window, bovenste_kaart_stok, aantal_kaarten_stok, aantal_kaarten_hand):
    window.configure(background="#d6e0f5")

    for speler in range(1, 4):
        window.rowconfigure(speler, weight=1, minsize=50)

        stapels_aanmaken(window, speler, bovenste_kaart_stok, aantal_kaarten_stok, 7 + aantal_kaarten_hand, 1, 9, 1)

        if speler != 2:
            hand_aanmaken(window, speler, [8, 3, 1, "SB", 11])

    window.mainloop()

def open_image(window, bestand, rotate, setting, row, column, padx, pady, sticky):
    image = Image.open(bestand)
    image = ImageTk.PhotoImage(image.rotate(180 if (rotate) else 0))

    label = tk.Label(window, image=image, background="#d6e0f5")
    label.image = image
    if setting == "grid":
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    elif setting == "place":
        label.place(x=70 * row if (column == 1) else 1320 + 73 * row, y=40 if (column == 1) else 780)

def stapels_aanmaken(window, speler, bovenste_kaart_stok, aantal_kaarten_stok, aantal_kaarten_hand, start, stop, step):
    for stapel in range(start, stop, step):
        window.columnconfigure(stapel, weight=1, minsize=75)

        temp_stapel = stop - stapel if (speler != 3) else stapel

        if temp_stapel == 1 or temp_stapel == 7 or temp_stapel == 8:
            frame = tk.Frame(master=window, relief=tk.RAISED, background="#d6e0f5")
            frame.grid(row=speler, column=stapel, padx=5, pady=40, ipadx=82.5, ipady=118.5,
                       sticky="n" if (speler == 1) else (None if (speler == 2) else "s"))

            if speler != 2 and temp_stapel == 1:
                label = tk.Label(master=window, text=aantal_kaarten_stok, background="#d6e0f5",
                                 font=('Helvetica', 50, 'bold'))
                label.place(x=1640 if (speler == 1) else 200, y=125 if (speler == 1) else 845)
            continue

        if speler == 2 and stapel == 7:
            open_image(window, "Images/Trekstapel.png", False, "grid", speler, stapel, 100, None, None)
        elif speler != 2 and temp_stapel == 2:
            open_image(window, "Images/{}/{} ({}).png".format(bovenste_kaart_stok, bovenste_kaart_stok,
                                                              5 if (aantal_kaarten_stok > 5) else aantal_kaarten_stok),
                       True if (speler == 1) else False, "grid", speler, stapel, 100, 40,
                       "n" if (speler == 1) else (None if (speler == 2) else "s"))
        else:
            open_image(window, "Images/{}/{} ({}).png".format(stapel, stapel, 1), True if (speler == 1) else False,
                       "grid", speler, stapel, 5, 40, "n" if (speler == 1) else (None if (speler == 2) else "s"))

def hand_aanmaken(window, speler, hand):
    for kaart in range(1, len(hand) + 1):
        open_image(window, "Images/{}".format(
            "Omgedraaide kaart.png" if (speler == 1) else "{}/{} ({}).png".format(hand[kaart - 1], hand[kaart - 1], 1)),
                   True if (speler == 1) else False, "place", kaart, speler, None, None, None)

run(tk.Tk(className=' Skip-Bo'), 10, 30, 0)
