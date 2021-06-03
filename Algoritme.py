from random import shuffle

trekstapel = [str(x % 12 + 1) for x in range(0, 144)]
trekstapel += ["SB"] * 18
shuffle(trekstapel)

print(trekstapel)