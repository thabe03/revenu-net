# return value name of the function

    

def frais_de_garde(age_enfant = [0], revenu = 0, cpe = 0, colonie_vac = [0,0], gardiennage = 0):
  # 450 pour 2 semaines
  colonie_vac = 125*colonie_vac[1] if colonie_vac[0]/colonie_vac[1] > 125 else colonie_vac[0]*colonie_vac[1]
  frais_de_garde = cpe + colonie_vac + gardiennage
  
  limite_7 = 8000
  limite_16 = 5000

  limite_globale = 0
  for i in age_enfant:
    if i < 7:
      limite_globale += limite_7
    elif i < 16:
      limite_globale += limite_16
    else:
      limite_globale += 0

  deux_tier = 2/3*revenu

  if frais_de_garde > limite_globale:
    print("[INFO] frais_de_garde non déductibles en raison de la limite globable par enfant", limite_globale)
    return 0
  elif frais_de_garde > deux_tier:
    print("[INFO] frais_de_garde non déductibles parce que les frais de gardes dépassent le 2/3 du revenu", deux_tier)
    return 0
  else:
    print("[INFO] frais_de_garde déductibles")
    return frais_de_garde
  


def deduction_source(impot_fed_prov = 0, rrq = 0, ass_emploi = 0, rqap = 0, rpa = 0, rcam = 0):
  # Régime collectif d'assurance maladie
  deduction_source = impot_fed_prov + rrq + ass_emploi + rqap + rpa + rcam
  return deduction_source