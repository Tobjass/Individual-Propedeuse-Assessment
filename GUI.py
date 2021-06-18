import tkinter as tk
from PIL import ImageTk, Image
from random import shuffle

# Grafical User Interface
def open_image(window, bestand, rotate, setting, row, column, padx, pady, sticky):
    image = Image.open(bestand)
    image = ImageTk.PhotoImage(image.rotate(180 if (rotate) else 0))

    label = tk.Label(window, image=image, background="#d6e0f5")
    label.image = image
    if setting == "grid":
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    elif setting == "place":
        label.place(x=70 * row if (column == 1) else 1320 + 73 * row, y=40 if (column == 1) else 780)

def stapels_maken(window, speler, stapels, stok):
    for column in range(1, 9):
        window.columnconfigure(column, weight=1, minsize=75)

        temp_column = 9 - column if (speler != 3) else column

        if temp_column == 1 or temp_column == 7 or temp_column == 8:
            frame = tk.Frame(master=window, relief=tk.RAISED, background="#d6e0f5")
            frame.grid(row=speler, column=column, padx=5, pady=40, ipadx=82.5, ipady=118.5,
                       sticky="n" if (speler == 1) else (None if (speler == 2) else "s"))

            if speler != 2 and temp_column == 1:
                label = tk.Label(master=window, text=len(stok), background="#d6e0f5",
                                 font=('Helvetica', 50, 'bold'))
                label.place(x=1640 if (speler == 1) else 200, y=125 if (speler == 1) else 845)
            continue

        # Trekstapel
        if speler == 2 and column == 7:
            open_image(window, "Images/Trekstapel.png", False, "grid", speler, column, 100, None, None)
        # Stok
        elif speler != 2 and temp_column == 2:
            open_image(window, "Images/{}/{} ({}).png".format(stok[0], stok[0], 5 if (len(stok) > 5) else len(stok)),
                       True if (speler == 1) else False, "grid", speler, column, 100, 40,
                       "n" if (speler == 1) else (None if (speler == 2) else "s"))
        # Bouw en weggooistapels
        else:
            keys = ['A', 'B', 'C', 'D']
            stapel = stapels[keys[6 - (9 - column if (speler != 1) else column)]]
            open_image(window, "Images/{}".format(
                "Lege stapel.png" if (len(stapel) == 0) else "{}/{} ({}).png".format(stapel[-1], stapel[-1], 1)),
                       True if (speler == 1) else False, "grid", speler, column, 5, 40,
                       "n" if (speler == 1) else (None if (speler == 2) else "s"))

def hand_maken(window, speler, hand):
    for kaart in range(1, len(hand) + 1):
        open_image(window, "Images/{}".format(
            "Omgedraaide kaart.png" if (speler == 1) else "{}/{} ({}).png".format(hand[kaart - 1], hand[kaart - 1], 1)),
                   True if (speler == 1) else False, "place", kaart, speler, None, None, None)

# Overige functies
def kaart_van_trekstapel(trekstapel, aantal):
    return trekstapel[:aantal], trekstapel[aantal:]

def instellen():
    trekstapel = [x % 12 + 1 for x in range(0, 144)]
    trekstapel += ["SB"] * 18
    shuffle(trekstapel)

    bouwstapels = {'A': [1, 2, 3], 'B': [1, 2, 3, 4, 5, 6], 'C': [1, 2, 3, 4, 5, 7, 8, 9], 'D': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
    mens_weggooistapels = {'A': [9], 'B': [10], 'C': [11], 'D': [12]}
    comp_weggooistapels = {'A': [1], 'B': [2], 'C': [3], 'D': [4]}

    mens_stok, trekstapel = kaart_van_trekstapel(trekstapel, 30)
    comp_stok, trekstapel = kaart_van_trekstapel(trekstapel, 30)
    mens_hand, trekstapel = kaart_van_trekstapel(trekstapel, 5)

    return trekstapel, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand

# Main functie
def run(window):
    window.configure(background="#d6e0f5")

    trekstapel, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand = instellen()

    for speler in range(1, 4):
        window.rowconfigure(speler, weight=1, minsize=50)

        stapels_maken(window, speler,
                      comp_weggooistapels if (speler == 1) else (bouwstapels if (speler == 2) else mens_weggooistapels),
                      comp_stok if (speler == 1) else mens_stok)

        if speler != 2:
            hand_maken(window, speler, mens_hand)

    window.mainloop()

run(tk.Tk(className=' Skip-Bo'))
