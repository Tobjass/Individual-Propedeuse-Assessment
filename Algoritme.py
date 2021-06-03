from random import shuffle


def probeer_stok(bouwstapels, stok):
    print(stok)
    for x in bouwstapels:
        print(bouwstapels[x])
        if (len(bouwstapels[x]) == 0 and (stok[0] == "1" or stok[0] == "SB")) or (len(bouwstapels[x]) > 0 and bouwstapels[x][len(bouwstapels[x]) - 1] + 1 == stok[0]):
            bouwstapels[x].append(stok[0])
            stok = stok[1:]
    print(stok)
    print(bouwstapels)


trekstapel = [str(x % 12 + 1) for x in range(0, 144)]
trekstapel += ["SB"] * 18
shuffle(trekstapel)

bouwstapels = {'A': [], 'B': [], 'C': [], 'D': []}

stok = trekstapel[:30]
trekstapel = trekstapel[30:]

kaarten = trekstapel[:5]
trekstapel = trekstapel[5:]

probeer_stok(bouwstapels, stok)




