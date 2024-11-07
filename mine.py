import revenu_net as rn
import revenu_brut as rb
import revenu_brut_auto as auto
import revenu_brut_pret as pret

print("*"*50, "247") # revenu_brut_test
crb =  rb.RevenuBrut()
crb.sb(salaire_net=1751.51*26,impot_fed=229.47*26, impot_prov=287.74*26, rrq=168.30*26, ass_emploi=35.54*26, ass_parentale=13.30*26, rpa=0, ass_collectif=0)
crb.rbe(salaire_brut=crb.salaire_brut)
crb.dah()
crb.calcul()
crn = rn.RevenuNet(crb=crb)
crn.rl(taxes_foncieres=1500, interets_sur_hypotheque=10569, entretien_et_reparation=0, assurances=450, revenu_location=700*12) # crédit d'impôt 423
crn.a()
crn.b()
crn.c()
crn.d()
print(crn.calcul())