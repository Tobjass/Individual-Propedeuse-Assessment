from random import shuffle

def probeer_stok(bouwstapels, stok):
    verandering = False
    print(stok)
    for x in bouwstapels:
        print(bouwstapels[x])
        if ((len(bouwstapels[x]) == 0 and stok[0] == 1) or (len(bouwstapels[x]) > 0 and bouwstapels[x][-1] + 1 == stok[0])) or stok[0] == "SB":
            bouwstapels[x].append(stok[0])
            stok = stok[1:]
            verandering = True
    return bouwstapels, stok, verandering

def probeer_hand(bouwstapels, hand):
    verandering = False
    print(hand)
    for x in bouwstapels:
        print(bouwstapels[x])
        index = None
        if "SB" in hand:
            index = hand.index("SB")
        elif len(bouwstapels[x]) == 0 and 1 in hand:
            index = hand.index(1)
        elif len(bouwstapels[x]) > 0 and bouwstapels[x][-1] + 1 in hand:
            index = hand.index(bouwstapels[x][len(bouwstapels[x]) - 1] + 1)
        if index is not None:
            bouwstapels[x].append(hand[index])
            hand = hand[:index] + hand[index+1:]
            verandering = True
    return bouwstapels, hand, verandering

def probeer_weggooistapels(bouwstapels, weggooistapels):
    verandering = False
    print(weggooistapels)
    for x in bouwstapels:
        print(bouwstapels[x])
        for y in weggooistapels:
            if len(weggooistapels[y]) == 0:
                continue
            if (len(bouwstapels[x]) == 0 and weggooistapels[y][-1] == 1) or (len(bouwstapels[x]) > 0 and bouwstapels[x][-1] + 1 == weggooistapels[y][-1]):
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

bouwstapels, stok, verandering = probeer_stok(bouwstapels, stok)
print(bouwstapels, verandering)

bouwstapels, hand, verandering = probeer_hand(bouwstapels, hand)
print(bouwstapels, verandering)

bouwstapels, weggooistapels, verandering = probeer_weggooistapels(bouwstapels, weggooistapels)
print(bouwstapels, verandering)
