import json
import sys
import colorama
from colorama import Fore, Style


class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_data(data):
        # Transforme les données choix tuple (titre, bool bonne réponse) --> [choix1, choix2...]
        choix = [i[0] for i in data["choix"]]
        # Trouve le bon choix en fonction du bool "bonne réponse"
        bonne_reponse = [i[0] for i in data['choix'] if i[1]]
        # Si aucune bonne reponse ou plusieurs bonnes reponses --> Anomalie dans les données
        if len(bonne_reponse) != 1:
            return None
        q = Question(data['titre'], choix, bonne_reponse[0])
        return q

    def poser(self, num_question, nb_questions):
        print(f" QUESTION {num_question} sur {nb_questions}")
        print()
        print("  " + self.titre)
        print()
        for i in range(len(self.choix)):
            print("  ", i + 1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int - 1].lower() == self.bonne_reponse.lower():
            print(Fore.GREEN + " Bonne réponse")
            print(Style.RESET_ALL)
            resultat_response_correcte = True
        else:
            print(Fore.RED + " Mauvaise réponse")
            print(Style.RESET_ALL)

        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input(" Votre réponse (entre " + str(min) + " et " + str(max) + ") : ")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)


class Questionnaire:
    def __init__(self, questions, categorie, titre, difficulte):
        self.questions = questions
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte

    def from_data(data):
        questionnaire = data['questions']
        questions = [Question.from_data(i) for i in questionnaire]
        # Supprime les questions None (qui n'ont pas pu être créées)
        questions = [i for i in questions if i]

        return Questionnaire(questions, data['categorie'], data['titre'], data['difficulte'])

    def from_file(filename):
        try:
            file = open(filename, "r")
            json_data = file.read()
            file.close()
            data = json.loads(json_data)
        except:
            print("Exception lors de l'ouverture ou de la lecture du fichier ")
            return None
        return Questionnaire.from_data(data)

    def lancer(self):
        score = 0
        nb_questions = len(self.questions)
        print()
        print("------------------------------")
        print(" QUESTIONNAIRE: " + self.titre)
        print("   Categorie: " + self.categorie)
        print("   Difficulte: " + self.difficulte)
        print("   Nombre de question: " + str(nb_questions))
        print("------------------------------")
        print()

        for i in range(nb_questions):
            question = self.questions[i]
            if question.poser(i + 1, nb_questions):
                score += 1
        if score >= 5:
            print(Fore.GREEN + "Score final :", score, "sur", len(self.questions))
            print(Style.RESET_ALL)
        else:
            print(Fore.RED + "Score final :", score, "sur", len(self.questions))
            print(Style.RESET_ALL)
        return score


#Questionnaire.from_file("arts_museedulouvre_debutant.json").lancer()

if len(sys.argv) < 2:
    print("ERREUR; Vous devez spécifier le nom du fichier JSON à charger")
    exit(0)

json_filename = sys.argv[1]
questionnaire = Questionnaire.from_file(json_filename)
if questionnaire:
    questionnaire.lancer()
