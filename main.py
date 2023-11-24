# si patron, 1e
#   si perso | affaire fin

# avantage, 1e

# nombre, 1 mot
# dollar relié, prix_1 mot

# Dépenses personnelles
# prime d'assurance-vie, médicale et dentaire
# honoraire pour déclaration de revenus

import deduction_permise
from datetime import datetime

def revenu_interet(pret = 0, taux_interet = 0.0, nb_jour = 0):
  return pret * taux_interet * nb_jour / 365

def day_of_year(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_year = date.timetuple().tm_yday
        return day_of_year
    except ValueError:
        print("[ERREUR] day_of_year format invalide")
        return 0

def revenu_net_biens(revenu_interet = 0, interet_obligation = 0):
  return revenu_interet + interet_obligation






print("*"*50, "244")
revenu = rn.a(revenu_net_emploi=70000, prestation_consecutive_deces=[25000, deduction_permise.beneficiaire([25000])])
gain_perte = 0
gain_perte_cum = revenu + gain_perte
deduction_ap = 4000
deduction = c(pension_ex=6000, frais_demenagement=deduction_permise.frais_demenagement(km_proximite_travail_etude=20, repas_par_jour=100/15, logement_par_jour=800/15, jour=15, resiliation_bail=500, demenagement=1900, entreposage=920), b=gain_perte_cum) - deduction_ap
deduction_cum = gain_perte_cum - deduction
perte_entreprise = 0
total = revenu + gain_perte - deduction - perte_entreprise
print(revenu,"+", gain_perte, "-", deduction, "-", perte_entreprise, "=", total) # 85000 + 0 - 6220 - 0 = 78780

  
print("*"*50, "245")
rbe = revenu_net_emploi(salaire_brut=83000, patron_frais_representation=2700, patron_cot_reer=1500)
dah = deductible_art_huit(rpa=3800)
rne = rbe - dah
revenu = a(revenu_net_emploi=rne, prestation_consecutive_deces=[15000, deduction_permise.beneficiaire([15000])], allocation_depart_retraite=100000, rpa=12000, psv=3025, rrq=7500)
gain_perte = 0
gain_perte_cum = revenu + gain_perte
deduction_ap = 0
deduction = c(frais_demenagement=deduction_permise.frais_demenagement(km_proximite_travail_etude=0,demenagement=1200, jour=1), reer=20000+2500, frais_opposition=300, b=gain_perte_cum, psv=3025) - deduction_ap
deduction_cum = gain_perte_cum - deduction
perte_entreprise = 0
total = revenu + gain_perte - deduction - perte_entreprise
print(revenu,"+", gain_perte, "-", deduction, "-", perte_entreprise, "=", total) # 210925 + 0 - 25825 - 0 = 185100

######################################################################### deduction_permise



# print("*"*50, "240")
# frais_de_garde = deduction_permise.frais_de_garde(age_enfant=[5,9,17], revenu=13500, cpe=2500, colonie_vac=[400,2], gardiennage=0)
# print(frais_de_garde) # 2750