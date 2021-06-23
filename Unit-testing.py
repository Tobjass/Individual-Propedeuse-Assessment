def bovenste_kaart_bouwstapel(bouwstapel):
    if not bouwstapel:
        return 0
    elif len(bouwstapel) == 1:
        return 1
    elif bouwstapel[-1] == "SB":
        return bovenste_kaart_bouwstapel(bouwstapel[:-1]) + 1
    else:
        return bouwstapel[-1]

def test_bovenste_kaart_bouwstapel():
    assert bovenste_kaart_bouwstapel([1, 2, 3, "SB"]) == 4, "Moet 4 zijn"

test_bovenste_kaart_bouwstapel()
print("Tests succesvol")