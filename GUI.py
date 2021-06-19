import tkinter as tk
from PIL import ImageTk, Image
from random import shuffle
import pyautogui

# Grafical User Interface
def check_widget(hand_x, stapel_x, stapel_y):
    hand_posities = [[1357, 1448, 1539, 1630, 1721], [1403, 1494, 1585, 1676], [1448, 1539, 1630], [1494, 1585], [1539]]

    for positie in range(5):
        hand_index = None
        for kaart_pos in hand_posities[positie]:
            if kaart_pos == hand_x:
                hand_index = hand_posities[positie].index(hand_x)
                break
        if hand_index is not None:
            break

    posities = [[590, 750, 422, 658], [780, 944, 422, 658], [975, 1137, 422, 658], [1165, 1331, 422, 658],
                [589, 749, 799, 1039], [780, 943, 799, 1039], [972, 1137, 799, 1039], [1165, 1330, 799, 1039]]

    for stapel in posities:
        if stapel[0] <= stapel_x <= stapel[1] and stapel[2] <= stapel_y <= stapel[3]:
            return hand_index, posities.index(stapel)

def drag(widget):
    widget.bind("<ButtonRelease-1>", on_drop)
    widget.configure(cursor="hand2")

def on_drop(event):
    x, y = event.widget.winfo_pointerxy()
    target = event.widget.winfo_containing(x, y)

    try:
        x, y = pyautogui.position()
        hand_index, stapel = check_widget(event.widget.winfo_x(), x, y)
        keys = ['A', 'B', 'C', 'D']
        stapel = ["Bouwstapel", keys[stapel]] if (stapel <= 3) else (
            ["Weggooistapel", keys[stapel - 4]] if (4 <= stapel <= 7) else None)

        target.configure(image=event.widget.cget("image"))

        return hand_index, stapel
    except:
        pass

def mogelijkheid(kaart, bouwstapels):
    for stapel in bouwstapels:
        if bovenste_kaart_bouwstapel(bouwstapels[stapel]) + 1 == kaart or kaart == "SB":
            return True
    return False

def hover(label, on_hover, on_leave):
    label.bind("<Enter>", func=lambda x: label.config(background=on_hover))
    label.bind("<Leave>", func=lambda x: label.config(background=on_leave))

def open_image(window, bestand, rotate, setting, row, column, padx, pady, sticky):
    image = Image.open(bestand)
    image = ImageTk.PhotoImage(image.rotate(180 if (rotate) else 0))

    label = tk.Label(window, image=image, background="#d6e0f5")
    label.image = image
    if setting == "grid":
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    elif setting == "place":
        label.place(x=-63 + 45.5 * (5 - padx) + 91 * row if (column == 1) else 1266 + 45.5 * (5 - padx) + 91 * row, y=40 if (column == 1) else 801)
    return label

def stapels_maken(window, speler, bouwstapels, stapels, stok):
    for column in range(1, 9):
        window.columnconfigure(column, weight=1, minsize=75)

        temp_column = 9 - column if (speler != 3) else column

        if temp_column in [1, 7, 8]:
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
            label = open_image(window, "Images/{}/{} ({}).png".format(stok[0], stok[0], 5 if (len(stok) > 5) else len(stok)),
                       True if (speler == 1) else False, "grid", speler, column, 100, 40,
                       "n" if (speler == 1) else (None if (speler == 2) else "s"))
            if speler == 3 and mogelijkheid(stok[0], bouwstapels):
                hover(label, "red", "#d6e0f5")
        # Bouw en weggooistapels
        else:
            stapel = stapels[['A', 'B', 'C', 'D'][6 - (9 - column if (speler != 1) else column)]]
            label = open_image(window, "Images/{}".format(
                "Lege stapel.png" if (len(stapel) == 0) else "{}/{} ({}).png".format(stapel[-1], stapel[-1],
                                                                                     5 if (len(stapel) > 5) else len(
                                                                                         stapel))),
                               True if (speler == 1) else False, "grid", speler, column, 5, 40,
                               "n" if (speler == 1) else (None if (speler == 2) else "s"))
            if speler == 3 and (len(stapel) > 0 and mogelijkheid(stapel[-1], bouwstapels)):
                hover(label, "red", "#d6e0f5")

def hand_maken(window, speler, hand):
    for kaart in range(1, len(hand) + 1):
        label = open_image(window, "Images/{}".format(
            "Omgedraaide kaart.png" if (speler == 1) else "{}/{} ({}).png".format(hand[kaart - 1], hand[kaart - 1], 1)),
                   True if (speler == 1) else False, "place", kaart, speler, len(hand), None, None)
        if speler == 3:
            hover(label, "red", "#d6e0f5")
            drag(label)

def update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand):
    window.attributes('-fullscreen', True)
    for speler in range(1, 4):
        window.rowconfigure(speler, weight=1, minsize=50)

        stapels_maken(window, speler, bouwstapels,
                      comp_weggooistapels if (speler == 1) else (bouwstapels if (speler == 2) else mens_weggooistapels),
                      comp_stok if (speler == 1) else mens_stok)

        if (speler == 1 and len(comp_hand) > 0) or (speler == 3 and len(mens_hand) > 0):
            hand_maken(window, speler, comp_hand if (speler == 1) else mens_hand)

# Overige functies
def kaart_van_trekstapel(trekstapel, aantal):
    return trekstapel[:aantal], trekstapel[aantal:]

def instellen():
    trekstapel = [x % 12 + 1 for x in range(0, 144)]
    trekstapel += ["SB"] * 18
    shuffle(trekstapel)

    bouwstapels = {'A': [],  'B': [], 'C': [], 'D': []}
    mens_weggooistapels = {'A': [], 'B': [], 'C': [], 'D': []}
    comp_weggooistapels = {'A': [], 'B': [], 'C': [], 'D': []}

    mens_stok, trekstapel = kaart_van_trekstapel(trekstapel, 30)
    comp_stok, trekstapel = kaart_van_trekstapel(trekstapel, 30)
    mens_hand, trekstapel = kaart_van_trekstapel(trekstapel, 5)

    return trekstapel, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, []

def bovenste_kaart_bouwstapel(bouwstapel):
    if not bouwstapel:
        return 0
    elif len(bouwstapel) == 1:
        return 1
    elif bouwstapel[-1] == "SB":
        return bovenste_kaart_bouwstapel(bouwstapel[:-1]) + 1
    else:
        return bouwstapel[-1]

# Main functie
def run(window):
    window.configure(background="#d6e0f5")

    trekstapel, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand = instellen()

    update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand)

    window.mainloop()

run(tk.Tk(className=' Skip-Bo'))
