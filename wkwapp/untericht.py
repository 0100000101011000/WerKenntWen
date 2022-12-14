def Prim(a:int=None,b:int=None):
    import math

    list = []
    auto = False
    if a == None:
        a = int(input('Primzahlen von:'))
        b = int(input('Bis:'))
    else:
        auto = True

    for z in range(a, b+1):

        prim = True

        for i in range(2, int(math.sqrt(z))+1):
            if z % i == 0:
                prim = False
                break

        if z == 1:
            prim = False

        if prim:
            if not auto:
                print(z)
            else:
                list.append(z)
    if auto:
        return list
                


def Fussgesteuert():
    while True:
        print('\nHauptmenü')
        print('========')
        print('1 -> Tu was')
        print('9 -> Abbruch')
        a = input('Bitte Auswählen>')
        if a == '1':
            print('Jaja, ich mach ja was')
        if a == '9':
            break

    print('***Ende***')


def einmaleins():
    for x in range(1, 11):
        for y in range(1, 11):
            print('{:3}'.format(x*y), end=' ')
        print()


def aufgabe():
    n = 10
    fakult = 1

    for i in range(1, n+1):
        fakult *= i
        print(fakult)


def myapp():

    import statistics

    liste = [77, 32, 1, 98, 55, 22, 13, 8, 44, 72]

    minimal = min(liste)
    maximal = max(liste)
    mittelwert = statistics.mean(liste)

    liste.sort()

    def wahrscheinlichkeit(*args):
        wahr = 1
        for arg in args:
            wahr *= arg
        return wahr

    p = round(1/(wahrscheinlichkeit(4, 6)-1)*100, 2)

    print(p)


def matrix():
    n = 0
    for i in range(10):
        for j in range(10):
            print('{:2}'.format(j+n), end=' ')
        n += 10
        print()


def planeten():

    import csv

    u=['Name', 'Entf_Sonne(AE)', 'Radius(km)', 'Monde']
    s=['--------', '--------------', '----------', '-----']
    merkur = ['Merkur', 0.39, 2440, 0]
    venus = ['Venus', 0.72, 6052, 0]
    erde = ['Erde', 1.00, 6378, 1]
    mars = ['Mars', 1.52, 3397, 2]
    jupi = ['Jupiter', 5.20, 71493, 79]
    saturn = ['Saturn', 9.54, 60267, 82]
    uranus = ['Uranus', 19.19, 25559, 27]
    neptun = ['Neptun', 30.07, 24764, 14]

    planeten = []


    planeten.append(merkur)
    planeten.append(venus)
    planeten.append(erde)
    planeten.append(mars)
    planeten.append(jupi)
    planeten.append(saturn)
    planeten.append(uranus)
    planeten.append(neptun)


    fo = open("planeten.csv","w")
    writeobj = csv.writer(fo, delimiter=";", lineterminator="\n", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

    writeobj.writerows(planeten)
    fo.close()


    print(f"|{u[0]:8}|    {u[1]:14}|   {u[2]:10}|    {u[3]:5}  |")
    print("|--------+------------------|-------------|-----------|")

    for ds in planeten:
        print(f"|{ds[0]:8}| {ds[1]:14.2f}   | {ds[2]:10}  |    {ds[3]:5}  |")

planeten()

def zahlenraten():

    import random

    ratenzahl = random.randint(0,99)
    gefunden = False
    while not gefunden:
        Eingabe = int(input("Rate die Zahl:"))
        if Eingabe < ratenzahl:
            print("Zu klein!")
        elif Eingabe > ratenzahl:
            print("Zu groß!")
        else:
            print("Treffer!")
            gefunden = True

def prim200():
    
    list = Prim(1,1224)
    start = 0

    for i in range(20):

        for j in range(start,start+10):
            print("{:5}".format(list[j]), end=" ")
        start += 10
        print()

def km_mi(km):
    mi = km * 0.621371
    return mi

def mi_km(mi):
    km = mi * 1.60934
    return km