import tkinter as tk
from PIL import ImageTk, Image
from random import shuffle
from pyautogui import position

# Grafical User Interface
def check_widget(hand, x, stapel_x, stapel_y):
    print(x)

    weggooistapel_posities = [586, 779, 971, 972, 1163]
    if x == 298:
        index = 5
    elif x in weggooistapel_posities:
        index = 6 + weggooistapel_posities.index(x)
    else:
        hand_posities = [[1357, 1448, 1539, 1630, 1721], [1403, 1494, 1585, 1676], [1448, 1539, 1630], [1494, 1585], [1539]]

        if x in hand_posities[5 - len(hand)]:
            index = hand_posities[5 - len(hand)].index(x)

    stapelposities = [[590, 750, 422, 658], [780, 944, 422, 658], [975, 1137, 422, 658], [1165, 1331, 422, 658],
                [589, 749, 799, 1039], [780, 943, 799, 1039], [972, 1137, 799, 1039], [1165, 1330, 799, 1039]]
    for stapel in stapelposities:
        if stapel[0] <= stapel_x <= stapel[1] and stapel[2] <= stapel_y <= stapel[3]:
            return index, stapelposities.index(stapel)
    return -1, -1

def drag(widget, window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, trekstapel):
    widget.bind("<ButtonRelease-1>",
                lambda event: on_drop(event, window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok,
                                      comp_stok, mens_hand, comp_hand, trekstapel))
    widget.configure(cursor="hand2")

def on_drop(event, window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, trekstapel):
    x, y = event.widget.winfo_pointerxy()
    target = event.widget.winfo_containing(x, y)

    # try:
    target.configure(image=event.widget.cget("image"))

    x, y = position()
    index, stapel = check_widget(mens_hand, event.widget.winfo_x(), x, y)

    keys = ['A', 'B', 'C', 'D']
    mens_beurt = True

    if index == 5:
        if bovenste_kaart_bouwstapel(bouwstapels[keys[stapel]]) + 1 == mens_stok[0] or mens_stok[0] == "SB":
            print("Kaart {} uit de stok naar bouwstapel {}".format(mens_stok[0], keys[stapel]))
            bouwstapels[keys[stapel]].append(mens_stok[0])
            mens_stok = mens_stok[1:]
    elif index >= 6:
        if bovenste_kaart_bouwstapel(bouwstapels[keys[stapel]]) + 1 == mens_weggooistapels[keys[index - 6]][-1] or \
                mens_weggooistapels[keys[index - 6]][-1] == "SB":
            print("Kaart {} uit weggooistapel {} naar bouwstapel {}".format(mens_weggooistapels[keys[index - 6]][-1],
                                                                            keys[index - 6], keys[stapel]))
            bouwstapels[keys[stapel]].append(mens_weggooistapels[keys[index - 6]][-1])
            mens_weggooistapels[keys[index - 6]] = mens_weggooistapels[keys[index - 6]][:-1]
    elif stapel <= 3 and index < 5:
        if bovenste_kaart_bouwstapel(bouwstapels[keys[stapel]]) + 1 == mens_hand[index] or mens_hand[index] == "SB":
            print("Kaart {} uit de hand naar bouwstapel {}".format(mens_hand[index], keys[stapel]))
            bouwstapels[keys[stapel]].append(mens_hand[index])
            mens_hand = mens_hand[:index] + mens_hand[index + 1:]
    elif 4 <= stapel <= 7 and index < 5:
        mens_beurt = False
        print("Kaart {} uit de hand naar weggooistapel {}".format(mens_hand[index], keys[stapel - 4]))
        mens_weggooistapels[keys[stapel - 4]].append(mens_hand[index])
        mens_hand = mens_hand[:index] + mens_hand[index + 1:]

    window.destroy()
    window = tk.Tk(className=' Skip-Bo')
    update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel)
    # except:
    #     pass

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

def mogelijkheid(kaart, bouwstapels):
    for stapel in bouwstapels:
        if bovenste_kaart_bouwstapel(bouwstapels[stapel]) + 1 == kaart or kaart == "SB":
            return True
    return False

def stapels_maken(window, speler, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel):
    stapels = comp_weggooistapels if (speler == 1) else (bouwstapels if (speler == 2) else mens_weggooistapels)
    stok = comp_stok if (speler == 1) else mens_stok

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
            label = open_image(window,
                               "Images/{}/{} ({}).png".format(stok[0], stok[0], 5 if (len(stok) > 5) else len(stok)),
                               True if (speler == 1) else False, "grid", speler, column, 100, 40,
                               "n" if (speler == 1) else (None if (speler == 2) else "s"))
            if speler == 3 and mogelijkheid(stok[0], bouwstapels) and mens_beurt:
                hover(label, "red", "#d6e0f5")
                drag(label, window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok,
                     mens_hand, comp_hand, trekstapel)
        # Bouw en weggooistapels
        else:
            stapel = stapels[['A', 'B', 'C', 'D'][6 - (9 - column if (speler != 1) else column)]]
            label = open_image(window, "Images/{}".format(
                "Lege stapel.png" if (len(stapel) == 0) else "{}/{} ({}).png".format(stapel[-1], stapel[-1],
                                                                                     5 if (len(stapel) > 5) else len(
                                                                                         stapel))),
                               True if (speler == 1) else False, "grid", speler, column, 5, 40,
                               "n" if (speler == 1) else (None if (speler == 2) else "s"))
            if speler == 3 and (len(stapel) > 0 and mogelijkheid(stapel[-1], bouwstapels)) and mens_beurt:
                hover(label, "red", "#d6e0f5")
                drag(label, window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok,
                     mens_hand, comp_hand, trekstapel)

def hand_maken(window, speler, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel):
    hand = comp_hand if (speler == 1) else mens_hand
    for kaart in range(1, len(hand) + 1):
        label = open_image(window, "Images/{}".format(
            "Omgedraaide kaart.png" if (speler == 1) else "{}/{} ({}).png".format(hand[kaart - 1], hand[kaart - 1], 1)),
                   True if (speler == 1) else False, "place", kaart, speler, len(hand), None, None)
        if speler == 3 and mens_beurt:
            hover(label, "red", "#d6e0f5")
            drag(label, window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, trekstapel)

def update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel):
    check_bouwstapels(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel)

    if len(mens_hand) == 0:
        mens_hand, trekstapel = trek_kaarten(mens_hand, trekstapel)

        window.destroy()
        window = tk.Tk(className=' Skip-Bo')
        update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand,
                   comp_hand, True, trekstapel)

    window.attributes('-fullscreen', True)
    window.configure(background="#d6e0f5")

    for speler in range(1, 4):
        window.rowconfigure(speler, weight=1, minsize=50)

        stapels_maken(window, speler, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok,
                      mens_hand, comp_hand, mens_beurt, trekstapel)

        if (speler == 1 and len(comp_hand) > 0) or (speler == 3 and len(mens_hand) > 0):
            hand_maken(window, speler, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel)

    if mens_beurt is False:
        run_algoritme(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel)

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

def trek_kaarten(hand, trekstapel):
    index = 5 - len(hand)
    if index > 0:
        for kaart in trekstapel[:index]:
            hand.append(kaart)
        trekstapel = trekstapel[index:]
    return hand, trekstapel

def check_bouwstapels(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel):
    for stapel in bouwstapels:
        if bovenste_kaart_bouwstapel(bouwstapels[stapel]) == 12:
            print("\nBouwstapel {} heeft 12 behaald en wordt geleegd".format(stapel))
            for kaart in bouwstapels[stapel]:
                trekstapel.append(kaart)
            shuffle(trekstapel)
            bouwstapels[stapel] = []

            update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel)

# Algoritme
def run_algoritme(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel):
    comp_hand, trekstapel = trek_kaarten(comp_hand, trekstapel)

    while True:
        if len(comp_hand) == 0:
            comp_hand, trekstapel = trek_kaarten(comp_hand, trekstapel)

        dichtste_bij = dichtste_bij_stok(bouwstapels, comp_stok, comp_hand, comp_weggooistapels)
        pad = pad_maken(bouwstapels, comp_stok, comp_hand, comp_weggooistapels)

        print(
            "\nStok: {}   ({})\nBouwstapels: {}\nHand: {}\nWeggooistapels: {}\n\nBouwstapel {} is het dichtste bij de stok\nPad: {}\n".format(
                comp_stok[0], len(comp_stok), bouwstapels, comp_hand, comp_weggooistapels, dichtste_bij, pad))

        if not pad:
            break

        bouwstapels[dichtste_bij], comp_stok, comp_hand, comp_weggooistapels = pad_toepassen(pad,
                                                                                             bouwstapels[dichtste_bij],
                                                                                             comp_stok, comp_hand,
                                                                                             comp_weggooistapels)

        print("Na toepassen van pad:\n\nStok: {}   ({})\nBouwstapels: {}\nHand: {}\nWeggooistapels: {}".format(
            comp_stok[0], len(comp_stok), bouwstapels, comp_hand, comp_weggooistapels))

    comp_hand, comp_weggooistapels = kaart_wegleggen(comp_hand, comp_weggooistapels)

    mens_hand, trekstapel = trek_kaarten(mens_hand, trekstapel)

    window.destroy()
    window = tk.Tk(className=' Skip-Bo')
    update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand,
               comp_hand, True, trekstapel)

def kleinste_weggooistapel(weggooistapels):
    if len(weggooistapels['A']) == len(weggooistapels['B']) and len(weggooistapels['B']) == len(weggooistapels['C']) and len(weggooistapels['C']) == len(weggooistapels['D']):
        return 'A'
    len_kleinste = 100
    kleinste = None
    for stapel in weggooistapels:
        if len(weggooistapels[stapel]) < len_kleinste:
            len_kleinste = len(weggooistapels[stapel])
            kleinste = stapel
    return kleinste

def check_weggooistapel(stapel):
    gelijk = stapel[-1]
    for kaart in stapel:
        if kaart != gelijk:
            return False
    return True

def kaart_wegleggen(hand, weggooistapels):
    index = None
    for optie in range(4):
        for stapel in weggooistapels:
            if optie == 0 and (len(weggooistapels[stapel]) > 0 and (check_weggooistapel(weggooistapels[stapel]) and weggooistapels[stapel][-1] in hand)):
                index = hand.index(weggooistapels[stapel][-1])
                break
            elif optie == 1 and len(weggooistapels[stapel]) == 0:
                for handoptie in range(2):
                    for kaart in hand:
                        if (handoptie == 0 and (hand.count(kaart) > 1 and kaart != "SB")) or handoptie == 1 and kaart != "SB":
                            index = hand.index(kaart)
                            break
                    if index is not None:
                        break
                break
            elif optie == 2 and (len(weggooistapels[stapel]) > 0 and weggooistapels[stapel][-1] - 1 in hand):
                index = hand.index(weggooistapels[stapel][-1] - 1)
                break
            elif optie == 3:
                index = 0
                for kaart in hand:
                    if kaart != "SB":
                        index = hand.index(kaart)
                        break
                print("Kaart {} wordt naar weggooistapel {} verplaatst\n\n".format(hand[index], kleinste_weggooistapel(weggooistapels)))
                weggooistapels[kleinste_weggooistapel(weggooistapels)].append(hand[index])
                hand = hand[:index] + hand[index + 1:]
                return hand, weggooistapels
        if index is not None:
            break
    print("Kaart {} wordt naar weggooistapel {} verplaatst\n\n".format(hand[index], stapel))
    weggooistapels[stapel].append(hand[index])
    hand = hand[:index] + hand[index + 1:]
    return hand, weggooistapels

def check_weggooistapels(weggooistapels, kaart):
    for stapel in weggooistapels:
        if not weggooistapels[stapel]:
            continue
        if weggooistapels[stapel][-1] == kaart:
            return True, stapel
    return False, None

def beschikbare_kaarten(hand, weggooistapels):
    temp = hand.copy()
    for stapel in weggooistapels:
        if len(weggooistapels[stapel]) > 0:
            temp.append(weggooistapels[stapel][-1])
    return temp

def dichtste_bij_stok(bouwstapels, stok, hand, weggooistapels):
    if stok[0] == 'SB':
        for stapel in bouwstapels:
            if bovenste_kaart_bouwstapel(bouwstapels[stapel]) + 1 in beschikbare_kaarten(hand, weggooistapels):
                continue
            elif bovenste_kaart_bouwstapel(bouwstapels[stapel]) + 1 not in beschikbare_kaarten(hand, weggooistapels):
                return stapel

    kleinste_verschil = 13
    for stapel in bouwstapels:
        verschil = stok[0] - bovenste_kaart_bouwstapel(bouwstapels[stapel])
        if verschil <= 0:
            verschil += 12
        if verschil < kleinste_verschil:
            kleinste_verschil = verschil
            meest_dichtbij = stapel
    return meest_dichtbij

def pad_maken(bouwstapels, stok, hand, weggooistapels):
    if stok[0] == "SB":
        return [["stok", 0]]

    dichtste_bij = dichtste_bij_stok(bouwstapels, stok, hand, weggooistapels)
    bovenste = bovenste_kaart_bouwstapel(bouwstapels[dichtste_bij])
    verschil = stok[0] - bovenste + 1

    if verschil < 0:
        verschil += 11

    temp_hand = hand.copy()
    temp_weggooistapels = weggooistapels.copy()

    pad = []
    for kaart in range(1, verschil):
        if bovenste + kaart == stok[0]:
            pad.append(["stok", 0])
            break
        if bovenste + kaart in temp_hand:
            pad.append(["hand", temp_hand.index(bovenste + kaart)])
            temp_hand.remove(bovenste + kaart)
            continue
        weggooistapel = check_weggooistapels(temp_weggooistapels, bovenste + kaart)
        if weggooistapel[0]:
            pad.append(["weggooistapel", weggooistapel[1]])
            temp_weggooistapels[weggooistapel[1]] = temp_weggooistapels[weggooistapel[1]][:-1]
            continue
        elif "SB" in temp_hand:
            pad.append(["hand", temp_hand.index("SB")])
            temp_hand.remove("SB")
            continue
        break
    return pad

def pad_toepassen(pad, bouwstapel, stok, hand, weggooistapels):
    for stap in pad:
        if stap[0] == "stok":
            bouwstapel.append(stok[stap[1]])
            stok = stok[1:]
        elif stap[0] == "hand":
            bouwstapel.append(hand[stap[1]])
            hand = hand[:stap[1]] + hand[stap[1] + 1:]
        elif stap[0] == "weggooistapel":
            bouwstapel.append(weggooistapels[stap[1]][-1])
            weggooistapels[stap[1]] = weggooistapels[stap[1]][:-1]
    return bouwstapel, stok, hand, weggooistapels

# Main functie
def run(window):
    trekstapel, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand = instellen()

    update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, True, trekstapel)

    window.mainloop()

run(tk.Tk(className=' Skip-Bo'))
