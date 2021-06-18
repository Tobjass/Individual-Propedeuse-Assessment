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

def stapels_maken(window, speler, bouwstapels, weggooistapels, stok):
    for stapel in range(1, 9):
        window.columnconfigure(stapel, weight=1, minsize=75)

        temp_stapel = 9 - stapel if (speler != 3) else stapel

        if temp_stapel == 1 or temp_stapel == 7 or temp_stapel == 8:
            frame = tk.Frame(master=window, relief=tk.RAISED, background="#d6e0f5")
            frame.grid(row=speler, column=stapel, padx=5, pady=40, ipadx=82.5, ipady=118.5,
                       sticky="n" if (speler == 1) else (None if (speler == 2) else "s"))

            if speler != 2 and temp_stapel == 1:
                label = tk.Label(master=window, text=len(stok), background="#d6e0f5",
                                 font=('Helvetica', 50, 'bold'))
                label.place(x=1640 if (speler == 1) else 200, y=125 if (speler == 1) else 845)
            continue

        if speler == 2 and stapel == 7:
            open_image(window, "Images/Trekstapel.png", False, "grid", speler, stapel, 100, None, None)
        elif speler != 2 and temp_stapel == 2:
            open_image(window, "Images/{}/{} ({}).png".format(stok[0], stok[0], 5 if (len(stok) > 5) else len(stok)),
                       True if (speler == 1) else False, "grid", speler, stapel, 100, 40,
                       "n" if (speler == 1) else (None if (speler == 2) else "s"))
        else:
            open_image(window, "Images/{}/{} ({}).png".format(stapel, stapel, 1), True if (speler == 1) else False,
                       "grid", speler, stapel, 5, 40, "n" if (speler == 1) else (None if (speler == 2) else "s"))

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

    bouwstapels = {'A': [], 'B': [], 'C': [], 'D': []}
    weggooistapels = {'A': [], 'B': [], 'C': [], 'D': []}

    mens_stok, trekstapel = kaart_van_trekstapel(trekstapel, 30)
    comp_stok, trekstapel = kaart_van_trekstapel(trekstapel, 30)
    mens_hand, trekstapel = kaart_van_trekstapel(trekstapel, 5)

    return trekstapel, bouwstapels, weggooistapels, mens_stok, comp_stok, mens_hand

# Main functie
def run(window):
    window.configure(background="#d6e0f5")

    trekstapel, bouwstapels, weggooistapels, mens_stok, comp_stok, mens_hand = instellen()

    for speler in range(1, 4):
        window.rowconfigure(speler, weight=1, minsize=50)

        stapels_maken(window, speler, bouwstapels, weggooistapels, comp_stok if (speler == 1) else mens_stok)

        if speler != 2:
            hand_maken(window, speler, mens_hand)

    window.mainloop()

run(tk.Tk(className=' Skip-Bo'))
