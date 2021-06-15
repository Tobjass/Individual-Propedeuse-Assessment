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
    for x in bouwstapels:
        if bovenste_kaart_bouwstapel(bouwstapels[x]) == 12:
            for kaart in bouwstapels[x]:
                trekstapel.append(kaart)
            shuffle(trekstapel)
            bouwstapels[x] = []
    return bouwstapels, trekstapel

def vergelijk_bouwstapels(bouwstapel, stok):
    if bovenste_kaart_bouwstapel(bouwstapel) > stok[0]:
        return False
    elif bovenste_kaart_bouwstapel(bouwstapel) < stok[0]:
        return True

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
    for x in weggooistapels:
        if len(weggooistapels[x]) < len_kleinste:
            len_kleinste = len(weggooistapels[x])
            kleinste = x
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
                weggooistapel = stapel
                break
            elif optie == 1 and len(weggooistapels[stapel]) == 0:
                for handoptie in range(2):
                    for kaart in hand:
                        if (handoptie == 0 and (hand.count(kaart) > 1 and kaart != "SB")) or handoptie == 1 and kaart != "SB":
                            index = hand.index(kaart)
                            break
                    if index is not None:
                        break
                weggooistapel = stapel
                break
            elif optie == 2 and (len(weggooistapels[stapel]) > 0 and weggooistapels[stapel][-1] - 1 in hand):
                index = hand.index(weggooistapels[stapel][-1] - 1)
                weggooistapel = stapel
                break
            elif optie == 3:
                index = 0
                for kaart in hand:
                    if kaart != "SB":
                        index = hand.index(kaart)
                        break
                weggooistapels[kleinste_weggooistapel(weggooistapels)].append(hand[index])
                hand = hand[:index] + hand[index + 1:]
                return hand, weggooistapels
        if index is not None:
            break
    weggooistapels[weggooistapel].append(hand[index])
    hand = hand[:index] + hand[index + 1:]
    return hand, weggooistapels

    # weggegooid = False
    # for x in weggooistapels:
    #     sb_count = hand.count("SB")
    #     if "SB" in hand:
    #         for y in range(sb_count):
    #             hand.remove("SB")
    #     index = hand.index(max(hand))
    #     if len(weggooistapels[x]) == 0 or (len(weggooistapels[x]) > 0 and weggooistapels[x][-1] == hand[index]):
    #         weggooistapels[x].append(hand[index])
    #         hand = hand[:index] + hand[index+1:]
    #         weggegooid = True
    #         break
    # if weggegooid is False:
    #     weggooistapels[kleinste_weggooistapel(weggooistapels)].append(hand[index])
    #     hand = hand[:index] + hand[index+1:]
    # hand += ["SB"] * sb_count
    # return hand, weggooistapels

def check_weggooistapels(weggooistapels, kaart):
    for x in weggooistapels:
        if not weggooistapels[x]:
            continue
        if weggooistapels[x][-1] == kaart:
            return True, x
    return False, None

def dichtste_bij_stok(bouwstapels, stok):
    if stok[0] == 'SB':
        return 'A'
    kleinste_verschil = 13
    for x in bouwstapels:
        verschil = stok[0] - bovenste_kaart_bouwstapel(bouwstapels[x])
        if verschil <= 0:
            verschil += 11
        if verschil < kleinste_verschil:
            kleinste_verschil = verschil
            meest_dichtbij = x
    return meest_dichtbij

def pad_maken(bouwstapels, stok, hand, weggooistapels):
    if stok[0] == "SB":
        return [["stok", 0]]

    dichtste_bij = dichtste_bij_stok(bouwstapels, stok)
    bovenste = bovenste_kaart_bouwstapel(bouwstapels[dichtste_bij])
    verschil = stok[0] - bovenste + 1

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
    for x in pad:
        if x[0] == "stok":
            bouwstapel.append(stok[x[1]])
            stok = stok[1:]
        elif x[0] == "hand":
            bouwstapel.append(hand[x[1]])
            hand = hand[:x[1]] + hand[x[1] + 1:]
        elif x[0] == "weggooistapel":
            bouwstapel.append(weggooistapels[x[1]][-1])
            weggooistapels[x[1]] = weggooistapels[x[1]][:-1]
    return bouwstapel, stok, hand, weggooistapels

def probeer_stok(bouwstapels, stok):
    verandering = False
    print("Stok: {}".format(stok))
    for x in bouwstapels:
        while True:
            if not stok:
                return bouwstapels, stok, verandering
            append = None
            bool = False
            if bovenste_kaart_bouwstapel(bouwstapels[x]) == 0:
                if stok[0] != "SB" and stok[0] != 1:
                    break
                bool = True
                append = 1 if (stok[0] != "SB") else "SB"
            else:
                if bovenste_kaart_bouwstapel(bouwstapels[x]) + 1 == stok[0] or stok[0] == "SB":
                    bool = True
                    append = stok[0]
            if append is not None:
                bouwstapels[x].append(append)
                stok = stok[1:]
                verandering = True
            if bool is False:
                break
    return bouwstapels, stok, verandering

def probeer_hand(bouwstapels, hand, stok, trekstapel):
    verandering = False
    print("Hand: {}".format(hand))
    for x in bouwstapels:
        while True:
            if not hand:
                hand = trekstapel[:5]
                trekstapel = trekstapel[5:]
            append = None
            bool = False
            if bovenste_kaart_bouwstapel(bouwstapels[x]) == 0:
                if ("SB" not in hand and 1 not in hand) or stok[0] == 1:
                    break
                bool = True
                append = "SB" if ("SB" in hand) else 1
            else:
                if vergelijk_bouwstapels(bouwstapels[x], stok) is False:
                    break
                if bovenste_kaart_bouwstapel(bouwstapels[x]) + 1 in hand and stok[0] != bovenste_kaart_bouwstapel(bouwstapels[x]) + 1:
                    bool = True
                    append = bovenste_kaart_bouwstapel(bouwstapels[x]) + 1
                elif "SB" in hand and stok[0] != bovenste_kaart_bouwstapel(bouwstapels[x]) + 1:
                    bool = True
                    append = "SB"
            if append is not None:
                bouwstapels[x].append(append)
                hand = hand[:hand.index(append)] + hand[hand.index(append)+1:]
                verandering = True
            if bool is False:
                break
    return bouwstapels, hand, verandering, trekstapel

def probeer_weggooistapels(bouwstapels, weggooistapels, stok):
    verandering = False
    print("Weggooistapels: {}".format(weggooistapels))
    for x in bouwstapels:
        for y in weggooistapels:
            if len(weggooistapels[y]) == 0:
                continue
            if ((bovenste_kaart_bouwstapel(bouwstapels[x]) == 0 and weggooistapels[y][-1] == 1) or (bovenste_kaart_bouwstapel(bouwstapels[x]) + 1 == weggooistapels[y][-1])) and (stok[0] != weggooistapels[y][-1] and weggooistapels[y][-1] not in hand):
                bouwstapels[x].append(weggooistapels[y][-1])
                weggooistapels[y] = weggooistapels[y][:-1]
                verandering = True
    return bouwstapels, weggooistapels, verandering

def run():
    # trekstapel = [x % 12 + 1 for x in range(0, 144)]
    # trekstapel += ["SB"] * 18
    # shuffle(trekstapel)

    bouwstapels = {'A': [], 'B': [], 'C': [], 'D': []}
    weggooistapels = {'A': [3, 2], 'B': [4, 3, 1], 'C': [6], 'D': [2, 1]}

    trekstapel = [8, 'SB', 11, 9, 12, 2, 7, 9, 9, 8, 9, 8, 8, 2, 'SB', 3, 11, 'SB', 2, 1, 'SB', 6, 4, 5, 'SB', 2, 3, 6, 6, 10, 1, 3, 6, 4, 7, 1, 4, 12, 2, 4, 4, 6, 'SB', 9, 5, 'SB', 3, 9, 1, 4, 10, 7, 12, 12, 4, 5, 11, 4, 'SB', 11, 7, 10, 11, 6, 2, 'SB', 10, 3, 8, 9, 5, 'SB', 8, 3, 12, 3, 11, 6, 'SB', 'SB', 11, 7, 2, 7, 8, 8, 4, 1, 6, 12, 5, 7, 11, 1, 6, 4, 6, 8, 10, 7, 12, 1, 2, 5, 3, 3, 7, 'SB', 1, 9, 12, 8, 10, 7, 9, 10, 9, 7, 5, 10, 3, 4, 3, 5, 'SB', 5, 8, 9, 12, 'SB', 2, 2]
    stok = [9, 10, 5, 'SB', 7, 1, 6, 1, 3, 8, 11, 11, 1, 12, 5, 5, 'SB', 12, 10, 11, 10, 'SB', 11, 2, 1, 10, 2, 6, 4, 12]
    hand = ['SB', 8, 11, 9, 12]

    # stok = trekstapel[:30]
    # trekstapel = trekstapel[30:]

    # hand = trekstapel[:5]
    # trekstapel = trekstapel[5:]

    print(hand)

    hand, weggooistapels = kaart_wegleggen(hand, weggooistapels)

    print(weggooistapels)
    print(hand)

    # for beurt in range(10):
    #     print("Beurt {}".format(beurt + 1))
    #     hand, trekstapel = trek_kaarten(hand, trekstapel)
    #
    #     while True:
    #         if not hand:
    #             hand, trekstapel = trek_kaarten(hand, trekstapel)
    #
    #         dichtste_bij = dichtste_bij_stok(bouwstapels, stok)
    #         pad = pad_maken(bouwstapels, stok, hand, weggooistapels)
    #
    #         print("\nStok: {}\nBouwstapels: {}\nHand: {}\nWeggooistapels: {}\n\nBouwstapel {} is het dichtste bij de stok\nPad: {}\n".format(stok[0], bouwstapels, hand, weggooistapels, dichtste_bij, pad))
    #
    #         if not pad:
    #             break
    #
    #         bouwstapels[dichtste_bij], stok, hand, weggooistapels = pad_toepassen(pad, bouwstapels[dichtste_bij], stok, hand, weggooistapels)
    #
    #         print("Na toepassen van pad:\n\nStok: {}\nBouwstapels: {}\nHand: {}\nWeggooistapels: {}".format(stok, bouwstapels, hand, weggooistapels))

    # for beurt in range(50):
    #     check_bouwstapels(bouwstapels, trekstapel)
    #
    #     print("Beurt {}\n".format(beurt+1))
    #
    #     hand, trekstapel = trek_kaarten(hand, trekstapel)
    #
    #     print("Hand: {}".format(hand))
    #     print("Bouwstapel {} is het dichtste bij de stok\nPad: {}\n".format(dichtste_bij_stok(bouwstapels, stok), stok_mogelijkheid(bouwstapels, stok, hand, weggooistapels)))
    #
    #     while True:
    #         bouwstapels, stok, stok_verandering = probeer_stok(bouwstapels, stok)
    #         print("Bouwstapels: {}\nVerandering in stok: {}\n".format(bouwstapels, stok_verandering))
    #         check_bouwstapels(bouwstapels, trekstapel)
    #
    #         bouwstapels, hand, hand_verandering, trekstapel = probeer_hand(bouwstapels, hand, stok, trekstapel)
    #         print("Bouwstapels: {}\nVerandering in hand: {}\n".format(bouwstapels, hand_verandering))
    #         check_bouwstapels(bouwstapels, trekstapel)
    #
    #         bouwstapels, weggooistapels, weggooistapels_verandering = probeer_weggooistapels(bouwstapels, weggooistapels, stok)
    #         print("Bouwstapels: {}\nVerandering in weggooistapels: {}\n".format(bouwstapels, weggooistapels_verandering))
    #         check_bouwstapels(bouwstapels, trekstapel)
    #
    #         verandering = True if (stok_verandering or hand_verandering or weggooistapels_verandering) else False
    #         print("Verandering: {}\n\n".format(verandering))
    #
    #         if verandering is False or not stok:
    #             break
    #     if not stok:
    #         print("Stok leeg!")
    #         break
    #
    #     hand, weggooistapels = kaart_wegleggen(hand, weggooistapels)
    #     print("Weggooistapels: {}\nHand: {}\n\n".format(weggooistapels, hand))

run()
