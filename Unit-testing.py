#Functies uit GUI.py
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

def check_weggooistapel(stapel):
    gelijk = stapel[-1]
    for kaart in stapel:
        if kaart != gelijk:
            return False
    return True

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
                comp_weggooistapels[kleinste_weggooistapel(comp_weggooistapels)].append(comp_hand[index])
                comp_hand = comp_hand[:index] + comp_hand[index + 1:]
                return comp_hand, comp_weggooistapels
        if index is not None:
            break
    comp_weggooistapels[stapel].append(comp_hand[index])
    comp_hand = comp_hand[:index] + comp_hand[index + 1:]
    return comp_hand, comp_weggooistapels

def check_weggooistapels(comp_weggooistapels, kaart):
    for stapel in comp_weggooistapels:
        if not comp_weggooistapels[stapel]:
            continue
        if comp_weggooistapels[stapel][-1] == kaart:
            return True, stapel
    return False, None

def beschikbare_kaarten(comp_hand, comp_weggooistapels):
    temp = comp_hand.copy()
    for stapel in comp_weggooistapels:
        if len(comp_weggooistapels[stapel]) > 0:
            temp.append(comp_weggooistapels[stapel][-1])
    return temp

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

    if verschil - 1 != len(pad) and verschil - 1 - len(pad) < 3 and mens_verschil - 1 - len(pad) <= 3:
        pad = []
    return pad

def pad_toepassen(pad, bouwstapels, dichtste_bij, comp_stok, comp_hand, comp_weggooistapels, trekstapel):
    for stap in pad:
        bouwstapels, trekstapel, check_bouwstapels(bouwstapels, trekstapel)

        if stap[0] == "stok":
            bouwstapels[dichtste_bij].append(comp_stok[stap[1]])
            comp_stok = comp_stok[1:]
        elif stap[0] == "hand":
            bouwstapels[dichtste_bij].append(comp_hand[stap[1]])
            comp_hand = comp_hand[:stap[1]] + comp_hand[stap[1] + 1:]
        elif stap[0] == "weggooistapel":
            bouwstapels[dichtste_bij].append(comp_weggooistapels[stap[1]][-1])
            comp_weggooistapels[stap[1]] = comp_weggooistapels[stap[1]][:-1]
    return bouwstapels, comp_stok, comp_hand, comp_weggooistapels, trekstapel

#Test functies
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

def test_kleinste_weggooistapel():
    assert kleinste_weggooistapel({'A': [11, 11, 11], 'B': [10, 9], 'C': [7], 'D': [8, 8]}) == 'C', "Moet C zijn"

def test_check_weggooistapel():
    assert check_weggooistapel([11, 11]) is True, "Moet True zijn"
    assert check_weggooistapel([6, 6, 5]) is False, "Moet False zijn"

def test_kaart_wegleggen():
    assert kaart_wegleggen([8, 3, 11, "SB", 3], {'A': [7, 8], 'B': [8, 8], 'C': [], 'D': []}) == (
        [3, 11, "SB", 3], {'A': [7, 8], 'B': [8, 8, 8], 'C': [], 'D': []}), "Weggooistapel B moet [8, 8, 8] zijn"
    assert kaart_wegleggen([8, 3, 11, "SB", 3], {'A': [], 'B': [], 'C': [], 'D': []}) == (
        [8, 11, "SB", 3], {'A': [3], 'B': [], 'C': [], 'D': []}), "Weggooistapel A moet [3] zijn"
    assert kaart_wegleggen([8, 3, 11, "SB", 3], {'A': [2], 'B': [5], 'C': [12], 'D': [10]}) == (
        [8, 3, "SB", 3], {'A': [2], 'B': [5], 'C': [12, 11], 'D': [10]}), "Weggooistapel C moet [12, 11] zijn"
    assert kaart_wegleggen([8, 3, 11, "SB", 3], {'A': [10, 10], 'B': [7, 7, 7], 'C': [5], 'D': [2, 2]}) == (
        [3, 11, "SB", 3], {'A': [10, 10], 'B': [7, 7, 7], 'C': [5, 8], 'D': [2, 2]}), "Weggooistapel C moet [5, 8] zijn"

def test_check_weggooistapels():
    assert check_weggooistapels({'A': [10, 10, 10], 'B': [7, 6], 'C': [4], 'D': [8, 8]}, 6) == (
        True, "B"), "Moet (True, B) zijn"
    assert check_weggooistapels({'A': [10, 10, 10], 'B': [7], 'C': [4], 'D': [8, 8]}, 6) == (
        False, None), "Moet (False, None) zijn"

def test_beschikbare_kaarten():
    assert beschikbare_kaarten([2, "SB", 8, 12, "SB"], {'A': [6, 6], 'B': [10, 9], 'C': [11, 11, 11], 'D': [7]}) == \
           [2, 'SB', 8, 12, 'SB', 6, 9, 11, 7], "Moet [2, 'SB', 8, 12, 'SB', 6, 9, 11, 7] zijn"

def test_dichtste_bij_stok():
    assert dichtste_bij_stok(
        {'A': [1, 2, 3, 4, 5, 6], 'B': [1, "SB", 3], 'C': [1, 2, 3, 4], 'D': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        ["SB", 2, 9, 6, 11, 8, 12], [5, 7, 3, 9, "SB"],
        {'A': [6, 6], 'B': [10, 9], 'C': [11, 11, 11], 'D': [7]}) == "B", "Moet B zijn"
    assert dichtste_bij_stok(
        {'A': [1, 2, 3, 4, 5, 6], 'B': [1, "SB", 3], 'C': [1, 2, 3, 4], 'D': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
        [6, 2, 9, "SB", 11, 8, 12], [5, 7, 3, 9, "SB"],
        {'A': [6, 6], 'B': [10, 9], 'C': [11, 11, 11], 'D': [7]}) == "C", "Moet C zijn"

def test_pad_maken():
    assert pad_maken({'A': [1, 2, 3, 4, 5, 6, 7], 'B': [1, "SB", 3], 'C': [1], 'D': [1, 2, 3, 4, 5, 6, 7, 8]},
                     [8, 11, 3, 9, "SB", 7, 2, 8], [7, 2, 9, "SB", 11, 8, 12], [3, 5, 9, "SB", 7],
                     {'A': [6, 6, 5], 'B': [10, 9], 'C': [11, 11, 11], 'D': [7]}) == [], "Moet [] zijn"
    assert pad_maken({'A': [1, 2, 3, 4, 5, 6, 7], 'B': [1, "SB", 3, 4], 'C': [1], 'D': [1, 2, 3, 4, 5, 6, 7, 8]},
                     [6, 11, 3, 9, "SB", 7, 2, 8], [7, 2, 9, "SB", 11, 8, 12], [3, 5, 9, "SB", 7],
                     {'A': [6, 6, 5], 'B': [10, 9], 'C': [11, 11, 11], 'D': [7]}) == [['hand', 1], ['hand', 2], ['stok',
                        0]], "Moet [['hand', 1], ['hand', 2], ['stok', 0]] zijn"

def test_pad_toepassen(trekstapel):
    assert pad_toepassen([['hand', 1], ['hand', 2], ['stok', 0]],
                         {'A': [1, 2, 3, 4, 5, 6, 7], 'B': [1, "SB", 3], 'C': [1], 'D': [1, 2, 3, 4, 5, 6, 7, 8]}, "B",
                         [7, 2, 9, "SB", 11, 8, 12], [3, 5, 9, "SB", 7],
                         {'A': [6, 6, 5], 'B': [10, 9], 'C': [11, 11, 11], 'D': [7]}, trekstapel) == (
           {'A': [1, 2, 3, 4, 5, 6, 7], 'B': [1, 'SB', 3, 5, 'SB', 7], 'C': [1], 'D': [1, 2, 3, 4, 5, 6, 7, 8]},
           [2, 9, 'SB', 11, 8, 12], [3, 9, 7], {'A': [6, 6, 5], 'B': [10, 9], 'C': [11, 11, 11], 'D': [7]},
           trekstapel), "Klopt niet"

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
test_kleinste_weggooistapel()
test_check_weggooistapel()
test_kaart_wegleggen()
test_check_weggooistapels()
test_beschikbare_kaarten()
test_dichtste_bij_stok()
test_pad_maken()
test_pad_toepassen(trekstapel)
print("Tests succesvol")
