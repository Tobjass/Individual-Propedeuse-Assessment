from random import shuffle

trekstapel = [str(x % 12 + 1) for x in range(0, 144)]
trekstapel += ["SB"] * 18
shuffle(trekstapel)

print(trekstapel)

kaarten = trekstapel[:5]
trekstapel = trekstapel[5:]

print(kaarten)
print(trekstapel)

bouwstapels = {'A': [], 'B': [], 'C': [], 'D': []}
