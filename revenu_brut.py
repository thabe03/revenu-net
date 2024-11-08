import revenu_brut_auto as auto
class RevenuBrut:
    def __init__(self, est_vendeur=False, est_entrepreneur=False, cauto=auto.Auto(1,1), frais_repas=0, hebergement=0, frais_representation=0, frais_stationnement=0, membre_commerce=0, cout_ordinateur=0):
        self.revenu_brut_emploi = 0
        self.deduction_auto = 0
        self.deduction_article_huit = 0
        self.deduction_article_huit_vendeur = 0
        self.commission_brute = 0
        self.salaire_brut = 0
        self.bureau = 0
        self.advantage_action = 0
        self.cauto = cauto
        self.est_vendeur = est_vendeur
        self.frais_repas = frais_repas
        self.hebergement = hebergement
        self.frais_representation = frais_representation
        self.frais_stationnement = frais_stationnement
        self.membre_commerce = membre_commerce
        self.patron_frais_deplacement = 0
        self.revenu_net_emploi = 0
        self.rpa = 0
        self.rrq = 0
        self.ass_emploi = 0
        self.ass_parentale = 0
        self.credit_salaire_result = 0
        self.ass_maladie_prive = 0
        self.impot_fed = 0
        self.cot_syndic = 0
        self.deduction_travailleur_autonome = 0
        self.travailleur_autonome_rrq = 0
        self.travailleur_autonome_rqap = [0,0]

    def bure(self, fourn_cons = 0, loyer_bureau = 0, mois = 0, salaire_adjoint = 0):
        self.bureau = fourn_cons + loyer_bureau * mois + salaire_adjoint
        return self.bureau
    
    def action(self, *args, vente = 0, prix_vente = 0, deduction_employe = False):
        # [valeur, valeur_reduit, nb_action]
        nb_actions = 0
        for i in args:
            nb_actions += i[2]
        if vente > nb_actions:
            print("[ERREUR] action le nombre d'actions vendues ne peut pas être plus grand que le nombre d'actions détenues", vente, nb_actions)
            return 0
        advantage_imposable = 0
        prix_payes = 0
        for i in args:
            advantage_imposable += (i[0] - i[1])*i[2]
            prix_payes += i[1] * i[2]
        if vente == 0 and prix_vente == 0 and deduction_employe == True:
            self.advantage_action = advantage_imposable * 0.5
            return self.advantage_action
        elif vente == 0 and prix_vente == 0 and deduction_employe == False:
            self.advantage_action = advantage_imposable
            return self.advantage_action
        if deduction_employe == True:
            gain_cap_impos = vente*prix_vente - prix_payes - advantage_imposable
            self.advantage_action = advantage_imposable + gain_cap_impos * 0.5
            return self.advantage_action
        elif deduction_employe == False:
            gain_cap_impos = vente*prix_vente - prix_payes - advantage_imposable
            self.advantage_action = advantage_imposable + gain_cap_impos
            return self.advantage_action
    
    def sb(self, salaire_net = 0, impot_fed = 0, impot_prov = 0, rrq = 0, ass_emploi = 0, ass_parentale = 0, rpa = 0, cot_syndic = 0, ass_collectif = 0, ass_maladie_prive = 0, travailleur_autonome_rrq = 0, travailleur_autonome_rqap=[0,0]):
        self.rpa = rpa
        self.rrq = rrq if not rrq == 0 else travailleur_autonome_rrq/2
        self.cot_syndic = cot_syndic
        self.ass_emploi = ass_emploi
        self.ass_parentale = ass_parentale if not ass_parentale == 0 else travailleur_autonome_rqap[1]
        self.travailleur_autonome_rrq = travailleur_autonome_rrq
        self.travailleur_autonome_rqap = travailleur_autonome_rqap
        self.ass_maladie_prive = ass_maladie_prive
        self.impot_fed = impot_fed
        self.salaire_brut = salaire_net + impot_fed + impot_prov + rrq + ass_emploi + ass_parentale + rpa + self.cot_syndic + ass_collectif + ass_maladie_prive
        return self.salaire_brut
    
    def credit_salaire(self):
        self.credit_salaire_result = self.rrq*0.15 + self.ass_emploi*0.15 + self.ass_parentale*0.15
        print(f"[INFO] credits_salaire {round(self.credit_salaire_result)}")
        return self.credit_salaire_result

    def rbe(self, salaire_brut = 0, commission_brute = 0, patron_voyage_perso = 0, patron_frais_scol_perso = 0, advantage_pret = 0, honoraire_admn = 0, patron_cot_av = 0, patron_stationnement_perso = 0, advantage_action = 0, patron_cot_reer = 0, patron_frais_representation = 0, patron_cot_rpa = 0, patron_cot_rac = 0, patron_frais_scol_travail = 0, patron_frais_deplacement = 0): # av pour assurance-vie
        self.patron_frais_deplacement = patron_frais_deplacement
        self.commission_brute = commission_brute
        if not salaire_brut == 0:
            self.salaire_brut = salaire_brut
        if not advantage_action == 0:
            self.advantage_action = advantage_action
        patron_cot_rpa = 0
        patron_cot_rac = 0 # Régime assurance collectif contre la maladie ou les accidents
        patron_frais_scol_travail = 0
        self.revenu_brut_emploi = self.salaire_brut + patron_voyage_perso + patron_frais_scol_perso + self.cauto.imposable + advantage_pret + commission_brute + honoraire_admn + patron_cot_av + patron_stationnement_perso + self.advantage_action + patron_cot_reer + patron_frais_representation
        return self.revenu_brut_emploi
    
    def dah(self, depense_ext = 0, cot_syndic = 0, rpa = 0, bureau_centre_ville = 0, cot_professionnelle = 0, don = 0, frais_cartes_affaires = 0):
        if not rpa == 0:
            self.rpa = rpa
        if not cot_syndic == 0:
            self.cot_syndic = cot_syndic
        if not bureau_centre_ville == 0:
            self.bureau = bureau_centre_ville
        self.deduction_article_huit = depense_ext + self.cot_syndic + self.rpa + self.bureau + cot_professionnelle
        if self.patron_frais_deplacement == 0:
            self.deduction_article_huit+= self.cauto.deductible_amort_interet_pret
        if not self.patron_frais_deplacement == 0:
            self.cauto.deduction_frais_fonctionnement = 0
        if self.est_vendeur == False:
            self.frais_representation = 0
            self.membre_commerce = 0
            self.deduction_article_huit+= self.cauto.deduction_frais_fonctionnement + self.frais_repas*0.5 + self.hebergement + self.frais_stationnement + self.frais_representation + self.membre_commerce
        return self.deduction_article_huit

    # https://www.canada.ca/fr/agence-revenu/services/impot/particuliers/sujets/tout-votre-declaration-revenus/declaration-revenus/remplir-declaration-revenus/deductions-credits-depenses/ligne-22900-autres-depenses-emploi/employes-a-commission.html
    def dahv(self, telephone_bureau_centre_ville = 0, publicite = 0, location_ordi = 0):
        self.deduction_article_huit_vendeur = telephone_bureau_centre_ville + publicite + location_ordi
        if self.est_vendeur == True:
            self.deduction_article_huit_vendeur+= self.cauto.deduction_frais_fonctionnement + self.frais_repas*0.5 + self.hebergement + self.frais_stationnement + self.frais_representation*0.5 + self.membre_commerce
        return self.deduction_article_huit_vendeur
    
    # https://www.canada.ca/fr/agence-revenu/services/impot/entreprises/sujets/entreprise-individuelle-societe-personnes/depenses-entreprise.html
    def travailleur_autonome(self, frais_entretien = 0, salaire_verse = 0, assurances_professionnelles = 0, frais_bancaires = 0, congres = 0, loyer_paye = 0, fnacc_mobilier=[0,0], fourniture = 0, frais_demarrage = 0, frais_deplacement = 0, frais_gestion = 0, frais_livraison = 0, frais_transport = 0, divertissement = 0, publicite = 0, droit_adhesion = 0, permis = 0, cotisation = 0, telephone = 0, chauffage = 0, electricite = 0):
        self.deduction_travailleur_autonome = self.cauto.deduction_travailleur_autonome + self.frais_repas*0.5 + self.hebergement + self.frais_stationnement + self.frais_representation*0.5 + self.membre_commerce + frais_entretien + salaire_verse + assurances_professionnelles + frais_bancaires + congres + loyer_paye + fnacc_mobilier[0]*fnacc_mobilier[1] + fourniture + frais_demarrage + frais_deplacement + frais_gestion + frais_livraison + frais_transport + divertissement + publicite + droit_adhesion + permis + cotisation + telephone + chauffage + electricite
        return self.deduction_travailleur_autonome
    
    def calcul(self):
        self.revenu_net_emploi = self.revenu_brut_emploi - self.deduction_article_huit - self.commission_brute - self.deduction_travailleur_autonome if self.deduction_article_huit_vendeur > self.commission_brute else self.revenu_brut_emploi - self.deduction_article_huit - self.deduction_article_huit_vendeur - self.deduction_travailleur_autonome
        if not self.deduction_article_huit_vendeur == 0:
            print("[INFO] revenu_brut.RevenuBrut.calcul()", round(self.revenu_brut_emploi), round(self.deduction_article_huit), round(self.commission_brute if self.deduction_article_huit_vendeur > self.commission_brute else self.revenu_brut_emploi), round(self.revenu_net_emploi))
        elif not self.deduction_travailleur_autonome == 0:
            print("[INFO] revenu_brut.RevenuBrut.calcul()", round(self.revenu_brut_emploi), round(self.deduction_travailleur_autonome), round(self.revenu_net_emploi))
        else:
            print("[INFO] revenu_brut.RevenuBrut.calcul()", round(self.revenu_brut_emploi), round(self.deduction_article_huit), round(self.revenu_net_emploi))
        return f"{round(self.revenu_brut_emploi)} {round(self.deduction_article_huit)} {round(self.deduction_article_huit_vendeur)} {round(self.deduction_travailleur_autonome)} {round(self.revenu_net_emploi)}"