import requests
import json
from columnar import columnar
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import xlsxwriter
from xlrd import open_workbook
import xlwt
import os

class Comptes:
  def __init__(self, comptes):
    self.comptes = comptes
  
  def get_montant_by_no(self, no):
    montant = [i.montant for i in self.comptes if i.no == no]
    return montant
  
  def get_by_no(self, no):
    for i in self.comptes:
      if i.no == no:
        return i
  
  def add(self, compte):
    self.comptes.append(compte)

  def get_all(self):
    return self.comptes
  
  def get_all_no(self):
    return [i.no for i in self.comptes]
  
  def print_no(self):
    to_print = []
    for i in self.comptes:
      to_print.append([i.date, account_label(i.no), i.no, i.montant])
    headers = ['date', "compte", 'no', 'solde']
    to_print = columnar(to_print, headers, no_borders=True)
    print(to_print)

class CompteHistorique:
  def __init__(self, no, montant, type, date):
    self.no = no
    self.montant = montant
    self.type = type
    self.date = date

class Compte:
  def __init__(self, no):
    self.no = no    
    self.historique = []
    self.solde = 0
    self.type = None
  
  def add_montant(self, montant, type, date):
    self.solde = round(self.solde, 2)
    self.historique.append(CompteHistorique(self.no, montant, type, date))
    self.solde += montant
    self.type = type
  
  def print_history(self):
    to_print = []
    for i in self.historique:
      to_print.append([i.date, account_label(i.no), i.no, i.montant])  
    headers = ['date', "compte", 'no', 'solde']
    to_print = columnar(to_print, headers, no_borders=True)
    print(to_print)

class CompteSimplifie:
  def __init__(self, no, montant):
    self.no = no
    self.montant = montant
    self.type = account_type(no)
    

class Comptabilite:
  def __init__(self, jg = None, info = True):
    self.capital = 0
    self.pn = 0
    self.net = 0 
    if not jg == None:
        self.shortcut_jg_bv(jg, info=info)

  def shortcut_jg_bv(self, jg, info = True):
    print("JOURNAL GÉNÉRAL")
    comptes = Comptes([])
    journal_general = []  
    debit = 0
    credit = 0
    for i,j in jg:
      for k in j:
        compte = Compte(k[0])
        tmp = CompteSimplifie(compte.no, k[1])
        if not tmp.no in comptes.get_all_no():        
          compte.add_montant(tmp.montant, tmp.type, i)
          comptes.add(compte)
        elif tmp.no in comptes.get_all_no():
          compte = comptes.get_by_no(tmp.no)
          compte.add_montant(tmp.montant, tmp.type, i)
        if tmp.type == 1:
          debit += tmp.montant
          if not tmp.montant < 0:
            journal_general.append([i, account_label(tmp.no), tmp.no, tmp.montant, ""])
          else:
            journal_general.append([i, account_label(tmp.no), tmp.no, "", tmp.montant*-1])
        elif tmp.type == 0:
          credit+= tmp.montant
          if not tmp.montant < 0:
            journal_general.append([i, account_label(tmp.no), tmp.no, "", tmp.montant])
          else:
            journal_general.append([i, account_label(tmp.no), tmp.no, tmp.montant*-1, ""])
    journal_general.append(["", "", "", round(debit,0), round(credit,0)])  
    headers = ['date', "compte", 'no', 'débit', 'crédit']
    # write_excel(journal_general, "journal_general")
    journal_general_to_print = columnar(journal_general, headers, no_borders=True)
    if not info == False:
      print(journal_general_to_print)
    if not round(debit,0) == round(credit,0):
      print("[ERREUR] shortcut_jg_bv le débit et le crédit ne balancent pas", debit, credit)      
      return 0
    self.comptes = comptes

    print("BALANCE DE VÉRIFICATION")
    comptes = Comptes([])
    balance_verification = []
    debit = 0
    credit = 0
    for i,j in jg:
      for k in j:
        compte = Compte(k[0])
        tmp = CompteSimplifie(compte.no, k[1])
        if not tmp.no in comptes.get_all_no():        
          compte.add_montant(tmp.montant, tmp.type, i)
          comptes.add(compte)
        elif tmp.no in comptes.get_all_no():
          compte = comptes.get_by_no(tmp.no)
          compte.add_montant(tmp.montant, tmp.type, i)
    for i in comptes.get_all():
      if i.type == 1:
        if not i.solde < 0:
          balance_verification.append([i.no, account_label(i.no), i.solde, ""])
        else:
          balance_verification.append([i.no, account_label(i.no), "", i.solde*-1])
        debit += i.solde
      if i.type == 0:
        if not i.solde < 0:
          balance_verification.append([i.no, account_label(i.no), "", i.solde])
        else:
          balance_verification.append([i.no, account_label(i.no), i.solde*-1, ""])
        credit += i.solde
    balance_verification.append(["", "", round(debit,0), round(credit,0)]) 
    headers = ["no", "compte", "débit", "crédit"]
    balance_verification_to_print = columnar(balance_verification, headers, no_borders=True)
    if not info == False:
      print(balance_verification_to_print)
    if not round(debit,0) == round(credit,0):
      print("[ERREUR] shortcut_jg_bv le débit et le crédit ne balancent pas", round(debit,0), round(credit,0))
      return 0
    ac = []
    al = []
    pc = []
    pl = []
    c = []
    produit = []
    ventes_nettes = []
    cout_des_marchandises_vendues = []
    charge_expl = []
    balance_verification.pop() # total
    for i in balance_verification:
      if i[0] <= 1250:
        ac.append(i)
      elif i[0] <= 1980:
        al.append(i)
      elif i[0] <= 2490:
        pc.append(i)
      elif i[0] <= 2900:
        pl.append(i)
      elif i[0] <= 3490:
        c.append(i)
      elif i[0] <= 4300:
        produit.append(i)
      elif i[0] <= 4640:
        ventes_nettes.append(i)
      elif i[0] <= 5150:
        cout_des_marchandises_vendues.append(i)  
      elif i[0] < 6000:
        charge_expl.append(i)
    self.bv = [ac, al, pc, pl, c, produit, ventes_nettes, cout_des_marchandises_vendues, charge_expl]
    self.ac = self.bv[0]
    self.al = self.bv[1]
    self.pc = self.bv[2]
    self.pl = self.bv[3]
    self.c = self.bv[4]
    self.produit = self.bv[5]
    self.ventes_nettes = self.bv[6]
    self.cout_des_marchandises_vendues = self.bv[7]
    self.charge_expl = self.bv[8]
    
  # balance de vérification fini, reste simplement à générer les états de résultat
  def balance_verification_simplifie(self, input_no, input_montant):
    simplified = Comptes([])
    for i, j in zip(input_no, input_montant):
        simplified.add(CompteSimplifie(i, j))
    print("BALANCE DE VÉRIFICATION")
    balance_verification = []
    debit = 0
    credit = 0

    for i in simplified.get_all():
      if i.type == 1:
        if not i.montant < 0:
          balance_verification.append([i.no, account_label(i.no), i.montant, ""])
        else:
          balance_verification.append([i.no, account_label(i.no), "", i.montant*-1])
        debit += i.montant
      if i.type == 0:
        if not i.montant < 0:
          balance_verification.append([i.no, account_label(i.no), "", i.montant])
        else:
          balance_verification.append([i.no, account_label(i.no), i.montant*-1, ""])
        credit += i.montant
    balance_verification.append(["", "", debit, credit]) 
    headers = ["no", "compte", "débit", "crédit"]
    balance_verification_to_print = columnar(balance_verification, headers, no_borders=True)
    print(balance_verification_to_print)
    if not debit == credit:
      print("[ERREUR] balance_verification_simplifie le débit et le crédit ne balancent pas", debit, credit)
      return 0
    ac = []
    al = []
    pc = []
    pl = []
    c = []
    produit = []
    ventes_nettes = []
    cout_des_marchandises_vendues = []
    charge_expl = []
    balance_verification.pop() # total
    for i in balance_verification:
      if i[0] <= 1250:
        ac.append(i)
      elif i[0] <= 1980:
        al.append(i)
      elif i[0] <= 2490:
        pc.append(i)
      elif i[0] <= 2900:
        pl.append(i)
      elif i[0] <= 3490:
        c.append(i)
      elif i[0] <= 4300:
        produit.append(i)
      elif i[0] <= 4640:
        ventes_nettes.append(i)
      elif i[0] <= 5150:
        cout_des_marchandises_vendues.append(i)  
      elif i[0] < 6000:
        charge_expl.append(i)
    self.bv = [ac, al, pc, pl, c, produit, ventes_nettes, cout_des_marchandises_vendues, charge_expl]
    self.ac = self.bv[0]
    self.al = self.bv[1]
    self.pc = self.bv[2]
    self.pl = self.bv[3]
    self.c = self.bv[4]
    self.produit = self.bv[5]
    self.ventes_nettes = self.bv[6]
    self.cout_des_marchandises_vendues = self.bv[7]
    self.charge_expl = self.bv[8]
    return self.bv

  def etat_resultat(self):
    print("ÉTAT DES RÉSULTATS")
    produit = 0
    ventes_nettes = 0
    cout_des_marchandises_vendues = 0
    charge = 0
    marge_beneficiaire_brute = 0
    to_print = []

    to_print.append(["\nVentes nettes\n", "", ""])
    for i in self.ventes_nettes:
        try:
          to_print.append([i[1], "", f"{round(i[3], 0)}"])          
          ventes_nettes+= i[3]
        except:
          to_print.append([f"Moins: {i[1]}", round(i[2], 0), ""])
          ventes_nettes-= i[2]
    to_print.append(["Ventes nettes", "", round(ventes_nettes, 0)])

    to_print.append(["\nProduits - Produits d'exploitation\n", "", ""])
    for i in self.produit:
        to_print.append([i[1], "", round(i[3], 0)])
        produit += i[3]
    produit+=ventes_nettes
    to_print.append(["Total de produits d'exploitation", "", round(produit, 0)])

    to_print.append(["\nCoût des marchandises vendues\n", "", ""])
    for i in self.cout_des_marchandises_vendues:
        try:
          to_print.append([i[1], round(i[2], 0), ""])            
          cout_des_marchandises_vendues+= i[2]
        except:
          to_print.append([f"Moins: {i[1]}", "", f"{round(i[3], 0)}"])        
          cout_des_marchandises_vendues-= i[3]
    to_print.append(["Coût des marchandises vendues", "", round(cout_des_marchandises_vendues, 0)])
    marge_beneficiaire_brute = produit-cout_des_marchandises_vendues

    to_print.append(["Marge bénéficiaire brute", "", round(marge_beneficiaire_brute, 0)])

    to_print.append(["\nCharges - Charges d'exploitation\n", "", ""])
    for i in self.charge_expl:
        to_print.append([i[1], round(i[2], 0), ""])
        charge += i[2]
    to_print.append(["Total des charges d'exploitation", "", round(charge, 0)])

    if marge_beneficiaire_brute-charge > 0:
      self.net = marge_beneficiaire_brute-charge
      self.pn = 1
      to_print.append(["Bénéfice net", "", round(self.net, 0)])
    else:
      self.net = (marge_beneficiaire_brute-charge)*-1
      self.pn = 0
      to_print.append(["Perte net", "", round(self.net, 0)])
    to_print = columnar(to_print, no_borders=True)
    print(to_print)

  def etat_capitaux_propres(self):
    print("ÉTAT DES CAPITAUX PROPRES")
    to_print = []
    retrait = 0
    apport = 0
    benefice_non_reparti = 0
    for i in self.c:
      if i[0] == 3300:
        retrait = i[2]
      if i[0] == 3200:
        apport = i[3]
      if i[0] == 3100:
        self.capital = i[3]
      if i[0] == 3475:
        benefice_non_reparti = i[3]
    to_print.append(["Capital", "", round(self.capital, 0)])
    if self.pn == 1:
      to_print.append(["Plus: Bénéfice net", "", round(self.net, 0)])
      self.capital += self.net
    if self.pn == 0:
      to_print.append(["Moins: Perte net", round(self.net, 0), ""])
      self.capital -= self.net
    if not benefice_non_reparti == 0:
      to_print.append(["Plus: Bénéfice non réparti", "", round(benefice_non_reparti, 0)])
      self.capital += benefice_non_reparti
    if not apport == 0:
      to_print.append(["Plus: Apports", "", round(apport, 0)])
      self.capital += apport
    if not retrait == 0:
      to_print.append(["Moins: Retraits", round(retrait, 0), ""])
      self.capital -= retrait
    to_print.append(["Capital", "", round(self.capital, 0)])
    to_print = columnar(to_print, no_borders=True)
    print(to_print)
  
  def bilan(self):
    print("BILAN")
    to_print = []
    ac = 0
    to_print.append(["\nActif à court terme\n", "", ""])
    for i in self.ac:
      try:
        to_print.append([account_label(i[0]), round(i[2], 0), ""])
        ac+= i[2]
      except:
        to_print.append([account_label(i[0]), "", f"({round(i[3], 0)})"])
        ac-= i[3]
    to_print.append(["Total de l'actif à court terme", "", round(ac, 0)])
    al = 0
    to_print.append(["\nActif à long terme\n", "", ""])
    for i in self.al:
      try:
        to_print.append([account_label(i[0]), round(i[2], 0), ""])
        al+= i[2]
      except:
        to_print.append([f"Moins: {account_label(i[0])}", "", round(i[3], 0)])
        al-= i[3]
    to_print.append(["Total de l'actif à long terme", "", round(al, 0)])
    to_print.append(["Total de l'actif", "", round(ac+al, 0)])
    pc = 0
    to_print.append(["\nPassif à court terme\n", "", ""])
    for i in self.pc:
      try:
        to_print.append([account_label(i[0]), "", round(i[3], 0)])
        pc+= i[3]
      except:
        to_print.append([f"Plus: {account_label(i[0])}", round(i[2], 0), ""])
        pc-= i[2]
    to_print.append(["Total du passif à court terme", "", round(pc, 0)])
    pl = 0
    to_print.append(["\nPassif à long terme\n", "", ""])
    for i in self.pl:
      to_print.append([account_label(i[0]), "", round(i[3], 0)])
      pl+= i[3]
    to_print.append(["Total du passif à long terme", "", round(pl, 0)])
    to_print.append(["\nCapitaux propres\n", "", ""])
    to_print.append(["Thalia Be - capital", "", round(self.capital, 0)])
    to_print.append(["Total du passif et des capitaux propres", "", round(pc+pl+self.capital, 0)])
    to_print = columnar(to_print, no_borders=True)
    print(to_print)
    if not round(ac+al, 0) == round(pc+pl+self.capital, 0):
      print("[ERREUR] bilan l'actif n'est pas égal au passif+capitaux propres", round(ac+al, 0), round(pc+pl+self.capital, 0))
      return 0

  def calcul_bilan(self):
    self.etat_resultat()
    self.etat_capitaux_propres()
    self.bilan()
  
  def ratio_fond_roulement(self):
    ac = 0
    pc = 0
    for i in self.ac:
      try:
        ac+= i[2]
      except:
        ac-= i[3]
    for i in self.pc:
      pc+= i[3]
    fond_roulement = ac/pc
    if fond_roulement < 1:
        print("[Alerte] ratio_fond_roulement le ratio devrait être supérieur à 1 et idéalement, tendre vers 2 ou plus. Comparer au ratio observé dans le secteur d’activité de l’entreprise ou à celui d’entreprises concurrentes. Porter une attention particulière à la qualité des éléments de l’actif à court terme, principalement les stocks et les comptes clients.")
        return 0
    return fond_roulement
  
  def get_by_no_history(self, no):
    return format_history(self.comptes.get_by_no(no).historique)
  
  
def account_label(no):
  response = requests.get(f"http://127.0.0.1:5001/{no}", verify=False)
  if not response.status_code == 200:
    return 0
  data = json.loads(response.text)
  compte = data["plan_comptable"]["compte"]
  return compte

def account_type(no):
  response = requests.get(f"http://127.0.0.1:5001/{no}", verify=False)
  if not response.status_code == 200:
    return 0
  data = json.loads(response.text)
  type = data["plan_comptable"]["type"]
  return type

def format_history(history):
    format_history = []
    solde = 0
    print("GRAND LIVRE", account_label(history[0].no))
    for i in history:
      if i.type == 1:
        solde += i.montant
        format_history.append([i.date, i.montant, "", solde])
      if i.type == 0:
        solde += i.montant
        format_history.append([i.date, "", i.montant, solde])
    headers = ["date", "débit", "crédit", "solde"]
    format_history_to_print = columnar(format_history, headers, no_borders=True)
    print(format_history_to_print)

# def write_excel(array, feuille):
#   array = np.transpose(array,axes=None)
#   df = pd.DataFrame(array).T
#   df.to_excel()




