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

def kaart_wegleggen(hand, weggooistapels):
    weggegooid = False
    for x in weggooistapels:
        sb_count = hand.count("SB")
        if "SB" in hand:
            for y in range(sb_count):
                hand.remove("SB")
        index = hand.index(max(hand))
        if len(weggooistapels[x]) == 0 or (len(weggooistapels[x]) > 0 and weggooistapels[x][-1] == hand[index]):
            weggooistapels[x].append(hand[index])
            hand = hand[:index] + hand[index+1:]
            weggegooid = True
            break
    if weggegooid is False:
        weggooistapels[kleinste_weggooistapel(weggooistapels)].append(hand[index])
        hand = hand[:index] + hand[index+1:]
    hand += ["SB"] * sb_count
    return hand, weggooistapels

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
    if not pad:
        return bouwstapel, stok, hand, weggooistapels

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

    trekstapel = [5, 'SB', 8, 7, 10, 'SB', 7, 4, 6, 10, 1, 10, 12, 5, 9, 5, 10, 11, 11, 'SB', 11, 7, 9, 8, 4, 5, 12, 6, 1, 9, 8, 6, 3, 4, 12, 3, 3, 11, 9, 'SB', 9, 7, 12, 4, 10, 'SB', 6, 9, 6, 12, 3, 2, 5, 10, 'SB', 5, 5, 11, 'SB', 8, 2, 2, 'SB', 8, 'SB', 7, 6, 8, 5, 9, 5, 12, 'SB', 8, 1, 3, 7, 2, 9, 2, 3, 12, 11, 8, 2, 4, 12, 9, 6, 'SB', 7, 12, 7, 7, 'SB', 10, 'SB', 5, 10, 7, 2, 11, 1, 5, 3, 10, 3, 6, 11, 3, 9, 4, 1, 1, 6, 'SB', 10, 1, 3, 11, 4, 3, 9, 11, 11, 1, 4, 3, 6, 4, 2, 6, 5, 'SB', 1, 10, 'SB', 8, 11, 1, 9, 2, 1, 7, 8, 4, 1, 12, 2, 'SB', 12, 2, 8, 4, 2, 6, 8, 'SB', 4, 10, 12, 7]

    print("Trekstapel: {}".format(trekstapel))

    bouwstapels = {'A': [1, 2, 3, 4, 5, 6], 'B': [], 'C': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'D': []}
    weggooistapels = {'A': [12, 12], 'B': [9, 4], 'C': [1], 'D': []}

    # stok = trekstapel[:30]
    # trekstapel = trekstapel[30:]

    stok = [5, 'SB', 8, 7, 10, 'SB', 7, 4, 6, 10, 1, 10, 12, 5, 9, 5, 10, 11, 11, 'SB', 11, 7, 9, 8, 4, 5, 12, 6, 1, 9]

    print("Stok: {}".format(stok))

    hand = [8, 3, "SB", 9, 11]

    # hand = trekstapel[:5]
    # trekstapel = trekstapel[5:]

    for a in range(4):
        print("\nHand: {}".format(hand))
        dichtste_bij = dichtste_bij_stok(bouwstapels, stok)
        pad = pad_maken(bouwstapels, stok, hand, weggooistapels)
        print("Bouwstapel {} is het dichtste bij de stok\nPad: {}\n".format(dichtste_bij, pad))

        bouwstapels[dichtste_bij], stok, hand, weggooistapels = pad_toepassen(pad, bouwstapels[dichtste_bij], stok, hand, weggooistapels)

        print("Stok: {}\nBouwstapels: {}\nHand: {}\nWeggooistapels: {}".format(stok, bouwstapels, hand, weggooistapels))

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
