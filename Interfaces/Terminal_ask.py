########## QUESTIONS SUR UN TERMINAL ###########

# Récupère un entier naturel
def terminal_input_num(question, message):
    if len(str(question)) > 0:
        print(str(question))
    input_num = input(str(message) + " : ")
    while not input_num.isnumeric():
        input_num = input("(" + str(message) + ") Entrer un nombre : ")
    return int(input_num)


# Récupère un entier naturel borné
def terminal_input_num_borne(question, min, max):
    min, max = ordonne(min, max)
    if min < 0:
        min = 0
        if max < 0:
            return 0
    if len(str(question)) > 0:
        input_num = input(str(question) + " ")
    else:
        input_num = input(" Attend entre " + str(min) + " et " + str(max) + " : ")
    while not input_num.isnumeric() or (int(input_num) < min or int(input_num) > max):
        input_num = input(" Attend entre " + str(min) + " et " + str(max) + " : ")
    return int(input_num)


# Récupère deux bornes sur les entiers natuels
def terminal_input_bornes_range(question, min, max):
    min, max = ordonne(min, max)
    if min < 0:
        min = 0
        if max < 0:
            return 0, 0
    if len(str(question)) > 0:
        print(str(question))
    input_num_max = input("Valeur max : ")
    while not input_num_max.isnumeric() or (
        int(input_num_max) <= min or int(input_num_max) > max
    ):
        input_num_max = input(
            " Attend entre " + str(min + 1) + " et " + str(max) + " : "
        )
    input_num_max = int(input_num_max)
    if input_num_max == 0:
        return 0, 0
    input_num_min = input("Valeur min : ")
    while not input_num_min.isnumeric() or (
        int(input_num_min) < min or int(input_num_min) > input_num_max
    ):
        input_num_min = input(
            " Attend entre " + str(min) + " et " + str(input_num_max) + " : "
        )
    return int(input_num_min), input_num_max


# Récupère un booléen
def terminal_question_On(question, message, def_text, default):
    if len(str(question)) > 0:
        print(str(question))
    input_On = input(str(message) + " (O/n default: " + str(def_text) + ") : ")
    while not (input_On == "O" or input_On == "n" or input_On == ""):
        input_On = input(str(message) + " (O/n default: " + str(def_text) + ") : ")
    if input_On == "O" or (input_On == "" and default):
        input_On = True
    else:
        input_On = False
    return input_On


# Récupère l'indice d'un choix sur une liste
def terminal_question_choice(question, choices):
    if len(str(question)) > 0:
        print(str(question))
    for i in range(len(choices)):
        print("\t " + str(i) + " : " + str(choices[i]))
    input_c = terminal_input_num_borne("",0,len(choices)-1)
    return int(input_c)


# Récupère un ensemble (suite de numéros entiers et/ou intervalles)
def terminal_ensemble_num(question):
    ##### indices des graphes qui nous intéressent
    set_res = set()
    print(question)
    while len(set_res) == 0:
        error = False
        user_input = input("Entrer un ensemble : ")
        splited = user_input.replace(" ", "").split(",")
        for part in splited:
            if "-" in part:
                part = part.split("-")
                if len(part) != 2:
                    error = True
                else:
                    if part[0].isnumeric() and part[1].isnumeric():
                        if int(part[0]) >= 0 and int(part[0]) < int(part[1]):
                            for i in range(int(part[0]), int(part[1]) + 1):
                                set_res.add(i)
                        else:
                            error = True
                    else:
                        error = True
            else:
                if part == "*":
                    set_res.add(-1)
                    error = False
                    break
                if part.isnumeric():
                    if int(part) >= 0.0:
                        set_res.add(int(part))
            if error:
                break
        if error:
            set_res.clear()
            print("Valeurs supérieur à 0")
            print("* : toutes les valeurs possibles")
            print("x-y : de x à y")
            print("x,y : x et y")
    return sorted(set_res)


# fonction utilitaire qui ordonne deux numéros
def ordonne(x, y):
    if x > y:
        return y, x
    return x, y
