abc = "0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzÄabcdefghijkÄäÖöÜüß\!§$%&/()=?²³{[]}*_:;,.-#+~+#'\' "

eingabe = input('Gib was ein:')

list = []
sorted = ''

for b in range(len(eingabe)):                           #für jeden Buchstaben der eingabe (b = index)
    for v in range(len(abc)):                           #für jeden Buchstaben im Alphabet (v = index)
        if abc[v] == eingabe[b]:                        #wenn Buchstaben gleich
            list.append(v)                              #Packe Index des Buchstabens aus dem Alphabet in Liste z.B index 2 für C
            break                                       #Springt zum nächsten Buchstaben der Eingabe (for schleife der 2.Ebene wird abgebrochen)


for num in list:                                        #Für jeden Index in der Liste (kann auch mit eingabe gemacht werden da gleichlang)

    minind = list.index(min(list))                      #Speichet den Index des kleinsten Wertes aus der Liste
    sorted += eingabe[minind]                           #Fügt den Buchstaben aus der Eingabe[Stelle kleinster Wert] der neuen Variablen zu
    eingabe = eingabe[:minind] + eingabe[minind+1:]     #Entfernt Diesen Buchstaben aus der Eingabe
    list = list[:minind] + list[minind+1:]              #Entfernt Den zum Buchstaben gehörigen Index

print(sorted)


            
