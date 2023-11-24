import revenu_net as rn
import revenu_brut as rb


######################################################################### pension pour ancien combattant exclue
print("*"*50, "197")
crn = rn.RevenuNet()
crn.a(revenu_net_emploi=85000)
crn.b(gain_capital_imposable=18000, perte_capital_deductible=20000)
crn.c(4000)
crn.d(perte_entreprise=80000)
print(crn.calcul()=="85000 + 0 - 4000 - 80000 = 1000")

print("*"*50, "198")
crn = rn.RevenuNet()
crn.a(revenu_agricole=53000, revenu_entreprise=28000+2000, revenu_interet=7000)
crn.b(gain_capital_imposable=5000, perte_capital_deductible=9000)
crn.c(reer=2000)
crn.d(perte_entreprise=2000)
print(crn.calcul()=="90000 + 0 - 2000 - 2000 = 86000")

print("*"*50, "199")
crn = rn.RevenuNet()
crn.a(revenu_net_emploi=15500) 
crn.b(gain_capital_imposable=1000, perte_capital_deductible=1500)
crn.c(pension_ex=16000)
crn.d(perte_entreprise=2000)
print(crn.calcul()=="15500 + 0 - 15500 - 0 = 0")

print("*"*50, "201a")
crn = rn.RevenuNet()
crn.a(revenu_net_emploi=50000, revenu_entreprise=2000, revenu_interet=500)
crn.b(gain_capital_imposable=650, perte_capital_deductible=7500, perte_placement=7500)
crn.d()
print(crn.calcul()=="52500 + 650 - 0 - 7500 = 45650")

print("*"*50, "201b")
crn = rn.RevenuNet()
crn.a(revenu_net_emploi=52000, revenu_entreprise=5000, revenu_interet=500)
crn.b(gain_capital_imposable=1000, perte_capital_deductible=3000, perte_placement=1500)
crn.c(pension_ex=6000)
crn.d(perte_entreprise=2000)
print(crn.calcul()=="57500 + 0 - 6000 - 3500 = 48000")

print("*"*50, "201c")
crn = rn.RevenuNet()
crn.a(revenu_net_emploi=45000)
crn.b(gain_capital_imposable=2500, perte_capital_deductible=1500)
crn.c(frais_exploration=20000)
crn.d(perte_loyer=4000, perte_entreprise=10000)
print(crn.calcul()=="45000 + 1000 - 20000 - 14000 = 12000")

print("*"*50, "201d")
crn = rn.RevenuNet()
crn.a(revenu_net_emploi=50000, revenu_interet=1000)
crn.b(gain_capital_imposable=250, perte_capital_deductible=2000)
crn.c(frais_opposition=1300)
crn.d(perte_entreprise=3000)
print(crn.calcul()=="51000 + 0 - 1300 - 3000 = 46700")

print("*"*50, "203")
crn = rn.RevenuNet()
crn.a(revenu_net_emploi=52000, revenu_entreprise=2000, revenu_interet=100, revenu_dividende=800, pension_ex=6000, ferr=400)
crn.b(gain_capital_imposable=1500+500, perte_capital_deductible=9000, perte_placement=9000)
crn.c(frais_opposition=500, frais_demenagement=4000)
crn.d()
print(crn.calcul()=="61420 + 2000 - 4500 - 9000 = 49920")

print("*"*50, "203")
crn = rn.RevenuNet()
crn.a(revenu_net_emploi=13000, pension_ex=6000, ferr=600)
crn.b(gain_capital_imposable=3000, perte_capital_deductible=13600, perte_placement=5600)
crn.d(perte_entreprise=28000, perte_loyer=2000)
print(crn.calcul()=="19600 + 0 - 0 - 19600 = 0")

print("*"*50, "239")
crn = rn.RevenuNet()
print(crn.dd([9000,8000,5000])==[10000, 615, 385])

######################################################################### revenu fractionné

print("*"*50, "242a")
crn = rn.RevenuNet()
crn.a(rpa=70398, psv=7275, rrq=31907)
crn.c()
print(crn.calcul()=="109580 + 0 - 4800 - 0 = 104780")

print("*"*50, "242b")
crn = rn.RevenuNet()
crn.a(psv=7275, rrq=13825)
crn.c()
print(crn.calcul()=="21100 + 0 - 0 - 0 = 21100")

print("*"*50, "242c")
crn = rn.RevenuNet()
crn.a(rpa=70398, psv=7275, rrq=31907)
crn.c(montant_fractionne=0.5)
print(crn.calcul()=="109580 + 0 - 35199 - 0 = 74381")

print("*"*50, "242d")
crn = rn.RevenuNet()
crn.a(psv=7275, rrq=13825+70398*0.5)
crn.c()
print(crn.calcul()=="56299 + 0 - 0 - 0 = 56299")

######################################################################### pension alimentaire périodique et par écrit
print("*"*50, "243")
crn = rn.RevenuNet()
crn.a(prestation_retraite=25000, allocation_depart_retraite=20000, police_ass=50000, bourse_etude=4500)
crn.c(frais_proc_ass_emploi=500,pension_ex=15000, frais_scolarite=2000)
print(crn.calcul()=="45000 + 0 - 15500 - 0 = 29500")


print("*"*50, "244")
crn = rn.RevenuNet()
crn.a(revenu_net_emploi=70000, prestation_consecutive_deces=25000)
crn.fd(km_proximite_travail_etude=50, repas_par_jour=60, resiliation_bail=500, demenagement=1900, entreposage=920, jour=15, portion_deduite_ap=4000)
crn.c(pension_ex=6000)
print(crn.calcul()=="85000 + 0 - 6220 - 0 = 78780")

print("*"*50, "245")
crb = rb.RevenuBrut()
crb.rbe(salaire_brut=83000, patron_frais_representation=2700, patron_cot_reer=1500)
crb.dah(rpa=3800)
crb.calcul()
crn = rn.RevenuNet()
crb.revenu_net_emploi
crn.a(revenu_net_emploi=crb.revenu_net_emploi, prestation_consecutive_deces=15000, allocation_depart_retraite=100000, prestation_retraite=12000, psv=3025, rrq=7500)
crn.c(reer=2500, frais_opposition=300, autres=20000)
crn.calcul()

# print("*"*50, "247")
# crb = rb.RevenuBrut(est_vendeur=True)
# crb.rbe(salaire_brut=83000, commission_brute=5000)
# crb.dah(don=250)
# dahv = 5000
# rne = rbe - dah - commission_brute if dahv>commission_brute else rbe - dah - dahv
# revenu = a(revenu_net_emploi=rne, revenu_interet=2150, )
# gain_perte = 0
# gain_perte_cum = revenu + gain_perte
# deduction_ap = 0
# deduction = c(frais_demenagement=deduction_permise.frais_demenagement(km_proximite_travail_etude=0,demenagement=1200, jour=1), reer=20000+2500, frais_opposition=300, b=gain_perte_cum, psv=3025) - deduction_ap
# deduction_cum = gain_perte_cum - deduction
# perte_entreprise = 0
# total = revenu + gain_perte - deduction - perte_entreprise
# print(revenu,"+", gain_perte, "-", deduction, "-", perte_entreprise, "=", total) # 210925 + 0 - 25825 - 0 = 185100