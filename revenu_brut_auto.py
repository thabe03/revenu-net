class Auto:
  def __init__(self, portion_personnelle, portion_totale):
    self.usage = 0
    self.fonction = 0
    self.portion_personnelle = portion_personnelle
    self.portion_travail = 1-portion_personnelle/portion_totale
    self.portion_totale = portion_totale
    self.deduction_frais_fonctionnement = 0
    self.deductible_amort_interet_pret = 0
    self.imposable = 0
    self.deduction = 0
    self.remb_employeur = 0
    self.deduction_travailleur_autonome = 0

  def advantage_usage(self, mois, prix):
    self.usage = 1667 * mois
    if not self.portion_travail < 0.5:
      tmp = self.usage
      self.usage = self.portion_personnelle / tmp * 0.02 * prix * mois
      return self.usage
    else:
      tmp = self.usage
      self.usage = tmp / tmp * 0.02 * prix * mois 
      return self.usage

  def advantage_fonction(self, remb_perso = 0, remb_employeur = 0, choix = 0):
      self.remb_employeur = remb_employeur
      if self.portion_travail > 0.5 and choix == 1:
        self.fonction = self.usage * 0.5 - remb_perso
        return self.fonction
      elif not self.remb_employeur == 0:
        self.fonction = self.remb_employeur * self.portion_personnelle/self.portion_totale # imposé sur la portion de l'usage personnelle des dépenses payées par l'employeur, ton employeur a payé tes dépenses personnelles donc imposé
        return self.fonction   
      else:
        self.fonction = round(self.portion_personnelle * 0.28) - remb_perso
        return self.fonction            
        
  def frais_fonctionnement(self, essence = 0, entretiens_et_reparation = 0, assurance_immatriculation = 0):
    if self.advantage_fonction == 0:
      self.deduction_frais_fonctionnement = 0
      return self.deduction_frais_fonctionnement
    self.deduction_frais_fonctionnement = self.portion_travail * (essence + entretiens_et_reparation + assurance_immatriculation)
    return self.deduction_frais_fonctionnement

  def amort_interet_pret(self, interet_mois, mois, prix, amort_prix):
    interet = 0
    if interet_mois > 300:
      interet = 300 * mois
    else:
      interet = interet_mois * mois
    amortissement = prix * amort_prix
    self.deductible_amort_interet_pret = self.portion_travail * amortissement + self.portion_travail * interet
    print("[INFO] auto.Auto.amort_interet_pret() Déduction pour l'amortissement du véhicule", round(self.portion_travail * amortissement), "et l'intérêt sur le prêt automobile", round(self.portion_travail * interet), "=", round(self.deductible_amort_interet_pret))
    return self.deductible_amort_interet_pret
  
  # https://www.canada.ca/fr/agence-revenu/services/impot/entreprises/sujets/entreprise-individuelle-societe-personnes/depenses-entreprise/depenses-relatives-vehicules-a-moteur/frais-deductibles.html
  def travailleur_autonome(self, portion, immatriculation = 0, permis = 0, essence_electricite = 0, assurances = 0, interet = [0,0], entretien_et_reparation = 0, frais_location_auto = 0):
      self.deduction_travailleur_autonome = immatriculation + permis + essence_electricite + assurances + entretien_et_reparation + frais_location_auto
      self.deduction_travailleur_autonome*= self.portion_travail
      interet = min(interet[0], interet[1]*10) # minimum entre 10$*nombre de jour où l'intérêt a été payé, intérêt payé
      self.deduction_travailleur_autonome+= interet
      return self.deduction_travailleur_autonome
  
  def calcul(self):
    self.imposable = self.usage + self.fonction
    self.deduction = self.deduction_frais_fonctionnement + self.deductible_amort_interet_pret - self.deduction_travailleur_autonome
    if not self.usage == 0:
      print("[INFO] auto.Auto.calcul() Avantage imposable pour l'usage", round(self.usage))
    if not self.fonction == 0:
      print("[INFO] auto.Auto.calcul() Avantage imposable pour les frais de fonctionnement", round(self.fonction))
    if not self.usage == 0 and not self.fonction == 0:
      print("[INFO] auto.Auto.calcul() Avantages imposables cumulés", round(self.imposable))
    if not self.deduction_frais_fonctionnement == 0:
      print("[INFO] auto.Auto.calcul() Déduction pour les frais de fonctionnement", round(self.deduction_frais_fonctionnement))
    if not self.deductible_amort_interet_pret == 0 and not self.deduction_frais_fonctionnement == 0:
      print("[INFO] auto.Auto.calcul() Déductions cumulées", round(self.deduction))
    if not self.deduction_travailleur_autonome == 0:
      print("[INFO] auto.Auto.calcul() Déductions pour travailleur autonome", round(self.deduction))
    return f"{round(self.imposable)} {round(self.deduction)}"