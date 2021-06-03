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

def trek_kaarten(hand, trekstapel):
    index = 5 - len(hand)
    if index > 0:
        for kaart in trekstapel[:index]:
            hand.append(kaart)
        trekstapel = trekstapel[index:]
    return hand, trekstapel

def kleinste_weggooistapel(weggooistapels):
    len_kleinste = 0
    kleinste = None
    for x in weggooistapels:
        if len(weggooistapels[x]) > len_kleinste:
            len_kleinste = len(weggooistapels[x])
            kleinste = x
    return kleinste

def kaart_wegleggen(hand, weggooistapels):
    weggegooid = False
    for x in weggooistapels:
        index = hand.index(max(hand if ("SB" not in hand) else hand[:hand.index("SB")] + hand[hand.index("SB")+1:]))
        if len(weggooistapels[x]) == 0 or (len(weggooistapels[x]) > 0 and weggooistapels[x][-1] == hand[index]):
            weggooistapels[x].append(hand[index])
            hand = hand[:index] + hand[index + 1:]
            weggegooid = True
            break
    if weggegooid is False:
        weggooistapels[kleinste_weggooistapel(weggooistapels)].append(hand[index])
        hand = hand[:index] + hand[index + 1:]
    return hand, weggooistapels

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

def probeer_hand(bouwstapels, hand, stok):
    verandering = False
    print("Hand: {}".format(hand))
    for x in bouwstapels:
        while True:
            append = None
            bool = False
            if bovenste_kaart_bouwstapel(bouwstapels[x]) == 0:
                if ("SB" not in hand and 1 not in hand) or stok[0] == 1:
                    break
                bool = True
                append = "SB" if ("SB" in hand) else 1
            else:
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
    return bouwstapels, hand, verandering

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

trekstapel = [x % 12 + 1 for x in range(0, 144)]
trekstapel += ["SB"] * 18
shuffle(trekstapel)

bouwstapels = {'A': [], 'B': [], 'C': [], 'D': []}
weggooistapels = {'A': [], 'B': [], 'C': [], 'D': []}

stok = trekstapel[:30]
trekstapel = trekstapel[30:]

hand = trekstapel[:5]
trekstapel = trekstapel[5:]

for a in range(20):
    check_bouwstapels(bouwstapels, trekstapel)

    print("Beurt {}\n".format(a+1))

    hand, trekstapel = trek_kaarten(hand, trekstapel)
    while True:
        bouwstapels, stok, stok_verandering = probeer_stok(bouwstapels, stok)
        print("Bouwstapels: {}\nVerandering in stok: {}\n".format(bouwstapels, stok_verandering))

        bouwstapels, hand, hand_verandering = probeer_hand(bouwstapels, hand, stok)
        print("Bouwstapels: {}\nVerandering in hand: {}\n".format(bouwstapels, hand_verandering))

        bouwstapels, weggooistapels, weggooistapels_verandering = probeer_weggooistapels(bouwstapels, weggooistapels, stok)
        print("Bouwstapels: {}\nVerandering in weggooistapels: {}\n".format(bouwstapels, weggooistapels_verandering))

        verandering = True if (stok_verandering or hand_verandering or weggooistapels_verandering) else False
        print("Verandering: {}\n\n".format(verandering))

        if verandering is False or not stok:
            break
    if not stok:
        print("Stok leeg!")
        break

    hand, weggooistapels = kaart_wegleggen(hand, weggooistapels)
    print("Weggooistapels: {}\nHand: {}\n\n".format(weggooistapels, hand))
