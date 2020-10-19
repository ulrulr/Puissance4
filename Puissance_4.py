#Module
import random

#Fonctions utiles pour le programme

def afficher(plateau):
    for i in range(len(plateau)) :
        print(plateau[i], end = '')
        if (i+1)%12 == 0 :
            print()

def actions(plateau):
    liste = []
    for i in range(len(plateau)) :
        if i in [j for j in range(60,72)] :
            if plateau[i] == '.' :
                liste.append(i)
        else :
            if plateau[i] == '.' and plateau[i+12] != '.' :
                liste.append(i)
    return liste

def result(plateau, act):
    global joueur
    if plateau[act] != '.' :
        print("Cette case est déjà occupée.")
        return
    if act not in actions(plateau) :
        print("Impossible de jouer cette case.")
        return
    plateau[act] = joueurs[joueur]
    joueur = (joueur + 1) % 2

def terminal(plateau):
    res = '.'
    #Ligne
    for i in range(len(plateau)) :
        if i%12 in [j for j in range(9)] :
            if (plateau[i] != '.') and (plateau[i]==plateau[i+1]==plateau[i+2]==plateau[i+3]) :
                res = plateau[i]
    #Colonne
    for i in range(36) :
        if (plateau[i] != '.') and (plateau[i]==plateau[i+12]==plateau[i+24]==plateau[i+36]) :
            res = plateau[i]
    #Diagonale
    for i in range(36) :
        if i%12 in [j for j in range(9)] :
            if (plateau[i] != '.') and (plateau[i]==plateau[i+13]==plateau[i+26]==plateau[i+39]) :
                res = plateau[i]
    #Diagonale
    for i in range(36) :
        if i%12 in [j for j in range(3,12)] :
            if (plateau[i] != '.') and (plateau[i]==plateau[i+11]==plateau[i+22]==plateau[i+33]) :
                res = plateau[i]
    if res != '.' :
        return True
    if nombre(plateau) == 42:
        return True
    return False

def utility(plateau):
    plateau_coeff =[0,10,20,30,40,50,50,40,30,20,10,0,20,30,40,50,60,60,60,60,50,40,30,20,30,40,50,60,70,80,80,70,60,50,40,30,40,50,60,70,70,80,80,70,70,60,50,40,50,60,70,80,90,90,90,90,80,70,60,50,50,60,70,80,90,100,100,90,80,70,60,50]
    gagnant = gagner(plateau)
    if gagnant == 'X':
        return 100 - nombre(plateau) + plateau_coeff[act]
    elif gagnant == 'O':
        return -100 +  nombre(plateau) - plateau_coeff[act]
    else:
        return 0

def gagner(plateau):
    res = '.'
    #Ligne
    for i in range(len(plateau)) :
        if i%12 in [j for j in range(9)] :
            if (plateau[i] != '.') and (plateau[i]==plateau[i+1]==plateau[i+2]==plateau[i+3]) :
                res = plateau[i]
    #Colonne
    for i in range(36) :
        if (plateau[i] != '.') and (plateau[i]==plateau[i+12]==plateau[i+24]==plateau[i+36]) :
            res = plateau[i]
    #Diagonale
    for i in range(36) :
        if i%12 in [j for j in range(9)] :
            if (plateau[i] != '.') and (plateau[i]==plateau[i+13]==plateau[i+26]==plateau[i+39]) :
                res = plateau[i]
    #Diagonale
    for i in range(36) :
        if i%12 in [j for j in range(3,12)] :
            if (plateau[i] != '.') and (plateau[i]==plateau[i+11]==plateau[i+22]==plateau[i+33]) :
                res = plateau[i]
    if nombre(plateau) == 9:
        return 'Jeu fini'
    return res

def nombre(plateau):
    compteur = 0
    for i in range(9) :
        if plateau[i] != '.' :
            compteur = compteur+1
    return compteur

def annuler(plateau, act):
    global joueur
    plateau[act] = '.'
    joueur = (joueur + 1) % 2

def score(plateau, act, fonction,a,b, profondeur):
    result(plateau, act)
    score = fonction(plateau,a,b,profondeur)
    annuler(plateau, act)
    return score

#Fonction Alpha/Beta

def Alpha_Beta_Search(plateau,profondeur):
    print(profondeur)
    maxi = None
    meilleurindex = None
    global act
    for act in actions(plateau):
        result(plateau, act)
        tmp = Min_Value(plateau,-1000,1000,profondeur - 1)
        if maxi is None or tmp > maxi :
            maxi = tmp
            meilleurindex = act
        annuler(plateau, act)
    return meilleurindex

def Min_Value(plateau,a,b,profondeur):
    if profondeur == 0 or terminal(plateau):
        return utility(plateau)
    v = +1000
    for act in actions(plateau) :
        v = min(v,score(plateau, act, Max_Value,a,b,profondeur - 1))
        if v <= a :
            return v
        b = min(b,v)
    return v

def Max_Value(plateau,a,b,profondeur):
    if profondeur == 0 or terminal(plateau) :
        return utility(plateau)
    v = -1000
    for act in actions(plateau) :
        v = max(v,score(plateau, act, Min_Value,a,b,profondeur - 1))
        if v >= b :
            return v
        a = max(a,v)
    return v


#Programme

#Initialisation

IA = 0
JOUEUR = 1
joueurs = {IA: 'X', JOUEUR: 'O'}

joueur = random.choice([IA, JOUEUR])

plateau = ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.']
afficher(plateau)
print()


if joueur == IA :
    result(plateau, random.randint(60,71))
    joueur = JOUEUR
    afficher(plateau)

#Déroulement de la partie
while terminal(plateau) == False:
    if joueur == IA:
        position = Alpha_Beta_Search(plateau,6)
    else:
        ligne = int(input("Quelle ligne voulez vous jouer? (Saisissez un entier entre 0 et 5)"))
        colonne = int(input("Quelle colonne voulez vous jouer? (Saisissez un entier entre 0 et 11)"))
        position = 71 - ligne*12  - 11 + colonne
    result(plateau, position)
    print()
    afficher(plateau)

#Fin de partie et affichage du résultat
gagnant = gagner(plateau)
if gagnant == 'X':
    print("L'IA a gagné")
elif gagnant == 'O':
    print("Vous avez gagné")
else:
    print("Aucun gagnant")
