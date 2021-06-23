def bovenste_kaart_bouwstapel(bouwstapel):
    if not bouwstapel:
        return 0
    elif len(bouwstapel) == 1:
        return 1
    elif bouwstapel[-1] == "SB":
        return bovenste_kaart_bouwstapel(bouwstapel[:-1]) + 1
    else:
        return bouwstapel[-1]

def mogelijkheid(kaart, bouwstapels):
    for stapel in bouwstapels:
        if bovenste_kaart_bouwstapel(bouwstapels[stapel]) + 1 == kaart or kaart == "SB":
            return True
    return False

def kaart_van_trekstapel(trekstapel, aantal):
    return trekstapel[:aantal], trekstapel[aantal:]

def trek_kaarten(hand, trekstapel):
    index = 5 - len(hand)
    if index > 0:
        for kaart in trekstapel[:index]:
            hand.append(kaart)
        trekstapel = trekstapel[index:]
    return hand, trekstapel

def check_bouwstapels(bouwstapels, trekstapel):
    for stapel in bouwstapels:
        if bovenste_kaart_bouwstapel(bouwstapels[stapel]) == 12:
            for kaart in bouwstapels[stapel]:
                trekstapel.append(kaart)
            # shuffle(trekstapel) is random, dus kan niet getest worden
            bouwstapels[stapel] = []
    return bouwstapels, trekstapel

def test_bovenste_kaart_bouwstapel():
    assert bovenste_kaart_bouwstapel([1, 2, 3, "SB"]) == 4, "Moet 4 zijn"

def test_mogelijkheid():
    assert mogelijkheid(6, {'A': [1, 2], 'B': [1, 2, 3, 4, 5, 6], 'C': [1, 2, "SB"],
                            'D': [1, 2, 3, 4, "SB"]}) is True, "Moet True zijn"
    assert mogelijkheid(10, {'A': [1, 2], 'B': [1, 2, 3, 4, 5, 6], 'C': [1, 2, "SB"],
                             'D': [1, 2, 3, 4, "SB"]}) is False, "Moet False zijn"

def test_kaart_van_trekstapel(trekstapel):
    stok = [6, 7, 'SB', 6, 'SB', 7, 8, 6, 12, 4, 4, 'SB', 10, 5, 3, 6, 6, 1, 9, 'SB', 1, 1, 5, 7, 'SB', 3, 1, 4, 8, 7]
    nieuwe_trekstapel = [12, 8, 10, 9, 2, 1, 2, 10, 5, 1, 8, 10, 1, 5, 9, 2, 11, 4, 10, 7, 7, 'SB', 8, 'SB', 3, 8, 5,
                         'SB', 6, 10, 11, 12, 9, 6, 'SB', 3, 10, 9, 4, 2, 11, 7, 1, 8, 8, 9, 11, 6, 3, 12, 4, 2, 'SB',
                         4, 8, 1, 5, 3, 3, 'SB', 7, 12, 6, 2, 9, 12, 'SB', 9, 2, 3, 9, 9, 12, 12, 10, 11, 11, 12, 'SB',
                         'SB', 5, 4, 11, 10, 5, 2, 7, 3, 4, 'SB', 7, 11, 11, 1, 10, 3, 3, 11, 12, 5, 8, 10, 1, 5, 9, 5,
                         'SB', 12, 7, 7, 4, 6, 6, 3, 11, 2, 'SB', 10, 8, 5, 12, 8, 11, 2, 6, 1, 'SB', 4, 2, 4, 2, 9]
    assert kaart_van_trekstapel(trekstapel, 30) == (stok, nieuwe_trekstapel), "Klopt niet"

def test_trek_kaarten(trekstapel):
    assert trek_kaarten([3, "SB", 8], trekstapel) == ([3, "SB", 8, 6, 7], trekstapel[2:]), "Moet [3, SB, 8, 6, 7] zijn"

def test_check_bouwstapels(trekstapel):
    bouwstapel_b = [1, 2, 3, 4, 5, 6, 7, "SB", 9, 10, 11, 12]
    nieuwe_trekstapel = trekstapel
    for kaart in bouwstapel_b:
        nieuwe_trekstapel.append(kaart)

    assert check_bouwstapels({'A': [1, 2], 'B': bouwstapel_b, 'C': [1, 2, "SB"], 'D': [1, 2, 3, 4, "SB"]},
                             trekstapel) == ({'A': [1, 2], 'B': [], 'C': [1, 2, "SB"], 'D': [1, 2, 3, 4, "SB"]},
                                             nieuwe_trekstapel), "Bouwstapel B moet leeg zijn"

trekstapel = [6, 7, 'SB', 6, 'SB', 7, 8, 6, 12, 4, 4, 'SB', 10, 5, 3, 6, 6, 1, 9, 'SB', 1, 1, 5, 7, 'SB', 3, 1, 4,
                  8, 7, 12, 8, 10, 9, 2, 1, 2, 10, 5, 1, 8, 10, 1, 5, 9, 2, 11, 4, 10, 7, 7, 'SB', 8, 'SB', 3, 8, 5,
                  'SB', 6, 10, 11, 12, 9, 6, 'SB', 3, 10, 9, 4, 2, 11, 7, 1, 8, 8, 9, 11, 6, 3, 12, 4, 2, 'SB', 4, 8, 1,
                  5, 3, 3, 'SB', 7, 12, 6, 2, 9, 12, 'SB', 9, 2, 3, 9, 9, 12, 12, 10, 11, 11, 12, 'SB', 'SB', 5, 4, 11,
                  10, 5, 2, 7, 3, 4, 'SB', 7, 11, 11, 1, 10, 3, 3, 11, 12, 5, 8, 10, 1, 5, 9, 5, 'SB', 12, 7, 7, 4, 6,
                  6, 3, 11, 2, 'SB', 10, 8, 5, 12, 8, 11, 2, 6, 1, 'SB', 4, 2, 4, 2, 9]

test_bovenste_kaart_bouwstapel()
test_mogelijkheid()
test_kaart_van_trekstapel(trekstapel)
test_trek_kaarten(trekstapel)
test_check_bouwstapels(trekstapel)
print("Tests succesvol")
