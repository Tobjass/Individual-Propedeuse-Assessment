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

def test_bovenste_kaart_bouwstapel():
    assert bovenste_kaart_bouwstapel([1, 2, 3, "SB"]) == 4, "Moet 4 zijn"

def test_mogelijkheid():
    assert mogelijkheid(6, {'A': [1, 2], 'B': [1, 2, 3, 4, 5, 6], 'C': [1, 2, "SB"],
                            'D': [1, 2, 3, 4, "SB"]}) is True, "Moet True zijn"
    assert mogelijkheid(10, {'A': [1, 2], 'B': [1, 2, 3, 4, 5, 6], 'C': [1, 2, "SB"],
                             'D': [1, 2, 3, 4, "SB"]}) is False, "Moet False zijn"

test_bovenste_kaart_bouwstapel()
test_mogelijkheid()
print("Tests succesvol")
