import revenu_brut as rb
import journal_general
def reporter(art, sticker, reporte = 0, montant = 0, total = 0):
  if reporte == 1:
    reporte = "à reporter"
  elif reporte == 0:
    reporte = "non reportable"
    
  if not montant == 0 and total == 0:
    print("[INFO]", art, sticker, round(montant), reporte)
    return 0
  elif not montant == 0 and not total == 0 and montant > total:
    print("[INFO]", art, sticker, round((total-montant)*-1), reporte)
    return total
  elif not montant == 0 and not total == 0 and montant <= total:
    return round(montant)
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
    self.imposition_federal_result = 0
    self.imposition_federal_deduit_source = self.crb.impot_fed
    self.scolarite_limite = 5000
    self.gain_capital_imposable = 0
    self.credit_transferable_result = 0
    self.credit_salaire_result = 0
    self.credit_transfere_result = 0
    self.handicap_montant = 2230
    self.deficiende_physique_limite = 8414
    self.credit_deficience_physique_result = 0
    self.credit_impot_etranger_result = 0
    self.credit_contribution_parti_federaux_result = 0
    self.revenu_location = 0
    self.revenu_location_auto = 0
    self.credit_investissement_result = 0
    self.travailleur_autonome_rqap_format = 0

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
  
  def credit_raison_age(self): # à faire
    if not self.revenu + self.gain_perte - self.deduction - self.pertes > self.raison_age_limite_sup:
      self.credit_raison_age_result = (self.raison_age_montant_maximal - ((self.revenu + self.gain_perte - self.deduction - self.pertes - self.raison_age_limite_inf)*0.15))*0.15
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
  
  def credit_transferable(self): # à faire
    self.imposition_revenu()
    self.credits()
    self.imposition_federal()
    self.credit_transferable_result = self.credit_scolarite_result - (self.imposition_revenu_result - (self.credit_personnel_base_result+self.credit_salaire_result+self.credit_cad_emploi_result+self.credit_deficience_physique_result+self.credit_frais_medicaux_result))
    print(f"[INFO] credit_transferable {round(self.credit_transferable_result)}")
    return self.credit_transferable_result
  
  def credit_transfere(self, montant_credit_transfere):
    self.credit_transfere_result += montant_credit_transfere
    print(f"[INFO] credit_transfere {round(montant_credit_transfere)}")
    return self.credit_transfere_result
  
  def credit_frais_medicaux(self, montant_frais_medicaux, remb_ass = 0): # à faire
    tmp = (montant_frais_medicaux + self.crb.ass_maladie_prive - remb_ass - (0.03*(self.revenu + self.gain_perte - self.deduction - self.pertes) if 0.03*(self.revenu + self.gain_perte - self.deduction - self.pertes) < self.frais_medicaux_limite else self.frais_medicaux_limite))*0.15
    self.credit_frais_medicaux_result = tmp if not tmp < 0 else 0
    print(f"[INFO] credit_frais_medicaux {round(self.credit_frais_medicaux_result)}")
    return self.credit_frais_medicaux_result

  
  def credit_don(self, montant_don = 0): # à faire
    if not montant_don == 0:
      self.revenu_entreprise_don = montant_don
    if not self.revenu_entreprise_don < 200:
      self.credit_don_result = (self.don_montant_premier * self.don_taux_premier) + ((self.revenu_entreprise_don - self.don_montant_premier)*self.don_taux_reste)
    else:
      self.credit_don_result = self.revenu_entreprise_don * self.don_taux_premier
    print(f"[INFO] credit_don {round(self.credit_don_result)}")
    return self.credit_don_result
  
  def credit_dividende_determine(self):
    self.credit_dividende_determine_result = ((self.revenu_dividende_determine+int(self.revenu_dividende_determine*0.38))-self.revenu_dividende_determine)*self.dividende_determine_majoration
    print(f"[INFO] credit_dividende_determine {round(self.credit_dividende_determine_result)}")
    return self.credit_dividende_determine_result
  
  def imposition_revenu(self):
    if self.calcul_result < self.imposition_revenu_pallier_un:
      tmp_un = self.calcul_result * self.imposition_revenu_pallier_un_taux
      tmp_result = tmp_un
    elif self.calcul_result < self.imposition_revenu_pallier_deux:
      tmp_un = self.imposition_revenu_pallier_un * self.imposition_revenu_pallier_un_taux
      tmp_deux = (self.calcul_result - self.imposition_revenu_pallier_un)*self.imposition_revenu_pallier_deux_taux
      tmp_result = tmp_un + tmp_deux
    elif self.calcul_result < self.imposition_revenu_pallier_trois:
      tmp_un = self.imposition_revenu_pallier_un * self.imposition_revenu_pallier_un_taux
      tmp_deux = (self.imposition_revenu_pallier_deux - self.imposition_revenu_pallier_un)*self.imposition_revenu_pallier_deux_taux
      tmp_trois = (self.calcul_result - self.imposition_revenu_pallier_deux)*self.imposition_revenu_pallier_trois_taux
      tmp_result = tmp_un + tmp_deux + tmp_trois
    elif self.calcul_result < self.imposition_revenu_pallier_quatre:
      tmp_un = self.imposition_revenu_pallier_un * self.imposition_revenu_pallier_un_taux
      tmp_deux = (self.imposition_revenu_pallier_deux - self.imposition_revenu_pallier_un)*self.imposition_revenu_pallier_deux_taux
      tmp_trois = (self.imposition_revenu_pallier_trois - self.imposition_revenu_pallier_deux)*self.imposition_revenu_pallier_trois_taux
      tmp_quatre = (self.calcul_result - self.imposition_revenu_pallier_trois)*self.imposition_revenu_pallier_quatre_taux
      tmp_result = tmp_un + tmp_deux + tmp_trois + tmp_quatre
    else:
      tmp_un = self.imposition_revenu_pallier_un * self.imposition_revenu_pallier_un_taux
      tmp_deux = (self.imposition_revenu_pallier_deux - self.imposition_revenu_pallier_un)*self.imposition_revenu_pallier_deux_taux
      tmp_trois = (self.imposition_revenu_pallier_trois - self.imposition_revenu_pallier_deux)*self.imposition_revenu_pallier_trois_taux
      tmp_quatre = (self.imposition_revenu_pallier_quatre - self.imposition_revenu_pallier_trois)*self.imposition_revenu_pallier_quatre_taux
      tmp_cinq = (self.calcul_result - self.imposition_revenu_pallier_quatre)*self.imposition_revenu_pallier_cinq_taux
      tmp_result = tmp_un + tmp_deux + tmp_trois + tmp_quatre + tmp_cinq
    self.imposition_revenu_result = tmp_result
    print(f"[INFO] imposition_revenu {round(self.imposition_revenu_result)}")
    return self.imposition_revenu_result
  
  def credit_personne_charge(self, montant_personne_charge = 0, handicap = False):
    if not handicap == True:
      self.credit_personne_charge_result = (self.montant_personnel_base - montant_personne_charge)*0.15
    else:
      self.credit_personne_charge_result = (self.montant_personnel_base + self.handicap_montant - montant_personne_charge)*0.15
    print(f"[INFO] credit_personne_charge {round(self.credit_personne_charge_result)}")
    return self.credit_personne_charge_result
  
  def imposition_base(self):
    self.imposition_base_result = self.imposition_revenu_result - self.credits_result
    print(f"[INFO] imposition_base {round(self.imposition_base_result)}")
    return self.imposition_base_result
  
  def credit_cad_emploi(self):
    self.credit_cad_emploi_result = min(self.cad_emploi_limite, self.calcul_result)*0.15
    print(f"[INFO] credit_cad_emploi {round(self.credit_cad_emploi_result)}")
    return self.credit_cad_emploi_result
  
  def credit_deficience_physique(self):
    self.credit_deficience_physique_result = self.deficiende_physique_limite*0.15
    print(f"[INFO] credit_deficience_physique {round(self.credit_deficience_physique_result)}")
    return self.credit_deficience_physique_result
  
  def credit_abattement(self):
    self.credit_abattement_result = self.imposition_base_result * self.abattement_taux
    print(f"[INFO] credit_abattement {round(self.credit_abattement_result)}")
    return self.credit_abattement_result
  
  def credit_contribution_parti_federaux(self, montant_contribution_parti_federaux):
    self.credit_contribution_parti_federaux_result = montant_contribution_parti_federaux*0.75
    print(f"[INFO] credit_contribution_parti_federaux {round(self.credit_contribution_parti_federaux_result)}")
    return self.credit_contribution_parti_federaux_result
  
  def credit_impot_etranger(self, montant_impot_etranger):
    self.credit_impot_etranger_result = (montant_impot_etranger*100/15)/(self.revenu + self.gain_perte - self.deduction - self.pertes)*(self.imposition_base_result+self.credit_dividende_determine_result-self.credit_abattement_result)
    print(f"[INFO] credit_impot_etranger {round(self.credit_impot_etranger_result)}")
    return self.credit_impot_etranger_result
  
  def credit_investissement(self, montant_investissement = [0,0]):
    self.credit_investissement_result = montant_investissement[0]*montant_investissement[1] # coût * crédit ex 0.1
    print(f"[INFO] credit_investissement {round(self.credit_investissement_result)}")
    return self.credit_investissement_result
  
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-21300-remboursement-prestation-universelle-garde-enfants-puge.html">21300 remboursement de la prestation universelle pour la garde d'enfants, <a href="https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-21400-frais-garde-enfants.html">21400 Frais de garde d'enfants
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-22100-frais-financiers-frais-interet.html"> 22100 honoraires versés à un conseiller en placements
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-22900-autres-depenses-emploi.html">22900 dépense en télétravail
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-25600-deductions-supplementaires.html">25600 revenu étranger
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-31270-montant-achat-habitation.html
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-31300-frais-adoption.html
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-31900-interets-payes-vos-prets-etudiants.html
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-32300-vos-frais-scolarite-montant-relatif-etudes-montant-manuels.html">32300 vos frais de scolarité, montant relatif aux études et montant pour manuels
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-34900-dons.html">34900 dons
  # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-40500-credit-federal-impot-etranger.html">40500 crédit fédéral pour impôt étranger
    
  def imposition_federal(self, montant_allocation_depart_retraite = 0, acompte_provisionnel = 0):
    self.imposition_federal_deduit_source += montant_allocation_depart_retraite
    self.imposition_federal_result = self.imposition_base_result - self.credit_abattement_result
    impot = 0
    message = f"[INFO] imposition_federal {round(self.imposition_federal_result)}"
    if not self.credit_impot_etranger_result == 0:
      self.imposition_federal_result -= self.credit_impot_etranger_result
      message += f" - crédit d'impôt étranger {round(self.credit_impot_etranger_result)}"
    if not acompte_provisionnel == 0:
      self.imposition_federal_result -= acompte_provisionnel
      message += f" - acompte provisionnel {round(acompte_provisionnel)}"
    if not self.credit_contribution_parti_federaux_result == 0:
      self.imposition_federal_result -= self.credit_contribution_parti_federaux_result
      message += f" - crédit pour contribution à un parti fédéral {round(self.credit_contribution_parti_federaux_result)}"
    message += f" = impôt fédéral {round(self.imposition_federal_result)}\nimpôt fédéral {round(self.imposition_federal_result)} - impôt fédéral déduit à la source {round(self.imposition_federal_deduit_source)}"
    if self.imposition_federal_result < self.imposition_federal_deduit_source:
      impot = (self.imposition_federal_result - self.imposition_federal_deduit_source)*-1
      self.credit_investissement_result = reporter("imposition_federal", "Crédit d'impot à l'investissement", 1, self.credit_investissement_result, impot)
      message += f" = impôt fédéral à recevoir {round(impot)}"
    elif self.imposition_federal_result > self.imposition_federal_deduit_source:
      impot = self.imposition_federal_result - self.imposition_federal_deduit_source
      print(f"[INFO] imposition_federal 40% du CII est remboursable {round((impot - self.credit_investissement_result)*0.4*-1)} et 60% reportable {round((impot - self.credit_investissement_result)*0.6*-1)}")
      self.credit_investissement_result = reporter("imposition_federal", "Crédit d'impot à l'investissement", 1, self.credit_investissement_result, impot)
      if not self.credit_investissement_result == 0:
        message += f" - crédit d'impôt à l'investissement {round(self.credit_investissement_result)}"
      impot-= self.credit_investissement_result
      message += f" = impôt fédéral à payer {round(impot)}"
      
    print(message)
    return impot
  
  def credits(self, credit_salaire_result = 0, message_credits = True):
    self.credit_salaire_result = credit_salaire_result
    if not self.crb.credit_salaire_result == 0:
      self.credit_salaire_result = self.crb.credit_salaire_result
    array = [self.credit_pension_result, self.credit_conjoint_result, self.credit_raison_age_result, self.credit_personnel_base_result, self.credit_scolarite_result, self.credit_frais_medicaux_result, self.credit_don_result, self.credit_dividende_determine_result, self.credit_personne_charge_result, self.credit_salaire_result, self.credit_cad_emploi_result, self.credit_transfere_result, self.credit_deficience_physique_result]
    message = ""
    credits = 0
    for i in range(len(array)):
      credits += array[i]
      if not array[i] == 0:
        message += f"{round(array[i])} + "
    self.credits_result = credits
    message = message[:-3]
    if message_credits:
      print(f"[INFO] credits {message} = {round(self.credits_result)}")
    return message
  
  def calcul_credits(self, montant_allocation_depart_retraite = 0, acompte_provisionnel = 0):
    message = ""
    message += f"{round(self.imposition_revenu())}"
    self.credits(message_credits=False)
    message += f" {round(self.imposition_base())} {round(self.credit_abattement())} {round(self.imposition_federal(montant_allocation_depart_retraite = montant_allocation_depart_retraite, acompte_provisionnel = acompte_provisionnel))}"
    return message
  
  def rl_auto(self, immatriculation = 0, permis = 0, essence_electricite = 0, assurances = 0, interet = [0,0], entretien_et_reparation = 0, frais_location_auto = 0):
    self.revenu_location_auto = immatriculation + permis + essence_electricite + assurances + entretien_et_reparation + frais_location_auto
    interet = min(interet[0], interet[1]*10) # minimum entre 10$*nombre de jour où l'intérêt a été payé, intérêt payé
    self.revenu_location_auto+= interet
    return self.revenu_location_auto
  
  # https://www.canada.ca/fr/agence-revenu/services/impot/entreprises/sujets/revenus-location/remplir-formulaire-t776-etat-loyers-biens-immeubles/depenses-vous-pouvez-deduire.html
  def rl(self, taxes_foncieres = 0, interets_sur_hypotheque = 0, entretien_et_reparation = 0, assurances = 0, fnacc = [0,0], revenu_location = 0, publicite = 0, frais_bureau = 0, honoraire_professionnel = 0, salaire_verse = 0, frais_deplacement = 0, chauffage = 0, electricite = 0):
    self.revenu_location = taxes_foncieres + interets_sur_hypotheque + entretien_et_reparation + assurances +  publicite + frais_bureau + honoraire_professionnel + salaire_verse + frais_deplacement + chauffage + electricite + self.revenu_location_auto
    deduction_pour_amortissement = fnacc[0]*fnacc[1]
    deduction_pour_amortissement = reporter("revenu_location", "Déduction pour amortissement", 0, deduction_pour_amortissement, revenu_location - self.revenu_location)
    self.revenu_location+= deduction_pour_amortissement
    self.revenu_location-=revenu_location
    return self.revenu_location

  def a(self, revenu_net_emploi = 0, revenu_entreprise = 0, revenu_agricole = 0, revenu_interet = [0,0], revenu_dividende_ordinaire = 0, revenu_dividende_determine = 0, pension_ex = 0, ferr = 0, psv = 0, rpa = 0, rrq = 0, prestation_retraite = 0, allocation_depart_retraite = 0, prestation_consecutive_deces = 0, police_ass = 0, bourse_etude = 0, revenu_location = 0, reer = [0,0], indeminite_accident = 0, revenu_dividende_etranger = 0, moins_conseiller = 0, revenu_entreprise_don = 0):
    police_ass = 0
    bourse_etude = 0
    self.rpa = rpa
    self.psv = psv
    self.revenu_agricole = revenu_agricole
    self.indeminite_accident = indeminite_accident
    self.revenu_retraite = rpa
    self.revenu_dividende_determine = revenu_dividende_determine
    self.revenu_entreprise_don = revenu_entreprise_don
    if not self.crb.revenu_net_emploi == 0:
      revenu_net_emploi = self.crb.revenu_net_emploi
    if not revenu_location == 0:
      self.revenu_location = revenu_location
    prestation_consecutive_deces = prestation_consecutive_deces-self.dd([prestation_consecutive_deces]) if prestation_consecutive_deces - self.dd([prestation_consecutive_deces]) > 0 else 0
    self.revenu = revenu_net_emploi + revenu_entreprise + self.revenu_entreprise_don + self.revenu_agricole + revenu_interet[0]-revenu_interet[1] + revenu_dividende_ordinaire+int(revenu_dividende_ordinaire*0.15) + revenu_dividende_determine+int(revenu_dividende_determine*0.38) + pension_ex + ferr + self.psv + self.rpa + rrq + prestation_retraite + allocation_depart_retraite + prestation_consecutive_deces + self.revenu_location + reer[0]+reer[1] + self.indeminite_accident + revenu_dividende_etranger*100/85 - moins_conseiller
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
  
  def c(self, autres = 0, pension_ex = 0, frais_exploration = 0, frais_opposition = 0, frais_demenagement = 0, montant_fractionne = 0.0, frais_proc_ass_emploi = 0, reer = 0):
    if not frais_demenagement == 0:
      self.frais_demenagement = frais_demenagement
    if montant_fractionne > 0:
      montant_fractionne = self.rpa * montant_fractionne
    b = self.revenu + self.gain_perte
    pension_ex = reporter("c", "Pension alimentaire de l'ex-conjoint", 0, pension_ex, b)
    frais_exploration = reporter("c", "Frais d'exploration", 1, frais_exploration, b)
    frais_opposition = reporter("c", "Frais d'opposition", 1, frais_opposition, b)
    self.frais_demenagement = reporter("c", "Frais de déménagement", 1, self.frais_demenagement, b)
    montant_fractionne = reporter("c", "Montant fractionné", 1, montant_fractionne, b)
    frais_proc_ass_emploi = reporter("c", "Frais d'appel en matière d'assurance-emploi", 1, frais_proc_ass_emploi, b)
    reer = reporter("c", "Contribution au REER", 1, reer, b)
    self.crb.travailleur_autonome_rrq /=2
    self.crb.travailleur_autonome_rrq = reporter("c", "Contribution au RRQ - travailleur autonome", 1, self.crb.travailleur_autonome_rrq, b)
    self.travailleur_autonome_rqap_format = self.crb.travailleur_autonome_rqap[0]-self.crb.travailleur_autonome_rqap[1]
    self.travailleur_autonome_rqap_format = reporter("c", "Contribution au RQAP - travailleur autonome", 1, self.travailleur_autonome_rqap_format, b)
    self.deduction = autres + pension_ex + frais_exploration + frais_opposition + self.frais_demenagement + montant_fractionne + frais_proc_ass_emploi + reer + self.crb.travailleur_autonome_rrq + self.travailleur_autonome_rqap_format
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
    message += f"= {round(calcul)}"
    print(message_reporte+message)    
    self.calcul_result = calcul
    return message
      

