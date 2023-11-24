import revenu_brut_auto as auto

######################################################################## Voiture de l'employeur payé par l'employeur utilisé pour le travail
print("*"*50, "218")
cauto = auto.Auto(portion_personnelle=9000, portion_totale=35000)
cauto.advantage_usage(mois=12, prix=28000)
cauto.advantage_fonction(remb_perso=600, choix=1)
print(cauto.calcul()=="3935 0")

######################################################################## Voiture de l'employeur payé par l'employeur utilisé pour usage personnel
print("*"*50, "219")
cauto = auto.Auto(portion_personnelle=20000, portion_totale=30000)
cauto.advantage_usage(mois=10, prix=32000)
cauto.advantage_fonction()
print(cauto.calcul()=="12000 0")
print(cauto.imposable)

######################################################################## Voiture de l'employeur payé par l'employé utilisé pour le travail
print("*"*50, "220")
cauto = auto.Auto(portion_personnelle=2000, portion_totale=50000)
cauto.advantage_usage(mois=12, prix=35000)
cauto.frais_fonctionnement(essence=5250, entretiens_et_reparation=3000, assurance_immatriculation=1400)
print(cauto.calcul()=="840 9264")

######################################################################## Voiture de l'employé payé par l'employeur utilisé pour le travail
print("*"*50, "221")
cauto = auto.Auto(portion_personnelle=9100, portion_totale=35000)
cauto.amort_interet_pret(interet_mois=300, mois=12, prix=25500, amort_prix=0.3)
cauto.advantage_fonction(remb_employeur=9800)
print(cauto.calcul())
print(cauto.calcul()=="2548 8325")