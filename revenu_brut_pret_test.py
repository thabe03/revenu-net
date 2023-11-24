import revenu_brut_pret

print("*"*50, "222")
avantage_imposage = revenu_brut_pret.pret(pret=20000, taux_reduit=1, taux=[0,4,3,5], start=revenu_brut_pret.index_mois("2023-04-01"), end=12, pour_travail=1)
print(avantage_imposage==450)

print("*"*50, "223")
avantage_imposable = revenu_brut_pret.pret([2000,revenu_brut_pret.index_trimestre("2023-06-01")], taux_reduit=0, pret=60000, taux=[0,4,3,4], pour_travail=0, start=revenu_brut_pret.index_mois("2023-04-01"), end=12)
print(avantage_imposable==1615)