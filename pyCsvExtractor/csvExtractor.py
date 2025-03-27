import csv
import ast
import random as r
from Binarytree import Binarytree as Bt


def buffedList(ly: list, upper: int) -> list:
    ext = []
    for x in range(upper):
        ext.append(False)
    return ly.extend(ext)


def printT(tab):
    for cell in tab:
        print(cell)


def randomDate() -> str:
    a = str(r.randint(1900, 2008))
    m = str(r.randint(1, 12))
    j = str(r.randint(1, 30))
    if len(m) < 2:
        m = "0" + m
    if len(j) < 2:
        j = "0" + j
    return a + "--" + m + "--" + j


def randomDate(aa, mm, jj) -> str:
    a = str(r.randint(aa, 2024))
    if (int(a) == aa):
        m = str(r.randint(mm, 12))
        j = str(r.randint(1, 28))
    else:
        m = str(r.randint(1, 12))
        j = str(r.randint(1, 30))
    if len(m) < 2:
        m = "0" + m
    if len(j) < 2:
        j = "0" + j
    return a + "-" + m + "-" + j


def randomTime() -> str:
    h = str(r.randint(0, 23))
    m = str(r.randint(0, 59))
    if len(m) < 2:
        h = "0" + h
    if len(h) < 2:
        m = "0" + m
    return h + ":" + m


def sintaxSoft(cell: str):
    cell = cell.removeprefix("[")
    cell = cell.removesuffix("]")
    cell = cell.replace("}, ", ("}//#"))
    return cell


def tabStrToDict(tab):
    res = []
    for x in tab:
        res.append(ast.literal_eval(x))
    return res


def buildTabLigne(ligne):
    res = {}
    i = 0
    for cell in ligne:
        cell = str(cell)
        if i == 0:
            cell = sintaxSoft(cell)
            cell = cell.split("//#")
            cell = tabStrToDict(cell)
            res.setdefault("Actor", cell)
        # elif i == 1:
        #     # cell = sintaxSoft(cell)
        #     # cell = cell.split("//#")
        #     # cell = tabStrToDict(cell)
        #     # res.setdefault("Staff", cell)
        else:
            res.setdefault("Num", -1)
        i += 1
    return res


def splitName(s: str):
    res = []
    res = s.split(" ")
    if len(res) < 2:
        res.append("Roget")
    return res


def getActor(tab, accActor: list, acc: list):
    for x in tab:
        ligne = []
        x = dict(x)
        if (x.get("id") not in acc):
            names = splitName(x.get("name"))
            ligne.append(x.get("id"))  # id
            ligne.append(names[0])  # prénom
            ligne.append(names[1])  # Nom
            ligne.append(randomDate())  # date de naissance
            accActor.append(ligne)
            acc.append(x.get("id"))

    return (accActor, acc)


def writeCsv(path: str, name: str, tab: list):
    write_file = open(path + "/"+name+".csv",
                      'w', newline='', encoding="utf-8")
    writer = csv.writer(write_file, delimiter=',')
    writer.writerows(tab)


def cinéma(pathIn: str, pathOut: str):
    res = []
    acc = []
    id = 0
    read_file = open(pathIn)
    reader = csv.reader(read_file, delimiter=',')
    for row in reader:
        if (row[3]not in acc):
            adr = row[4]+", "+row[5]+", "+row[6]+", "+row[7]
            res.append([id, row[3], adr])
            id += 1
            acc.append(row[3])
    writeCsv(path=pathOut, name="cinema", tab=res)


def getDirector(reader, id):
    for row in reader:
        if row[2] == id:
            cell = sintaxSoft(row[1])
            cell = cell.split("//#")
            cell = tabStrToDict(cell)
            for staf in cell:
                staf = dict(staf)
                if staf.get("job") == "Director":
                    return staf.get("name")


def getGenre(cell):
    cell = sintaxSoft(cell)
    cell = cell.split("//#")
    cell = tabStrToDict(cell)
    genre = dict(cell[0])
    return genre.get("name")


def filmCsv(pathOut: str):
    res = []
    i = 0
    read_file = open("csv_source/movies_metadata.csv", "r", encoding="UTF-8")
    reader = csv.reader(read_file, delimiter=',')
    read_file2 = open("csv_source/credits.csv", "r", encoding="UTF-8")
    reader2 = csv.reader(read_file2, delimiter=',')
    accID = []
    for row in reader:
        ligne = []
        try:
            id = row[5]
            if id not in accID:
                ligne.append(id)  # ID
                ligne.append(row[20])  # titre
                ligne.append(getDirector(reader2, id))  # real
                ligne.append(row[14])  # sorti
                ligne.append(row[16])  # duré
                ligne.append(getGenre(row[3]))  # genre
                res.append(ligne)
                accID.append(id)
        except:
            print(i)
            i += 1
    writeCsv(path=pathOut, name="films", tab=res)


def joue(pathOut: str):
    res = []
    i = 0
    l = 0
    read_file = open("csv_source/credits.csv", "r", encoding="UTF-8")
    reader = csv.reader(read_file, delimiter=',')
    for row in reader:
        try:
            cell = sintaxSoft(row[0])
            cell = cell.split("//#")
            cell = tabStrToDict(cell)
            for actor in cell:
                actor = dict(actor)
                ligne = []
                id_film = row[2]
                id_actor = actor.get("id")
                character = actor.get("character")
                if ((id_actor and id_film and character) is not ""):
                    ligne.append(id_film)
                    ligne.append(id_actor)
                    ligne.append(character)
                    res.append(ligne)
        except:
            print(str(i) + " -- " + str(l))
            i += 1
        l += 1
    writeCsv(path=pathOut, name="joue", tab=res)


def cleanJoue():
    root = Bt()
    idFilms = Bt()
    read_films = open("csv_out/films.csv", "r", encoding="UTF-8")
    films = csv.reader(read_films, delimiter=',')
    for f in films:
        idFilms.insert(f[0])
    i = 0
    res = []
    read_file = open("csv_out/joue.csv", "r", encoding="UTF-8")
    reader = csv.reader(read_file, delimiter=',')
    for row in reader:
        hashId = hash((int(row[0]), int(row[1])))  # calc hash
        if (not root.shear(hashId) and idFilms.shear(row[0])):
            res.append([row[0], row[1], row[2]])
            root.insert(hashId)
        if (i % 1000 == 0):
            print(i)
        i += 1
    writeCsv(path="csv_out", name="joue", tab=res)


def salle(pathOut: str):
    res = []
    i = 0
    id_sall = 0
    read_file = open("csv_out\cinema.csv", "r", encoding="UTF-8")
    reader = csv.reader(read_file, delimiter=',')
    for cinéma in reader:
        nb_salles = r.randint(1, 25)
        for salle in range(nb_salles):
            ligne = []
            ligne.append(id_sall)
            ligne.append(r.randint(120, 3500))
            ligne.append(cinéma[0])
            res.append(ligne)
            id_sall += 1
    writeCsv(path=pathOut, name="salle", tab=res)


def randTypeSeance() -> str:
    typeSeance = ["Standard", "3D", "Ciné-debat",
                  "Avant-Première"]
    r1 = r.randint(0, 3)
    r2 = r.randint(0, 1)
    r3 = r.randint(0, 1)
    if r1 is 0 or r2 is 0 or r3 is 0:
        return typeSeance[0]
    else:
        return typeSeance[r1]

# def randDateAfter(date : str) -> str:
#     year = date
#     if r1 or r2 is 0:
#         return typeSeance[0]
#     else:
#         return typeSeance[r1]


def getDate(date: str):
    return (int(date[0:4]), int(date[5:7]), int(date[8:10]))


def seance(pathOut: str) -> any:
    err = 0
    res = []
    id_Seance = 0
    read_films = open("csv_out/films.csv", "r", newline='', encoding="UTF-8")
    films = read_films.readlines()
    lenFilms = len(films)
    read_salles = open("csv_out/cinema.csv", "r", encoding="UTF-8")
    salles = csv.reader(read_salles, delimiter=',')
    for salle in salles:
        nb_seance = r.randint(50, 1000)
        for seance in range(nb_seance):
            try:
                ligne = []
                rdFilm = r.randint(0, lenFilms)
                film = films[rdFilm].split(",")
                ligne.append(id_Seance)  # id seance
                ligne.append(randTypeSeance())  # Type
                date = getDate(film[3])
                ligne.append(randomDate(*date))  # Date
                ligne.append(salle[0])  # idSalle
                ligne.append(int(film[0]))
                res.append(ligne)
                id_Seance += 1
            except:
                err += 1
                print(err)
    writeCsv(path=pathOut, name="seance", tab=res)


def getLieuProd(id: int) -> str:
    read_file = open("csv_source/movies_metadata.csv", "r", encoding="UTF-8")
    reader = csv.reader(read_file, delimiter=',')
    for cell in reader:
        if id == cell[5]:
            try:
                prod = sintaxSoft(cell[13])
                prod = prod.split("//#")
                prod = tabStrToDict(prod)[0]
                prod = dict(prod)
                return prod.get("name")
            except:
                print(id)
                return "NONE"


def typeImpact() -> str:
    typeSeance = ["CO2", "Electrique", "Hydrique",
                  "Sonor"]
    r1 = r.randint(0, 3)
    r2 = r.randint(0, 1)
    if r1 is 0 or r2 is 0:
        return typeSeance[0]
    else:
        return typeSeance[r1]


def impactFilm(pathOut: str) -> any:
    idFilms = Bt()
    err = 0
    id_EmprintC = 0
    res = []
    read_file = open("csv_out/films.csv", "r", encoding="UTF-8")
    reader = csv.reader(read_file, delimiter=',')
    for film in reader:
        idFilms.insert(film[0])
    read_file2 = open("csv_source/movies_metadata.csv", "r", encoding="UTF-8")
    reader2 = csv.reader(read_file2, delimiter=',')
    for film in reader2:
        if idFilms.shear(film[5]):
            try:
                ligne = []
                ligne.append(film[5])
                ligne.append(id_EmprintC)
                ligne.append(typeImpact())
                prod = sintaxSoft(film[13])
                prod = prod.split("//#")
                prod = dict(tabStrToDict(prod)[0])
                ligne.append(prod.get("name"))
                res.append(ligne)
                id_EmprintC += 1
                if id_EmprintC % 1000 == 0:
                    print("--->" + str(id_EmprintC))
            except:
                err += 1
                print(err)
    writeCsv(path=pathOut, name="impact_film", tab=res)


def typeBillet() -> str:
    typeB = ["Standard", "VIP", "Enfant",
                "Etudient"]
    r1 = r.randint(0, 3)
    r2 = r.randint(0, 1)
    if r1 is 0 or r2 is 0:
        return typeB[0]
    else:
        return typeB[r1]


def Billet(pathOut: str):
    res = []
    id_Billet = 0
    read_file = open("csv_out/seance.csv", "r", encoding="UTF-8")
    reader = csv.reader(read_file, delimiter=',')
    for seance in reader:
        nb_Billet = r.randint(0, 50)
        nb_Billet2 = r.randint(0, 50)
        for billet in range(min(nb_Billet2,nb_Billet)):
            ligne = []
            typeB = typeBillet()
            rdDPrix = r.randint(0, 9)
            rdPrix = r.randint(5, 25)
            match typeB:
                case "VIP":
                    rdPrix += 5.0
                case "Enfant":
                    rdPrix -= 4.0
                case "Etudient":
                    rdPrix -= 2.0
            ligne.append(id_Billet)
            ligne.append(rdPrix + rdDPrix*0.1)
            ligne.append(typeB)
            ligne.append(seance[0])
            res.append(ligne)
            id_Billet += 1
            if id_Billet % 10000 == 0:
                print("--->" + str(id_Billet))
    writeCsv(path=pathOut, name="billet", tab=res)
    
def typeEP()->str :
    typeSeance = ["Essence", "Electrique", "Deplacement"]
    r1 = r.randint(0, 2)
    r2 = r.randint(0, 1)
    if r1 is 0 or r2 is 0:
        return typeSeance[0]
    else:
        return typeSeance[r1]
    
def EC(pathOut: str)->any :
    err = 0
    res = []
    id_EP = 0
    read_file = open("csv_out/films.csv", "r", encoding="UTF-8")
    reader = csv.reader(read_file, delimiter=',')
    for film in reader:
        try :
            ep = r.randint(50,900000)
            epD = r.randint(0,99)*0.01
            ligne = []
            ligne.append(id_EP)
            ligne.append(typeEP())
            ligne.append(ep+epD)
            ligne.append(randomDate(*getDate(film[3])))
            ligne.append(film[0])
            res.append(ligne)
            id_EP += 1
        except :
            err+=1
            print(err)
    writeCsv(path=pathOut, name="empreinteCarbone", tab=res)

def impactSalle(pathOut: str)->any :
    res = []
    id_impactSalle = 0
    read_file = open("csv_out/salle.csv", "r", encoding="UTF-8")
    reader = csv.reader(read_file, delimiter=',')
    for salle in reader:
        ligne = []
        ligne.append(id_impactSalle)
        ep = r.randint(50,900000)
        epD = r.randint(0,99)*0.01
        ligne.append(ep+epD)
        ligne.append(r.randint(0,1)==0)
        ligne.append(randomDate(2005,1,1))
        ligne.append(salle[0])
        id_impactSalle+=1
        res.append(ligne)
    writeCsv(path=pathOut, name="empreinteSalle", tab=res)


print("-"*60 + ">START")
# impactFilm("csv_out")
print("-"*60 + ">END")
