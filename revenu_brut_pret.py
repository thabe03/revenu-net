# elif pour une condition appartenant au même groupe
# return 0

import datetime

def index_trimestre(date):
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    mois = date_obj.month
    if mois <= 3:
        return 0
    elif mois <= 6:
        return 1
    elif mois <= 9:
        return 2
    else:
        return 3
    
def index_mois(date):
  date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
  mois = date_obj.month
  return int(mois)

def pret(*remb, pret, taux_reduit, taux, pour_travail = 0, start, end):
  if not remb:
    trimestre = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
    trimestre_total = len(trimestre)
    mois_actif = []
    taux_mois = []
    for i in range(1,13):
      if i <= end and i >= start:
        mois_actif.append(True)
      else:
        mois_actif.append(False)
        
    for i in trimestre:
      for j in range(len(taux)):   
        if i == j:
          taux_mois.append(taux[j])
        
    len_group_trimestre_true = []
    for i, j, k in zip(taux_mois, mois_actif, trimestre):
      len_group_trimestre_true.append(sum(1 for x, y in zip(trimestre, mois_actif) if y == True and x == k))

    small_trimestre_true = []

    break_list = [0,3,6,9]
    for i in range(len(len_group_trimestre_true)):
      for j in break_list:
        if i == j:          
          small_trimestre_true.append(len_group_trimestre_true[j])
    taux_habituel_cum = 0      
    for i, j in zip(taux, small_trimestre_true):
      taux_habituel_cum += pret * i/100 * j/trimestre_total
    interet_reel_paye = (pret * (taux_reduit/100) * mois_actif.count(True)/trimestre_total)
    interet_rep_paye = taux_habituel_cum - interet_reel_paye  
    if pour_travail == 1:
      print("[INFO] pret.pret() intérêts réputés payés déductibles", round(interet_rep_paye))
      print("[INFO] pret.pret() intérêts réellement payés déductibles", round(interet_reel_paye))
      avantage_imposable = taux_habituel_cum - interet_reel_paye
      return avantage_imposable
    else:
      print("[INFO] pret.pret() intérêts réputés payés non déductibles", round(interet_rep_paye))
      print("[INFO] pret.pret() intérêts réellement payés non déductibles", round(interet_reel_paye))
      avantage_imposable = taux_habituel_cum - interet_reel_paye
      return avantage_imposable
  else:
    trimestre = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
    trimestre_total = len(trimestre)
    mois_actif = []
    taux_mois = []
    for i in range(1,13):
      if i <= end and i >= start:
        mois_actif.append(True)
      else:
        mois_actif.append(False)
        
    for i in trimestre:
      for j in range(len(taux)):   
        if i == j:
          taux_mois.append(taux[j])
        
    len_group_trimestre_true = []
    for i, j, k in zip(taux_mois, mois_actif, trimestre):
      len_group_trimestre_true.append(sum(1 for x, y in zip(trimestre, mois_actif) if y == True and x == k))

    small_trimestre_true = []

    break_list = [0,3,6,9]
    for i in range(len(len_group_trimestre_true)):
      for j in break_list:
        if i == j:          
          small_trimestre_true.append(len_group_trimestre_true[j])
    taux_habituel_cum = 0 
    inc_four = 0
    for i, j in zip(taux, small_trimestre_true):
      for l, m in remb:
        if inc_four == m:
          taux_habituel_cum += pret * i/100 * j/trimestre_total
          pret = pret - l
        else:
          taux_habituel_cum += pret * i/100 * j/trimestre_total
      inc_four += 1
    interet_reel_paye = (pret * (taux_reduit/100) * mois_actif.count(True)/trimestre_total)
    interet_rep_paye = taux_habituel_cum - interet_reel_paye  
    if pour_travail == 1:
      print("[INFO] pret.pret() intérêts réputés payés déductibles", round(interet_rep_paye))
      print("[INFO] pret.pret() intérêts réellement payés déductibles", round(interet_reel_paye))
      avantage_imposable = taux_habituel_cum - interet_reel_paye
      return avantage_imposable
    else:
      print("[INFO] pret.pret() intérêts réputés payés non déductibles", round(interet_rep_paye))
      print("[INFO] pret.pret() intérêts réellement payés non déductibles", round(interet_reel_paye))
      avantage_imposable = taux_habituel_cum - interet_reel_paye
      return avantage_imposable