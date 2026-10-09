"""Knäcker chiffret i FRA_krypto.py.

Kör: python solve.py

Chiffret är en kolumntransposition med nyckel: klartexten skrivs rad för rad
i ett rutnät med W kolumner, och kolumnerna läses ut i en hemlig ordning.
Vi testar alla kolumnordningar för W = 2..8 och poängsätter resultatet med
svensk trigramstatistik (inkl. Å, Ä, Ö).
"""
import math
import sys
from collections import Counter
from itertools import permutations

sys.stdout.reconfigure(encoding="utf-8")
from FRA_krypto import krypto

ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"

# Liten svensk referenstext för trigramstatistik.
REFERENS = """
Det var en gång en liten pojke som bodde i ett rött hus vid sjön tillsammans med sin mor och far.
Varje dag gick han till skolan och lärde sig att läsa och skriva. Han tyckte om att vara ute i
skogen och titta på fåglarna när solen gick ner. Försvarets radioanstalt är en myndighet som
bedriver signalspaning och arbetar med informationssäkerhet. Vi söker dig som vill arbeta med
kryptering och kryptoanalys. Meddelandet ska skickas till staben innan midnatt och får inte läsas
av någon annan. Fienden har förflyttat sina trupper norrut under natten och vi måste agera snabbt.
Om du har knäckt detta chiffer är du välkommen att skicka in din ansökan till oss. Grattis du har
löst uppgiften och nu vet du att det inte var så svårt som det såg ut. Sverige är ett land i norra
Europa med många sjöar och stora skogar. På vintern är det kallt och mörkt men på sommaren är det
ljust nästan hela dygnet. Många svenskar tycker om att fira midsommar med sill och potatis.
Regeringen har beslutat att satsa mer pengar på forskning och utbildning de kommande åren.
Studenterna bygger en racerbil som ska tävla mot andra lag i Europa. Teamet arbetar hårt varje
kväll för att bli klara i tid. Hemligheten finns gömd i texten och den som letar noga hittar den.
Det är viktigt att alla deltagare kommer i tid till mötet på fredag. Glöm inte kartan och kompassen.
"""
ref = "".join(c for c in REFERENS.upper() if c in ALFABET)
TRIGRAM = Counter(ref[i:i + 3] for i in range(len(ref) - 2))
TOTAL = sum(TRIGRAM.values())


def poang(t):
    """Genomsnittlig log-sannolikhet per trigram; högre = mer svenskt."""
    return sum(math.log((TRIGRAM.get(t[i:i + 3], 0) + 0.1) / TOTAL)
               for i in range(len(t) - 2)) / (len(t) - 2)


def dekryptera(text, nyckel):
    """nyckel[i] = vilken kolumn som står som i:e block i kryptotexten."""
    w, n = len(nyckel), len(text)
    rader = -(-n // w)
    fulla = n % w or w  # kolumner som har en bokstav i sista raden
    langd = [rader if k < fulla else rader - 1 for k in range(w)]
    kolumner, pos = {}, 0
    for k in nyckel:
        kolumner[k] = text[pos:pos + langd[k]]
        pos += langd[k]
    return "".join(kolumner[k][r] for r in range(rader) for k in range(w) if r < len(kolumner[k]))


text = krypto.replace(" ", "")
resultat = []
for w in range(2, 9):
    for nyckel in permutations(range(w)):
        klar = dekryptera(text, nyckel)
        resultat.append((poang(klar), w, nyckel, klar))
resultat.sort(reverse=True)

print("Topp 5:")
for p, w, nyckel, klar in resultat[:5]:
    print(f"{p:6.2f}  W={w}  nyckel={nyckel}  {klar}")

_, w, nyckel, klar = resultat[0]
print(f"\nLösning (W={w}, kolumnordning {nyckel}):\n{klar}")
