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