import tkinter as tk
from PIL import ImageTk, Image
from random import shuffle
from pyautogui import position

# Grafical User Interface
"""
Controleert waar de gesleepte kaart vandaan komt en op welke stapel deze moet komen te liggen d.m.v. x en y coördinaten.
"""
def check_widget(hand, x, stapel_x, stapel_y):
    weggooistapel_posities = [[584, 585, 586, 587, 588], [777, 778, 779, 780, 781], [969, 970, 971, 972, 973],
                              [1161, 1162, 1163, 1164, 1165]]

    if x == 298:
        index = 5
    elif x in weggooistapel_posities[0] + weggooistapel_posities[1] + weggooistapel_posities[2] + \
            weggooistapel_posities[3]:
        for weggooistapel in weggooistapel_posities:
            if x in weggooistapel:
                index = 6 + weggooistapel_posities.index(weggooistapel)
    else:
        hand_posities = [[1357, 1448, 1539, 1630, 1721], [1403, 1494, 1585, 1676], [1448, 1539, 1630], [1494, 1585],
                         [1539]]

        if x in hand_posities[5 - len(hand)]:
            index = hand_posities[5 - len(hand)].index(x)

    stapelposities = [[590, 750, 422, 658], [780, 944, 422, 658], [975, 1137, 422, 658], [1165, 1331, 422, 658],
                      [589, 749, 799, 1039], [780, 943, 799, 1039], [972, 1137, 799, 1039], [1165, 1330, 799, 1039]]
    for stapel in stapelposities:
        if stapel[0] <= stapel_x <= stapel[1] and stapel[2] <= stapel_y <= stapel[3]:
            return index, stapelposities.index(stapel)
    return -1, -1

"""
Maakt een widget sleepbaar.
"""
def drag(widget, window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, trekstapel):
    widget.bind("<ButtonRelease-1>",
                lambda event: on_drop(event, window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok,
                                      comp_stok, mens_hand, comp_hand, trekstapel))
    widget.configure(cursor="hand2")

"""
Legt d.m.v. check_widget() de gesleepte kaart op de juiste stapel, en update de GUI daarna.
"""
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
            print("(Speler)   Kaart {} uit stok naar bouwstapel {}".format(mens_stok[0], keys[stapel]))
            bouwstapels[keys[stapel]].append(mens_stok[0])
            mens_stok = mens_stok[1:]
    elif index >= 6:
        if bovenste_kaart_bouwstapel(bouwstapels[keys[stapel]]) + 1 == mens_weggooistapels[keys[index - 6]][-1] or \
                mens_weggooistapels[keys[index - 6]][-1] == "SB":
            print("(Speler)   Kaart {} uit weggooistapel {} naar bouwstapel {}"
                  .format(mens_weggooistapels[keys[index - 6]][-1], keys[index - 6], keys[stapel]))
            bouwstapels[keys[stapel]].append(mens_weggooistapels[keys[index - 6]][-1])
            mens_weggooistapels[keys[index - 6]] = mens_weggooistapels[keys[index - 6]][:-1]
    elif stapel <= 3 and index < 5:
        if bovenste_kaart_bouwstapel(bouwstapels[keys[stapel]]) + 1 == mens_hand[index] or mens_hand[index] == "SB":
            print("(Speler)   Kaart {} uit hand naar bouwstapel {}".format(mens_hand[index], keys[stapel]))
            bouwstapels[keys[stapel]].append(mens_hand[index])
            mens_hand = mens_hand[:index] + mens_hand[index + 1:]
    elif 4 <= stapel <= 7 and index < 5:
        mens_beurt = False
        print("(Speler)   Kaart {} uit hand naar weggooistapel {}\n".format(mens_hand[index], keys[stapel - 4]))
        mens_weggooistapels[keys[stapel - 4]].append(mens_hand[index])
        mens_hand = mens_hand[:index] + mens_hand[index + 1:]

    window.destroy()
    window = tk.Tk(className=' Skip-Bo')
    update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand,
               comp_hand, mens_beurt, trekstapel)
    # except:
    #     pass

"""
Maakt de achtergrond van een kaart rood als de muis er op zit.
"""
def hover(label, on_hover, on_leave):
    label.bind("<Enter>", func=lambda x: label.config(background=on_hover))
    label.bind("<Leave>", func=lambda x: label.config(background=on_leave))

"""
Opent een kaart-foto en past deze toe op de GUI
"""
def open_image(window, bestand, rotate, setting, row, column, padx, pady, sticky):
    image = Image.open(bestand)
    image = ImageTk.PhotoImage(image.rotate(180 if (rotate) else 0))

    label = tk.Label(window, image=image, background="#d6e0f5")
    label.image = image
    if setting == "grid":
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    elif setting == "place":
        label.place(x=-63 + 45.5 * (5 - padx) + 91 * row if (column == 1) else 1266 + 45.5 * (5 - padx) + 91 * row,
                    y=40 if (column == 1) else 801)
    return label

"""
Controleert of de kaart gebruikt kan worden.
"""
def mogelijkheid(kaart, bouwstapels):
    for stapel in bouwstapels:
        if bovenste_kaart_bouwstapel(bouwstapels[stapel]) + 1 == kaart or kaart == "SB":
            return True
    return False

"""
Het aanmaken van de stapels voor de GUI.
"""
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
                               "Images/{}".format("Lege stapel.png" if (len(stok) == 0) else "{}/{} ({}).png".format(
                                   stok[0], stok[0], 5 if (len(stok) > 5) else len(stok))),
                               True if (speler == 1) else False, "grid", speler, column, 100, 40,
                               "n" if (speler == 1) else (None if (speler == 2) else "s"))
            if mens_beurt and speler == 3 and mogelijkheid(stok[0], bouwstapels):
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

"""
Het aanmaken van de 5 (of minder) kaarten in de hand voor de GUI.
"""
def hand_maken(window, speler, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel):
    hand = comp_hand if (speler == 1) else mens_hand
    for kaart in range(1, len(hand) + 1):
        label = open_image(window, "Images/{}".format(
            "Omgedraaide kaart.png" if (speler == 1) else "{}/{} ({}).png".format(hand[kaart - 1], hand[kaart - 1], 1)),
                   True if (speler == 1) else False, "place", kaart, speler, len(hand), None, None)
        if speler == 3 and mens_beurt:
            hover(label, "red", "#d6e0f5")
            drag(label, window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand,
                 comp_hand, trekstapel)

"""
Het updaten van de GUI, deze bouwt de stapels en hand opnieuw op. Ook wordt het algoritme vanuit hier gebruikt als de 
beurt van de speler afgelopen is.
"""
def update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, mens_beurt, trekstapel):
    win = False
    if len(comp_stok) == 0 or len(mens_stok) == 0:
        win = True
        label = tk.Label(master=window, text="{} wint".format("Computer" if (len(comp_stok) == 0) else "      Jij"),
                         background="#d6e0f5", font=('Helvetica', 50, 'bold'))
        label.place(x=725, y=300)

    bouwstapels, trekstapel = check_bouwstapels(bouwstapels, trekstapel)

    if len(mens_hand) == 0 and mens_beurt and win is False:
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
                      mens_hand, comp_hand, True if (mens_beurt and win is False) else False, trekstapel)

        if (speler == 1 and len(comp_hand) > 0) or (speler == 3 and len(mens_hand) > 0):
            hand_maken(window, speler, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok,
                       mens_hand, comp_hand, True if (mens_beurt and win is False) else False, trekstapel)

    if mens_beurt is False and win is False:
        run_algoritme(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand,
                      comp_hand, trekstapel)

# Overige functies
"""
Bepaald aantal kaarten van de trekstapel af halen en aan een lijst toevoegen.
"""
def kaart_van_trekstapel(trekstapel, aantal):
    return trekstapel[:aantal], trekstapel[aantal:]

"""
Het instellen van de benodigde lijsten, d.m.v. shuffle() voor de trekstapel en kaart_van_trekstapel() voor de stok en 
mens_hand.
"""
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

"""
Returnt de bovenste kaart van de bouwstapel als int, ook als de bovenste een Skip-Bo kaart is.
"""
def bovenste_kaart_bouwstapel(bouwstapel):
    if not bouwstapel:
        return 0
    elif len(bouwstapel) == 1:
        return 1
    elif bouwstapel[-1] == "SB":
        return bovenste_kaart_bouwstapel(bouwstapel[:-1]) + 1
    else:
        return bouwstapel[-1]

"""
Voegt een aantal kaarten aan de hand toe om er weer 5 van te maken.
"""
def trek_kaarten(hand, trekstapel):
    index = 5 - len(hand)
    if index > 0:
        for kaart in trekstapel[:index]:
            hand.append(kaart)
        trekstapel = trekstapel[index:]
    return hand, trekstapel

"""
Controleert of een bouwstapel geleegd moet worden (als het 12 behaald heeft).
"""
def check_bouwstapels(bouwstapels, trekstapel):
    for stapel in bouwstapels:
        if bovenste_kaart_bouwstapel(bouwstapels[stapel]) == 12:
            print("\nBouwstapel {} heeft 12 behaald en wordt geleegd\n".format(stapel))
            for kaart in bouwstapels[stapel]:
                trekstapel.append(kaart)
            shuffle(trekstapel)
            bouwstapels[stapel] = []
    return bouwstapels, trekstapel

# Algoritme
"""
Runnen van het algoritme, hier wordt de hand bijgevuld, berekent welke stapel het dichtste bij de stok is, of er een pad 
mogelijk is, en zo ja deze toepassen. Als er geen pad meer mogelijk is wordt er een kaart afgelegd en is de mens weer 
aan de beurt.
"""
def run_algoritme(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand, trekstapel):
    comp_hand, trekstapel = trek_kaarten(comp_hand, trekstapel)

    mens_beurt = True
    while True:
        if len(comp_stok) == 0:
            mens_beurt = False
            break

        if len(comp_hand) == 0:
            comp_hand, trekstapel = trek_kaarten(comp_hand, trekstapel)

        dichtste_bij = dichtste_bij_stok(bouwstapels, comp_stok, comp_hand, comp_weggooistapels)
        pad = pad_maken(bouwstapels, mens_stok, comp_stok, comp_hand, comp_weggooistapels)

        if not pad:
            break

        bouwstapels, comp_stok, comp_hand, comp_weggooistapels, trekstapel = pad_toepassen(pad, bouwstapels,
            dichtste_bij, comp_stok, comp_hand, comp_weggooistapels, trekstapel)

    comp_hand, comp_weggooistapels = kaart_wegleggen(comp_hand, comp_weggooistapels)
    if len(comp_stok) > 0:
        mens_hand, trekstapel = trek_kaarten(mens_hand, trekstapel)

    window.destroy()
    window = tk.Tk(className=' Skip-Bo')
    update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand,
               comp_hand, mens_beurt, trekstapel)

"""
Berekent welke weggooistapel de minste kaarten heeft, om later een kaart op te kunnen gooien.
"""
def kleinste_weggooistapel(comp_weggooistapels):
    if len(comp_weggooistapels['A']) == len(comp_weggooistapels['B']) and len(comp_weggooistapels['B']) == len(
            comp_weggooistapels['C']) and len(comp_weggooistapels['C']) == len(comp_weggooistapels['D']):
        return 'A'
    len_kleinste = 100
    kleinste = None
    for stapel in comp_weggooistapels:
        if len(comp_weggooistapels[stapel]) < len_kleinste:
            len_kleinste = len(comp_weggooistapels[stapel])
            kleinste = stapel
    return kleinste

"""
Controleert of alle kaarten in de weggooistapel hetzelfde zijn.
"""
def check_weggooistapel(stapel):
    gelijk = stapel[-1]
    for kaart in stapel:
        if kaart != gelijk:
            return False
    return True

"""
Het wegleggen van een kaart (beurt eindigen). 
- Optie 1: Als alle kaarten in een weggooistapel hetzelfde zijn en deze in de hand aanwezig is, wordt deze hierbij gegooid. 
- Optie 2: Als de stapel leeg is wordt er een kaart die dubbel aanwezig is in de hand opgegooid.
- Optie 3: Als de kaart die 1 kleiner is dan de bovenste kaart van de weggooistapel aanwezig is in de hand, wordt deze 
    hierbij gegooid, om later een 'chain' te kunnen vormen
- Optie 4: Als de vorige opties allemaal niet mogelijk zijn wordt de eerste kaart uit de hand die geen Skip-Bo kaart is 
    aan de kleinste weggooistapel toegevoegd
"""
def kaart_wegleggen(comp_hand, comp_weggooistapels):
    index = None
    for optie in range(4):
        for stapel in comp_weggooistapels:
            if optie == 0 and (len(comp_weggooistapels[stapel]) > 0 and (
                    check_weggooistapel(comp_weggooistapels[stapel]) and comp_weggooistapels[stapel][-1] in comp_hand)):
                index = comp_hand.index(comp_weggooistapels[stapel][-1])
                break
            elif optie == 1 and len(comp_weggooistapels[stapel]) == 0:
                for handoptie in range(2):
                    for kaart in comp_hand:
                        if (handoptie == 0 and (
                                comp_hand.count(kaart) > 1 and kaart != "SB")) or handoptie == 1 and kaart != "SB":
                            index = comp_hand.index(kaart)
                            break
                    if index is not None:
                        break
                break
            elif optie == 2 and (len(comp_weggooistapels[stapel]) > 0 and comp_weggooistapels[stapel][-1] - 1 in comp_hand):
                index = comp_hand.index(comp_weggooistapels[stapel][-1] - 1)
                break
            elif optie == 3:
                index = 0
                for kaart in comp_hand:
                    if kaart != "SB":
                        index = comp_hand.index(kaart)
                        break
                print("(Computer)   Kaart {} uit hand naar weggooistapel {}\n".format(comp_hand[index],
                                                                        kleinste_weggooistapel(comp_weggooistapels)))
                comp_weggooistapels[kleinste_weggooistapel(comp_weggooistapels)].append(comp_hand[index])
                comp_hand = comp_hand[:index] + comp_hand[index + 1:]
                return comp_hand, comp_weggooistapels
        if index is not None:
            break
    print("(Computer)   Kaart {} uit hand naar weggooistapel {}\n".format(comp_hand[index], stapel))
    comp_weggooistapels[stapel].append(comp_hand[index])
    comp_hand = comp_hand[:index] + comp_hand[index + 1:]
    return comp_hand, comp_weggooistapels

"""
Controleert of de benodigde kaart in een weggooistapel aanwezig is.
"""
def check_weggooistapels(comp_weggooistapels, kaart):
    for stapel in comp_weggooistapels:
        if not comp_weggooistapels[stapel]:
            continue
        if comp_weggooistapels[stapel][-1] == kaart:
            return True, stapel
    return False, None

"""
Voegt de kaarten uit de hand en beschikbare kaarten uit de weggooistapels bij elkaar.
"""
def beschikbare_kaarten(comp_hand, comp_weggooistapels):
    temp = comp_hand.copy()
    for stapel in comp_weggooistapels:
        if len(comp_weggooistapels[stapel]) > 0:
            temp.append(comp_weggooistapels[stapel][-1])
    return temp

"""
Stapel die het dichtste bij de stok kaart is berekenen. Als de stok kaart een Skip-Bo kaart is wordt deze als kaart 
gebruikt die niet aanwezig is in de hand en weggooistapels
"""
def dichtste_bij_stok(bouwstapels, comp_stok, comp_hand, comp_weggooistapels):
    if comp_stok[0] == "SB":
        for stapel in bouwstapels:
            if bovenste_kaart_bouwstapel(bouwstapels[stapel]) + 1 in beschikbare_kaarten(comp_hand,
                                                                                         comp_weggooistapels):
                continue
            elif bovenste_kaart_bouwstapel(bouwstapels[stapel]) + 1 not in beschikbare_kaarten(comp_hand, comp_weggooistapels):
                return stapel
        return 'A'

    kleinste_verschil = 13
    for stapel in bouwstapels:
        verschil = comp_stok[0] - bovenste_kaart_bouwstapel(bouwstapels[stapel])
        if verschil <= 0:
            verschil += 12
        if verschil < kleinste_verschil:
            kleinste_verschil = verschil
            meest_dichtbij = stapel
    return meest_dichtbij

"""
Maken van een pad naar de stok kaart. Als het pad niet helemaal naar de stok loopt, het uiteindelijke verschil kleiner 
is dan 3, en de kaart van de mens stok te dichtbij komt, wordt het pad niet toegepast.  
"""
def pad_maken(bouwstapels, mens_stok, comp_stok, comp_hand, comp_weggooistapels):
    if comp_stok[0] == "SB":
        return [["stok", 0]]

    dichtste_bij = dichtste_bij_stok(bouwstapels, comp_stok, comp_hand, comp_weggooistapels)
    bovenste = bovenste_kaart_bouwstapel(bouwstapels[dichtste_bij])
    verschil = comp_stok[0] - bovenste + 1
    mens_verschil = mens_stok[0] - bovenste + 1

    if verschil < 0:
        verschil += 11
    if mens_verschil < 0:
        verschil += 11

    temp_hand = comp_hand.copy()
    temp_weggooistapels = comp_weggooistapels.copy()

    pad = []
    for kaart in range(1, verschil):
        if bovenste + kaart == comp_stok[0]:
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

    if verschil - 1 != len(pad) and verschil - 1 - len(pad) < 3 and mens_verschil - 1 - len(pad) < 3:
        pad = []
    return pad

"""
Het toepassen van het pad op de bouwstapel die het dichtste bij de stok kaart is.
"""
def pad_toepassen(pad, bouwstapels, dichtste_bij, comp_stok, comp_hand, comp_weggooistapels, trekstapel):
    for stap in pad:
        bouwstapels, trekstapel, check_bouwstapels(bouwstapels, trekstapel)

        if stap[0] == "stok":
            print("(Computer)   Kaart {} uit stok naar bouwstapel {}".format(comp_stok[0], dichtste_bij))
            bouwstapels[dichtste_bij].append(comp_stok[stap[1]])
            comp_stok = comp_stok[1:]
        elif stap[0] == "hand":
            print("(Computer)   Kaart {} uit hand naar bouwstapel {}".format(comp_hand[stap[1]], dichtste_bij))
            bouwstapels[dichtste_bij].append(comp_hand[stap[1]])
            comp_hand = comp_hand[:stap[1]] + comp_hand[stap[1] + 1:]
        elif stap[0] == "weggooistapel":
            print("(Computer)   Kaart {} uit weggooistapel {} naar bouwstapel {}"
                  .format(comp_weggooistapels[stap[1]][-1], stap[1], dichtste_bij))
            bouwstapels[dichtste_bij].append(comp_weggooistapels[stap[1]][-1])
            comp_weggooistapels[stap[1]] = comp_weggooistapels[stap[1]][:-1]
    return bouwstapels, comp_stok, comp_hand, comp_weggooistapels, trekstapel

# Main functie
"""
Runnen van de applicatie
"""
def run(window):
    trekstapel, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand, comp_hand = instellen()

    update_gui(window, bouwstapels, mens_weggooistapels, comp_weggooistapels, mens_stok, comp_stok, mens_hand,
               comp_hand, True, trekstapel)

    window.mainloop()

run(tk.Tk(className=' Skip-Bo'))
