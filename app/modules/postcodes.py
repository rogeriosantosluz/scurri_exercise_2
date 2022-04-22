"""
This module aims to validate all the formatting of a postcode
Tests will be run against this module for each validation
"""

from .. import app

#The postcodes are alphanumeric...
def verify_alphanumeric(postcode):
    if postcode.replace(" ", "").isalnum():
        return f"Postcode {postcode} is alphanumeric"
    return {"error": f"Postcode {postcode} is not alphanumeric"}
    
#, and are variable in length: ranging from six to eight characters (including a space).
def verify_length(postcode):
    postcode_len = len(postcode)
    if postcode_len >= 6 and postcode_len <= 8:
        return f"Postcode {postcode} has {postcode_len} lenght"
    return {"error": f"Postcode {postcode} must ranging from six to eight characters (including a space) an this one has {postcode_len} lenght"}

#Each postcode is divided into two parts separated by a single space
def verify_space(postcode):
    if postcode.count(" ") == 1:
        return f"Postcode has a single space"
    return {"error": f"Postcode {postcode} must be separated by a single space"}

#The outward code is the part of the postcode before the single space in the middle. 
#It is between two and four characters long.
def verify_outward_code(postcode):
    outward_code = postcode.split(" ")[0]
    if len(outward_code) >= 2 and len(outward_code) <= 4:
        return f"Postcode {postcode} has valid outward_code lenght"
    return {"error": f"Postcode {postcode} has invalid outward_code lenght. Must be between two and four characters long"}

#The postcode area is either one or two characters long and is alphabetical.
#The postcode district is one digit, two digits or a digit followed by a letter.
def verify_postcode_area_and_district(postcode):
    outward_code = postcode.split(" ")[0]
    area, district = "", ""
    index = 0
    for oc in outward_code:
        if not oc.isdigit():
            area += oc
        else:
            district = outward_code[index:]
            break
        index+=1
    if area != "" and district != "":
        return f"Postcode {postcode} has valid area {area} and district {district}"
    return {"error": f"Postcode {postcode} has invalid area or district"}
    #app.logger.info(f"area: {area} district: {district}")
    
#The inward code is the part of the postcode after the single space in the middle. 
# It is three characters long. 
# The inward code assists in the delivery of post within a postal district. 
# Examples of inward codes are "0NY", "7GZ", "7HF", or "8JQ"
def verify_inward_code(postcode):
    inward_code = postcode.split(" ")[1]
    if len(inward_code) == 3:
        return f"Postcode {postcode} has valid inward code length"
    return {"error": f"Postcode {postcode} has invalid inward code length"}

#The postcode sector is made up of a single digit (the first character of the inward code).
#The postcode unit is two characters added to the end of the postcode sector. 
# A postcode unit generally represents a street, part of a street, a single address, a group of properties, 
# a single property, a sub-section of the property, an individual organisation or 
# (for instance Driver and Vehicle Licensing Agency) a subsection of the organisation. 
# The level of discrimination is often based on the amount of mail received by the premises or business.
def verify_postcode_sector_and_unit(postcode):
    inward_code = postcode.split(" ")[1]
    sector, unit = "", ""
    if inward_code[0].isdigit():
        sector = inward_code[0]
    if inward_code[1:].isalpha():
        unit = inward_code[1:]
    if sector != "" and unit != "":
        return f"Postcode {postcode} has valid sector {sector} and unit {unit}"
    return {"error": f"Postcode {postcode} has invalid sector or unit"}

#Areas with only single-digit districts: BR, FY, HA, HD, HG, HR, HS, HX, JE, LD, SM, SR, WC, WN, ZE (although WC is always subdivided by a further letter, e.g. WC1A)
def verify_areas_single_digit_district(postcode):
    areas = ["BR", "FY", "HA", "HD", "HG", "HR", "HS", "HX", "JE", "LD", "SM", "SR", "WC", "WN", "ZE"]
    outward_code = postcode.split(" ")[0]
    area, district = "", ""
    index = 0
    for oc in outward_code:
        if not oc.isdigit():
            area += oc
        else:
            district = outward_code[index:]
            break
        index+=1
    if area != "" and district != "":
        app.logger.info(f"area: {area} district: {district}")
        if area not in areas:
            app.logger.info(f"area: {area} not in areas") 
            return f"Postcode {postcode} has valid area {area} and district {district}"
        elif area in areas and len(district) == 1:
            return f"Postcode {postcode} has valid area {area} and district {district}"
        else:
            return {"error": f"Postcode {postcode} has an area {area} that should have a single-digit district, {district} provided"}
    return {"error": f"Postcode {postcode} has invalid area or district"}

#Areas with only double-digit districts: AB, LL, SO
def verify_areas_double_digit_district(postcode):
    areas = ["AB", "LL", "SO"]
    outward_code = postcode.split(" ")[0]
    area, district = "", ""
    index = 0
    for oc in outward_code:
        if not oc.isdigit():
            area += oc
        else:
            district = outward_code[index:]
            break
        index+=1
    if area != "" and district != "":
        if area not in areas:
            return f"Postcode {postcode} has valid area {area} and district {district}"
        elif area in areas and len(district) == 2:
            return f"Postcode {postcode} has valid area {area} and district {district}"
        else:
            return {"error": f"Postcode {postcode} has an area {area} that should have double-digit district, {district} provided"}
    return {"error": f"Postcode {postcode} has invalid area or district"}

#Areas with a district '0' (zero): BL, BS, CM, CR, FY, HA, PR, SL, SS (BS is the only area to have both a district 0 and a district 10)

#The following central London single-digit districts have been further divided by inserting a letter after the digit and before the space: EC1–EC4 (but not EC50), SW1, W1, WC1, WC2 and parts of E1 (E1W), N1 (N1C and N1P), NW1 (NW1W) and SE1 (SE1P).

#The letters Q, V and X are not used in the first position.

#The letters I, J and Z are not used in the second position.

#The only letters to appear in the third position are A, B, C, D, E, F, G, H, J, K, P, S, T, U and W when the structure starts with A9A.

#The only letters to appear in the fourth position are A, B, E, H, M, N, P, R, V, W, X and Y when the structure starts with AA9A.

#The final two letters do not use C, I, K, M, O or V, so as not to resemble digits or each other when hand-written.

#Postcode sectors are one of ten digits: 0 to 9, with 0 only used once 9 has been used in a post town, save for Croydon and Newport (see above).