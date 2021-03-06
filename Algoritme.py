from random import shuffle

def bovenste_kaart_bouwstapel(bouwstapel):
    if not bouwstapel:
        return 0
    elif len(bouwstapel) == 1:
        return 1
    elif bouwstapel[-1] == "SB":
        return bovenste_kaart_bouwstapel(bouwstapel[:-1]) + 1
    else:
        return bouwstapel[-1]

def check_bouwstapels(bouwstapels, trekstapel):
    for stapel in bouwstapels:
        if bovenste_kaart_bouwstapel(bouwstapels[stapel]) == 12:
            print("\nBouwstapel {} heeft 12 behaald en wordt geleegd".format(stapel))
            for kaart in bouwstapels[stapel]:
                trekstapel.append(kaart)
            shuffle(trekstapel)
            bouwstapels[stapel] = []
    return bouwstapels, trekstapel

def trek_kaarten(hand, trekstapel):
    index = 5 - len(hand)
    if index > 0:
        for kaart in trekstapel[:index]:
            hand.append(kaart)
        trekstapel = trekstapel[index:]
    return hand, trekstapel

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

def run():
    trekstapel = [x % 12 + 1 for x in range(0, 144)]
    trekstapel += ["SB"] * 18
    shuffle(trekstapel)

    bouwstapels = {'A': [], 'B': [], 'C': [], 'D': []}
    weggooistapels = {'A': [], 'B': [], 'C': [], 'D': []}

    stok = trekstapel[:30]
    trekstapel = trekstapel[30:]

    hand = trekstapel[:5]
    trekstapel = trekstapel[5:]

    for beurt in range(50):
        print("----- Beurt {} -----".format(beurt + 1))
        hand, trekstapel = trek_kaarten(hand, trekstapel)

        while True:
            bouwstapels, trekstapel = check_bouwstapels(bouwstapels, trekstapel)

            if len(hand) == 0:
                hand, trekstapel = trek_kaarten(hand, trekstapel)

            dichtste_bij = dichtste_bij_stok(bouwstapels, stok, hand, weggooistapels)
            pad = pad_maken(bouwstapels, stok, hand, weggooistapels)

            print("\nStok: {}   ({})\nBouwstapels: {}\nHand: {}\nWeggooistapels: {}\n\nBouwstapel {} is het dichtste bij de stok\nPad: {}\n".format(stok[0], len(stok), bouwstapels, hand, weggooistapels, dichtste_bij, pad))

            if not pad:
                break

            bouwstapels[dichtste_bij], stok, hand, weggooistapels = pad_toepassen(pad, bouwstapels[dichtste_bij], stok, hand, weggooistapels)

            print("Na toepassen van pad:\n\nStok: {}   ({})\nBouwstapels: {}\nHand: {}\nWeggooistapels: {}".format(stok[0], len(stok), bouwstapels, hand, weggooistapels))

        hand, weggooistapels = kaart_wegleggen(hand, weggooistapels)

run()
