# daten braucht das cursor.fetchall objekt,
# bei args müssen die Überschriften rein

# Beispiel:
# daten = cursor.fetchall()
# toList(daten,"ID","Firma","Vorname","Nachname","Email","Telefonnummer")

# Wenn autoformat.py im gleichen Ordner ist, schreibe am Anfang "from autoformat import toList"

def toList(daten,*args):
    columns = []
    spaces = []

    for arg in args:
        columns.append(arg)   

    for d in daten[0]:
        spaces.append(0)

    for ds in daten:
        for d in ds:
            if len(str(d)) > spaces[ds.index(d)]:
                spaces[ds.index(d)] = len(str(d))

    header = ""
    for head in range(len(columns)):
        if len(columns[head]) > spaces[head]:
            spaces[head] = len(columns[head])
        header += " {:"+str(spaces[head])+"} |"
        header = header.format(columns[head])

    print(header)
    print("-"*len(header))


    for ds in daten:
        line = ""
        for d in range(len(ds)):
            line += " {:"+str(spaces[d])+"} |"
            line = line.format(ds[d])
    
            
        print(line)