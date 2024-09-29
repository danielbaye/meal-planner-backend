def get_negative_points(energy_kj, sugars_g, saturated_fat_g, sodium_mg):
    # Negative points for energy (kJ)
    if energy_kj <= 335: energy_points = 0
    elif energy_kj <= 670: energy_points = 1
    elif energy_kj <= 1005: energy_points = 2
    elif energy_kj <= 1340: energy_points = 3
    elif energy_kj <= 1675: energy_points = 4
    elif energy_kj <= 2010: energy_points = 5
    elif energy_kj <= 2345: energy_points = 6
    elif energy_kj <= 2680: energy_points = 7
    elif energy_kj <= 3015: energy_points = 8
    elif energy_kj <= 3350: energy_points = 9
    else: energy_points = 10

    # Negative points for sugars (g)
    if sugars_g <= 4.5: sugars_points = 0
    elif sugars_g <= 9: sugars_points = 1
    elif sugars_g <= 13.5: sugars_points = 2
    elif sugars_g <= 18: sugars_points = 3
    elif sugars_g <= 22.5: sugars_points = 4
    elif sugars_g <= 27: sugars_points = 5
    elif sugars_g <= 31: sugars_points = 6
    elif sugars_g <= 36: sugars_points = 7
    elif sugars_g <= 40: sugars_points = 8
    elif sugars_g <= 45: sugars_points = 9
    else: sugars_points = 10

    # Negative points for saturated fat (g)
    if saturated_fat_g <= 1: sat_fat_points = 0
    elif saturated_fat_g <= 2: sat_fat_points = 1
    elif saturated_fat_g <= 3: sat_fat_points = 2
    elif saturated_fat_g <= 4: sat_fat_points = 3
    elif saturated_fat_g <= 5: sat_fat_points = 4
    elif saturated_fat_g <= 6: sat_fat_points = 5
    elif saturated_fat_g <= 7: sat_fat_points = 6
    elif saturated_fat_g <= 8: sat_fat_points = 7
    elif saturated_fat_g <= 9: sat_fat_points = 8
    elif saturated_fat_g <= 10: sat_fat_points = 9
    else: sat_fat_points = 10

    # Negative points for sodium (mg)
    if sodium_mg <= 90: sodium_points = 0
    elif sodium_mg <= 180: sodium_points = 1
    elif sodium_mg <= 270: sodium_points = 2
    elif sodium_mg <= 360: sodium_points = 3
    elif sodium_mg <= 450: sodium_points = 4
    elif sodium_mg <= 540: sodium_points = 5
    elif sodium_mg <= 630: sodium_points = 6
    elif sodium_mg <= 720: sodium_points = 7
    elif sodium_mg <= 810: sodium_points = 8
    elif sodium_mg <= 900: sodium_points = 9
    else: sodium_points = 10

    return energy_points + sugars_points + sat_fat_points + sodium_points


def get_positive_points(fruits_percent, fiber_g, protein_g):
    # Positive points for fruits/vegetables/nuts (percentage)
    if fruits_percent <= 40: fruits_points = 0
    elif fruits_percent <= 60: fruits_points = 1
    elif fruits_percent <= 80: fruits_points = 2
    else: fruits_points = 5

    # Positive points for fiber (g)
    if fiber_g <= 0.9: fiber_points = 0
    elif fiber_g <= 1.9: fiber_points = 1
    elif fiber_g <= 2.8: fiber_points = 2
    elif fiber_g <= 3.7: fiber_points = 3
    elif fiber_g <= 4.7: fiber_points = 4
    else: fiber_points = 5

    # Positive points for protein (g)
    if protein_g <= 1.6: protein_points = 0
    elif protein_g <= 3.2: protein_points = 1
    elif protein_g <= 4.8: protein_points = 2
    elif protein_g <= 6.4: protein_points = 3
    elif protein_g <= 8: protein_points = 4
    else: protein_points = 5

    return fruits_points + fiber_points + protein_points


def calculate_nutri_score(energy_kj, sugars_g, saturated_fat_g, sodium_mg,
                          fruits_percent, fiber_g, protein_g):
    # Get the negative and positive points
    negative_points = get_negative_points(energy_kj, sugars_g, saturated_fat_g,
                                          sodium_mg)
    positive_points = get_positive_points(fruits_percent, fiber_g, protein_g)

    # Total Nutri-Score
    nutri_score = negative_points - positive_points

    return nutri_score


score = calculate_nutri_score(energy_kj, sugars_g, saturated_fat_g, sodium_mg,
                              fruits_percent, fiber_g, protein_g)

print("Nutri-Score:", score)
