import revenu_brut as rb
def reporter(art, sticker, reporte = 0, montant = 0, total = 0):
  if reporte == 1:
    reporte = "à reporter"
  elif reporte == 0:
    reporte = "non reportable"
    
  if not montant == 0 and total == 0:
    print("[INFO]", art, sticker, montant, reporte)
    return 0
  elif not montant == 0 and not total == 0 and montant > total:
    print("[INFO]", art, sticker, (total-montant)*-1, reporte)
    return total
  elif not montant == 0 and not total == 0 and montant <= total:
    return montant
  else:
    return 0

class RevenuNet:  
  def __init__(self, crb = rb.RevenuBrut()):
    self.revenu = 0
    self.gain_perte = 0
    self.deduction = 0
    self.perte_autre = 0
    self.perte_placement = 0
    self.pertes = 0
    self.rpa = 0
    self.beneficiaire = 0
    self.frais_demenagement = 0
    self.psv = 0
    self.revenu_agricole = 0
    self.perte_agricole = 0
    self.perte_agricole_restreinte = 0
    self.perte_capital = 0
    self.revenu_retraite = 0
    self.montant_personnel_base = 12069
    self.raison_age_limite_inf = 37790
    self.raison_age_limite_sup = 87750
    self.raison_age_montant_maximal = 7494
    self.credit_pension_result = 0
    self.credit_conjoint_result = 0
    self.credit_raison_age_result = 0
    self.credit_personnel_base_result = 0
    self.credit_scolarite_result = 0
    self.credit_frais_medicaux_result = 0
    self.credit_don_result = 0
    self.credit_dividende_determine_result = 0
    self.revenu_dividende_determine = 0
    self.frais_medicaux_limite = 2352
    self.don_taux_premier = 0.15
    self.don_taux_reste = 0.29
    self.don_montant_premier = 200
    self.dividende_determine_majoration = 6/11
    self.imposition_revenu_pallier_un = 47630
    self.imposition_revenu_pallier_deux = 95259
    self.imposition_revenu_pallier_trois = 147667
    self.imposition_revenu_pallier_quatre = 210371
    self.imposition_revenu_pallier_un_taux = 0.15
    self.imposition_revenu_pallier_deux_taux = 0.205
    self.imposition_revenu_pallier_trois_taux = 0.26
    self.imposition_revenu_pallier_quatre_taux = 0.29
    self.imposition_revenu_pallier_cinq_taux = 0.33
    self.imposition_revenu_result = 0
    self.calcul_result = 0
    self.credit_personne_charge_result = 0
    self.credit_cad_emploi_result = 0
    self.cad_emploi_limite = 1222
    self.crb = crb
    self.imposition_base_result = 0
    self.credits_result = 0
    self.abattement_taux = 0.165
    self.credit_abattement_result = 0
    self.imposition_federale_result = 0
    self.imposition_federale_deduit_source = self.crb.impot_fed
    self.scolarite_limite = 5000
    self.gain_capital_imposable = 0

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
    
  def fd(self, km_proximite_travail_etude, repas_par_jour = 0, logement_par_jour = 0, jour = 0, resiliation_bail = 0, demenagement = 0, entreposage = 0, notaire_pa = 0, veterinaire = 0, frais_amenagement = 0, portion_deduite_ap = 0):
    if jour == 0:
      print("[ERREUR] fd déclarer le nombre de jour")
      return 0
    elif km_proximite_travail_etude < 40:
      print("[INFO] fd Le déménagement ne se rapproche pas de 40 km au moins du nouveau lieu de travail ou d'étude")
      return 0
    if jour > 15:
      repas_par_jour = 15*repas_par_jour
      logement_par_jour = 15*logement_par_jour
    else:
      repas_par_jour = jour*repas_par_jour
      logement_par_jour = jour*logement_par_jour
    self.frais_demenagement = (repas_par_jour + logement_par_jour + resiliation_bail + demenagement + entreposage + notaire_pa + veterinaire + frais_amenagement) - portion_deduite_ap
    return self.frais_demenagement
  
  def credit_pension(self):   
    self.credit_pension_result = min(self.revenu_retraite, 2000)*0.15
    print(f"[INFO] credit_pension {round(self.credit_pension_result)}")
    return self.credit_pension_result
  
  def credit_conjoint(self, epoux):
    self.credit_conjoint_result = (self.montant_personnel_base - epoux)*0.15
    print(f"[INFO] credit_conjoint {round(self.credit_conjoint_result)}")
    return self.credit_conjoint_result
  
  def credit_raison_age(self):
    self.credit_raison_age_result = (self.raison_age_montant_maximal - ((self.revenu + self.gain_perte - self.raison_age_limite_inf)*0.15))*0.15
    print(f"[INFO] credit_raison_age {round(self.credit_raison_age_result)}")
    return self.credit_raison_age_result

  def credit_personnel_base(self):
    self.credit_personnel_base_result = self.montant_personnel_base*0.15
    print(f"[INFO] credit_personnel_base {round(self.credit_personnel_base_result)}")
    return self.credit_personnel_base_result
  
  def credit_scolarite(self, montant_scolarite):
    self.credit_scolarite_result = min((montant_scolarite*0.15), self.scolarite_limite*0.15)
    print(f"[INFO] credit_scolarite {round(self.credit_scolarite_result)}")
    return self.credit_scolarite_result
  
  def credit_frais_medicaux(self, montant_frais_medicaux, remb_ass = 0):
    self.credit_frais_medicaux_result = (montant_frais_medicaux - remb_ass - (0.03*(self.revenu + self.gain_perte) if 0.03*(self.revenu + self.gain_perte) < self.frais_medicaux_limite else self.frais_medicaux_limite))*0.15
    print(f"[INFO] credit_frais_medicaux {round(self.credit_frais_medicaux_result)}")
    return self.credit_frais_medicaux_result
  
  def credit_don(self, montant_don):
    if not montant_don < 200:
      self.credit_don_result = (self.don_montant_premier * self.don_taux_premier) + ((montant_don - self.don_montant_premier)*self.don_taux_reste)
    else:
      self.credit_don_result = montant_don * self.don_taux_premier
    print(f"[INFO] credit_don {round(self.credit_don_result)}")
    return self.credit_don_result
  
  def credit_dividende_determine(self):
    self.credit_dividende_determine_result = ((self.revenu_dividende_determine+int(self.revenu_dividende_determine*0.38))-self.revenu_dividende_determine)*self.dividende_determine_majoration
    print(f"[INFO] credit_dividende_determine {round(self.credit_dividende_determine_result)}")
    return self.credit_dividende_determine_result
  
  def imposition_revenu(self):
    if self.calcul_result < self.imposition_revenu_pallier_un:
      self.imposition_revenu_result = self.calcul_result * self.imposition_revenu_pallier_un_taux
    elif self.calcul_result < self.imposition_revenu_pallier_deux:
      self.imposition_revenu_result = (self.imposition_revenu_pallier_un * self.imposition_revenu_pallier_un_taux) + ((self.calcul_result-self.imposition_revenu_pallier_un)*self.imposition_revenu_pallier_deux_taux)
    print(f"[INFO] imposition_revenu {round(self.imposition_revenu_result)}")
    return self.imposition_revenu_result
  
  def imposition_base(self):
    self.imposition_base_result = self.imposition_revenu_result - self.credits_result
    print(f"[INFO] imposition_base {round(self.imposition_base_result)}")
    return self.imposition_base_result
  
  def credit_personne_charge(self, montant_personne_charge):
    self.credit_personne_charge_result = (self.montant_personnel_base - montant_personne_charge)*0.15
    print(f"[INFO] credit_personne_charge {round(self.credit_personne_charge_result)}")
    return self.credit_personne_charge_result
  
  def credit_cad_emploi(self):
    self.credit_cad_emploi_result = min(self.cad_emploi_limite, self.calcul_result)*0.15
    print(f"[INFO] credit_cad_emploi {round(self.credit_cad_emploi_result)}")
    return self.credit_cad_emploi_result
  
  def credit_abattement(self):
    self.credit_abattement_result = self.imposition_base_result * self.abattement_taux
    print(f"[INFO] credit_abattement {round(self.credit_abattement_result)}")
    return self.credit_abattement_result
  
  def imposition_federale(self):
    self.imposition_federale_result = self.imposition_base_result - self.credit_abattement_result
    impot = 0
    message = ""
    if self.imposition_federale_result < self.imposition_federale_deduit_source:
      impot = (self.imposition_federale_result - self.imposition_federale_deduit_source)*-1
      message = f"[INFO] imposition_federale Impôt fédérale à recevoir {round(impot)}"
    elif self.imposition_federale_result > self.imposition_federale_deduit_source:
      impot = self.imposition_federale_result - self.imposition_federale_deduit_source
      message = f"[INFO] imposition_federale Impôt fédérale à payer {round(impot)}"
    print(message)
    return impot  
  
  def credits(self, credit_salaire_result = 0):
    if not self.crb.credit_salaire_result == 0:
      credit_salaire_result = self.crb.credit_salaire_result
    array = [self.credit_pension_result, self.credit_conjoint_result, self.credit_raison_age_result, self.credit_personnel_base_result, self.credit_scolarite_result, self.credit_frais_medicaux_result, self.credit_don_result, self.credit_dividende_determine_result, self.credit_personne_charge_result, credit_salaire_result, self.credit_cad_emploi_result]
    message = ""
    credits = 0
    for i in range(len(array)):
      credits += array[i]
      if not array[i] == 0:
        message += f"{round(array[i])} + "
    self.credits_result = credits
    message = message[:-3]
    print(f"[INFO] credits {message} = {round(credits)}")
    return message

  def a(self, revenu_net_emploi = 0, revenu_entreprise = 0, revenu_agricole = 0, revenu_interet = [0,0], revenu_dividende_ordinaire = 0, revenu_dividende_determine = 0, pension_ex = 0, ferr = 0, psv = 0, rpa = 0, rrq = 0, prestation_retraite = 0, allocation_depart_retraite = 0, prestation_consecutive_deces = 0, police_ass = 0, bourse_etude = 0, revenu_location = 0, reer = [0,0], indeminite_accident = 0, revenu_dividende_etranger = 0, moins_conseiller = 0, revenu_retraite = 0):
    police_ass = 0
    bourse_etude = 0
    self.rpa = rpa
    self.psv = psv
    self.revenu_agricole = revenu_agricole
    self.indeminite_accident = indeminite_accident
    self.revenu_retraite = revenu_retraite
    self.revenu_dividende_determine = revenu_dividende_determine
    if not self.crb.revenu_net_emploi == 0:
      revenu_net_emploi = self.crb.revenu_net_emploi
    prestation_consecutive_deces = prestation_consecutive_deces-self.dd([prestation_consecutive_deces]) if prestation_consecutive_deces - self.dd([prestation_consecutive_deces]) > 0 else 0
    self.revenu = revenu_net_emploi + revenu_entreprise + self.revenu_agricole + revenu_interet[0]-revenu_interet[1] + revenu_dividende_ordinaire+int(revenu_dividende_ordinaire*0.15) + revenu_dividende_determine+int(revenu_dividende_determine*0.38) + pension_ex + ferr + self.psv + self.rpa + rrq + prestation_retraite + allocation_depart_retraite + prestation_consecutive_deces + revenu_location + reer[0]+reer[1] + self.indeminite_accident + revenu_dividende_etranger*100/85 - moins_conseiller + self.revenu_retraite
    return self.revenu
  
  def b(self, gain_capital_imposable = 0, perte_capital_deductible = 0, perte_placement = 0):
    gain_capital_imposable = gain_capital_imposable*0.5
    perte_capital_deductible = perte_capital_deductible*0.5
    self.gain__capital_imposable = gain_capital_imposable
    self.perte_placement = perte_placement*0.5
    self.gain_perte = gain_capital_imposable - (perte_capital_deductible - self.perte_placement)
    if self.gain_perte < 0:
      self.perte_capital = reporter("b", "Perte en capital", 1, perte_capital_deductible, gain_capital_imposable + self.perte_placement)
      self.gain_perte = 0
      return self.gain_perte
    else:
      return self.gain_perte 
  
  def c(self, autres = 0, pension_ex = 0, frais_exploration = 0, frais_opposition = 0, frais_demenagement = 0, montant_fractionne = 0.0, frais_proc_ass_emploi = 0, prestation_consecutive_deces = 0, reer = 0, frais_scolarite = 0, prime_ass_vie_med_dent = 0):
    if not frais_demenagement == 0:
      self.frais_demenagement = frais_demenagement
    if frais_scolarite > 0:
      print("[INFO] c crédit d'impôt pour frais de scolarité", frais_scolarite)
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

  def d(self, perte_entreprise = 0, perte_loyer = 0, perte_agricole = 0, perte_agricole_principale = 0):
    c = self.revenu + self.gain_perte - self.deduction    
    self.perte_autre = perte_entreprise + self.perte_placement + perte_loyer + self.indeminite_accident
    self.perte_autre = reporter("d", "Perte autre qu'en capital", 1, self.perte_autre, c)
    if perte_agricole_principale == 0 and not perte_agricole == 0:
      self.perte_agricole = perte_agricole - (2500 + (0.5*(perte_agricole-2500)))
      print(f"[INFO] d Perte agricole restreinte {self.perte_agricole} à reporter")
    elif not perte_agricole_principale == 0 and not perte_agricole == 0:
      self.perte_agricole = reporter("d", "Perte agricole", 1, perte_agricole, self.revenu_agricole)
    self.pertes = self.perte_autre + (round(2500 + (0.5*(perte_agricole-2500))) if not perte_agricole == 0 else 0)
    return self.pertes
  
  def calcul(self, ap = 0, ap_agricole = 0, ap_autre = 0, ap_capital = 0):
    self.pertes = reporter("calcul", "Pertes", 1, self.pertes, self.revenu + self.gain_perte - self.deduction)
    message = f"{round(self.revenu)} + {round(self.gain_perte)} - {round(self.deduction)} - {round(self.pertes)} "
    message_reporte = ""
    calcul = self.revenu + self.gain_perte - self.deduction - self.pertes
    if not ap == 0:
      reporte = 0 if calcul - ap > 0 else calcul - ap
      if not reporte == 0:
        message_reporte += f"[INFO] calcul AP {round(reporte)*-1} à reporter\n"
      calcul -= (ap + reporte)
      message += f"- {round(ap+reporte)} "
    if not ap_agricole == 0:
      reporte = 0 if self.revenu_agricole - ap_agricole > 0 else self.revenu_agricole - ap_agricole
      calcul -= (ap_agricole + reporte)
      if not reporte == 0:
        message_reporte += f"[INFO] calcul AP Perte agricole {round(reporte)*-1} à reporter\n"
      message += f"- {round(ap_agricole+reporte)} "
    if not ap_autre == 0:
      reporte = 0 if calcul - ap_autre > 0 else calcul - ap_autre
      if not reporte == 0:
        message_reporte += f"[INFO] calcul AP Perte autre qu'en capital {round(reporte)*-1} à reporter\n"
      calcul -= (ap_autre + reporte)
      message += f"- {round(ap_autre+reporte)} "
    if not ap_capital == 0:
      if (ap_capital - self.gain_capital_imposable) > calcul:
        reporte = ap_capital - calcul
      else:
        reporte = 0
      if not reporte == 0:
        message_reporte += f"[INFO] calcul AP Perte en capital {round(reporte)} à reporter\n"
      message += f"- {round(calcul if (ap_capital - self.gain_capital_imposable) > calcul else min(self.gain_perte, ap_capital))} "
      calcul -= calcul if (ap_capital - self.gain_capital_imposable) > calcul else min(self.gain_perte, ap_capital)
    message+= f"= {round(calcul)}"
    print(message_reporte+message)
    self.calcul_result = calcul
    return message
      

