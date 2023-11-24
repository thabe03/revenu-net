def reporter(art = None, sticker = None, reporte = 0, montant = 0, total = 0):
  if art == None:
    print("[INFO] revenu_pret.reporter() déclarer art pour l'article a|b|c|d")
    return 0
  elif sticker == None:
    print("[INFO] revenu_net.reporter() déclarer art pour l'article a|b|c|d")
    return 0

  if reporte == 1:
    reporte = "à reporter"
  elif reporte == 0:
    reporte = "non reportable"
    
  if not montant == 0 and total == 0:
    print("[INFO]", sticker, montant, reporte)
    return 0
  elif not montant == 0 and not total == 0 and montant > total:
    print("[INFO]", art, sticker, (total-montant)*-1, reporte)
    return total
  elif not montant == 0 and not total == 0 and montant < total:
    return montant
  else:
    return 0

class RevenuNet:  
  def __init__(self):
    self.revenu = 0
    self.gain_perte = 0
    self.deduction = 0
    self.perte_entreprise = 0

    self.perte_placement = 0
    self.rpa = 0
    self.beneficiaire = 0
    self.frais_demenagement = 0
    self.psv = 0
    self.revenu_net = 0

  @staticmethod
  def dd(array = []):
    if len(array) > 1:
      reste = sum(array) - array.pop(0)
      deduction_deces = [10000]
      for i in array:
        deduction_deces.append(round(1000*i/reste))
      return deduction_deces
    else:
      deduction_deces = 10000
      return deduction_deces
    
  def fd(self, km_proximite_travail_etude, repas_par_jour = 0, logement_par_jour = 0, jour = 0, resiliation_bail = 0, demenagement = 0, entreposage = 0, notaire_ph = 0, veterinaire = 0, frais_amenagement = 0, portion_deduite_ap = 0):
    if jour == 0:
      print("[ERREUR] frais_demenagement déclarer le nombre de jour")
      return 0
    elif km_proximite_travail_etude < 40:
      print("[INFO] frais_demenagement Le déménagement ne se rapproche pas de 40 km au moins du nouveau lieu de travail ou d'étude")
      return 0
    if jour > 15:
      repas_par_jour = 15*repas_par_jour
      logement_par_jour = 15*logement_par_jour
    else:
      repas_par_jour = jour*repas_par_jour
      logement_par_jour = jour*logement_par_jour
    self.frais_demenagement = (repas_par_jour + logement_par_jour + resiliation_bail + demenagement + entreposage + notaire_ph + veterinaire + frais_amenagement) - portion_deduite_ap
    return self.frais_demenagement

  def a(self, revenu_net_emploi = 0, revenu_entreprise = 0, revenu_agricole = 0, revenu_interet = 0, revenu_dividende = 0, pension_ex = 0, ferr = 0, psv = 0, rpa = 0, rrq = 0, montant_fractionne = 0, prestation_retraite = 0, allocation_depart_retraite = 0, prestation_consecutive_deces = 0, police_ass = 0, bourse_etude = 0):
    police_ass = 0
    bourse_etude = 0
    self.rpa = rpa
    self.psv = psv
    prestation_consecutive_deces = prestation_consecutive_deces-self.dd([prestation_consecutive_deces]) if prestation_consecutive_deces - self.dd([prestation_consecutive_deces]) > 0 else 0
    self.revenu = revenu_net_emploi + revenu_entreprise + revenu_agricole + revenu_interet + revenu_dividende+int(revenu_dividende*0.15) + pension_ex + ferr + self.psv + self.rpa + rrq + montant_fractionne + prestation_retraite + allocation_depart_retraite + prestation_consecutive_deces
    return self.revenu
  
  def b(self, gain_capital_imposable = 0, perte_capital_deductible = 0, perte_placement = 0):
    self.perte_placement = perte_placement
    self.gain_perte = gain_capital_imposable - (perte_capital_deductible - perte_placement)
    if self.gain_perte < 0:
      if perte_placement > 0:
        print("[INFO] revenu_net.RevenuNet.b Perte en capital", perte_capital_deductible - perte_placement-gain_capital_imposable, "à reporter")
      else:
        print("[INFO] revenu_net.RevenuNet.b Perte en capital", self.gain_perte*-1, "à reporter")
      self.gain_perte = 0
      return self.gain_perte
    else:
      return self.gain_perte 
  
  def c(self, autres = 0, pension_ex = 0, frais_exploration = 0, frais_opposition = 0, frais_demenagement = 0, montant_fractionne = 0.0, frais_proc_ass_emploi = 0, prestation_consecutive_deces = 0, reer = 0, frais_scolarite = 0, vetement = 0, prime_ass_vie_med_dent = 0, frais_prep_declaration = 0):
    if not frais_demenagement == 0:
      self.frais_demenagement = frais_demenagement
    if frais_scolarite > 0:
      print("[INFO] revenu_net.RevenuNet.c crédit d'impôt pour frais de scolarité", frais_scolarite)
      frais_scolarite = 0
    if montant_fractionne > 0:
      montant_fractionne = self.rpa * montant_fractionne
    b = self.revenu + self.gain_perte
    pension_ex = reporter("c", "Pension alimentaire de l'ex-conjoint", 0, pension_ex, b)
    frais_exploration = reporter("c", "Frais d'exploration", 1, frais_exploration, b)
    frais_opposition = reporter("c", "Frais d'opposition", 1, frais_opposition, b)
    self.frais_demenagement = reporter("c", "Frais de déménagement", 1, self.frais_demenagement, b)
    montant_fractionne = reporter("c", "Montant fractionné", 1, montant_fractionne, b)
    frais_proc_ass_emploi = reporter("c", "Frais d'appel en matière d'assurance-emploi", 1, frais_proc_ass_emploi, b)
    prestation_consecutive_deces = reporter("c", "Prestation consécutive au décès", 1, prestation_consecutive_deces, b)
    reer = reporter("c", "Contribution au REER", 1, reer, b)
    self.deduction = autres + pension_ex + frais_exploration + frais_opposition + self.frais_demenagement + montant_fractionne + frais_proc_ass_emploi + prestation_consecutive_deces + reer
    if 0.15*(b-self.deduction-77580) > 0 and not self.psv == 0:
      tmp = self.psv
      self.psv = 0.15*(b-self.deduction-77580)
      if self.psv > tmp:
          self.psv = tmp
    else:
      self.psv = 0
    self.psv = reporter("c", "Prestation de service vieillesse", 1, self.psv, b)
    self.deduction += self.psv
    return self.deduction

  def d(self, perte_entreprise = 0, perte_loyer = 0):
    c = self.revenu + self.gain_perte - self.deduction
    self.perte_entreprise = perte_entreprise + self.perte_placement + perte_loyer
    self.perte_entreprise = reporter("d", "Perte d'entreprise", 1, self.perte_entreprise, c)
    return self.perte_entreprise
  
  def calcul(self):
    calcul = self.revenu + self.gain_perte - self.deduction - self.perte_entreprise
    print(round(self.revenu),"+", round(self.gain_perte), "-", round(self.deduction), "-", round(self.perte_entreprise), "=", round(calcul))
    return f"{round(self.revenu)} + {round(self.gain_perte)} - {round(self.deduction)} - {round(self.perte_entreprise)} = {round(calcul)}"
      

