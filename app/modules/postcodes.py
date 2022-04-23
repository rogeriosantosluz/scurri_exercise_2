"""
This module aims to validate all the formatting of a postcode
Tests will be run against this module for each validation
"""

from .. import app

#Verify Format
#-------------------------------------------------------------------
#   Format          Coverage                                Example
#-------------------------------------------------------------------
#1. AA9A 9AA	WC postcode area; EC1–EC4, NW1W, SE1P, SW1	EC1A 1BB
#2. A9A 9AA	    E1, N1, W1	                                W1A 0AX
#3. A9 9AA	    B, E, G, L, M, N, S, W	                    M1 1AE
#   A99 9AA	                                                B33 8TH
#4. AA9 9AA     All other postcodes                         CR2 6XH
#   AA99 9AA	                                            DN55 1PT
#-------------------------------------------------------------------
def verify_format(postcode):

    if postcode in special_postcodes:
        return "Postcode {} is special {}".format(postcode, special_postcodes.get(postcode))
        
    valid_formats = ["AA9A 9AA", "A9A 9AA", "A9 9AA", "A99 9AA", "AA9 9AA", "AA99 9AA"]
    for format in valid_formats:
        if len(format) == len(postcode):
            #app.logger.info(f"Lets validate format {format} against postcode {postcode}, same length")
            validate_all_positions = []
            index = 0
            for f in format:
                #app.logger.info(f"Comparing {f} with {postcode[index]}")
                if f.isalpha() and postcode[index].isalpha():
                    validate_all_positions.append(True)    
                    #app.logger.info("Is alpha")
                elif f.isdigit() and postcode[index].isdigit():
                    validate_all_positions.append(True)  
                    #app.logger.info("Is digit")
                elif f == " " and postcode[index] == " ":
                    validate_all_positions.append(True)  
                    #app.logger.info("Is space")
                else:
                    validate_all_positions.append(False)  
                    #app.logger.info("Doesnt match")
                index+=1
            #app.logger.info(validate_all_positions)
            if False not in validate_all_positions:
                app.logger.info("FORMAT MATCH: " + postcode + " " + format)
                return f"Postcode {postcode} matches a valid format {format}"
    return {"error": f"Postcode {postcode} doesnt match a valid format"}

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
    if postcode in special_postcodes:
        return "Postcode {} is special {}".format(postcode, special_postcodes.get(postcode))
    
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
    if postcode in special_postcodes:
        return "Postcode {} is special {}".format(postcode, special_postcodes.get(postcode))

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
            return f"1. Postcode {postcode} has valid area {area} and district {district}"
        elif area in areas and len(district) == 1:
            return f"2. Postcode {postcode} has valid area {area} and district {district}"
        elif area in areas and area == "WC" and len(district) == 2:
            return f"3. Postcode {postcode} has valid area {area} and district {district}"
        else:
            return {"error": f"Postcode {postcode} has an area {area} that should have a single-digit district, {district} provided"}
    return {"error": f"Postcode {postcode} has invalid area or district"}

#Areas with only double-digit districts: AB, LL, SO
def verify_areas_double_digit_district(postcode):
    if postcode in special_postcodes:
        return "Postcode {} is special {}".format(postcode, special_postcodes.get(postcode))

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

#Areas with a district '0' (zero): BL, BS, CM, CR, FY, HA, PR, SL, SS 
# (BS is the only area to have both a district 0 and a district 10)
def verify_areas_with_a_district_zero(postcode):
    if postcode in special_postcodes:
        return "Postcode {} is special {}".format(postcode, special_postcodes.get(postcode))

    areas = ["BL", "BS", "CM", "CR", "FY", "HA", "PR", "SL", "SS"]
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
    app.logger.info(f"area: {area} district: {district}")
    if area != "" and district != "":
        if district == "0":
            if area in areas:
                return f"1. Postcode {postcode} has valid area {area} and district {district}"
        elif district == "10":
            if area == "BS":
                return f"2. Postcode {postcode} has valid area {area} and district {district}"
            else:
                return f"2.1 Postcode {postcode} doent have an area BS ({area}) with a district 0 or 10"
        else:
            return f"3. Postcode {postcode} doent have an area {area} with a district 0 or 10"
    return {"error": f"Postcode {postcode} has invalid area or district"}

#The following central London single-digit districts have been further divided by 
# inserting a letter after the digit and before the space: 
# EC1–EC4 (but not EC50), SW1, W1, WC1, WC2 and parts of E1 (E1W), N1 (N1C and N1P), NW1 (NW1W) and SE1 (SE1P).
def verify_areas_single_digit_district_extra_letter(postcode):
    if postcode in special_postcodes:
        return "Postcode {} is special {}".format(postcode, special_postcodes.get(postcode))

    areas = ["EC1", "EC2", "EC3", "EC4", "SW1", "W1", "WC1", "WC2", "E1", "N1", "NW1", "SE1"]
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
        if district[1:].isalpha():
            if area + district[:-1] in areas:
                if area + district in ["E1W", "N1C", "N1P", "NW1W", "SE1P"]:
                    return f"2. Postcode {postcode} has valid area {area} and district {district}"
                else:
                    return f"3. Postcode {postcode} area+district:{area}{district} allowed any extra letter"
            else:
                return {"error": f"Postcode {postcode} area+district:{area}{district} not allowed to have an extra letter"}
        else:
            return f"4. Postcode {postcode} doesnt have an extra letter district: {district}"
    return {"error": f"Postcode {postcode} has invalid area or district"}

#The letters Q, V and X are not used in the first position.
def verify_first_position(postcode):
    not_allowed = ["Q", "V", "X"]
    if postcode[0] not in not_allowed:
        return f"Postcode {postcode} have allowed letters in first position"
    return {"error": f"Postcode {postcode} has letter {postcode[0]} wich is not allowed {not_allowed} in the first position"}

#The letters I, J and Z are not used in the second position.
def verify_second_position(postcode):
    not_allowed = ["I", "J", "X"]
    if postcode[1] not in not_allowed or postcode in special_postcodes:
        return f"Postcode {postcode} has allowed letters in second position"
    return {"error": f"Postcode {postcode} has letter {postcode[1]} wich is not allowed {not_allowed} in the second position"}

#The only letters to appear in the third position are 
# A, B, C, D, E, F, G, H, J, K, P, S, T, U and W when the structure starts with A9A.
def verify_third_position(postcode):
    if postcode in special_postcodes:
        return "Postcode {} is special {}".format(postcode, special_postcodes.get(postcode))

    allowed = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "P", "S", "T", "U", "W"]
    if postcode[0].isalpha() and postcode[1].isdigit() and postcode[2].isalpha():
        if postcode[2] in allowed:
            return f"Postcode {postcode} has allowed letters in third position"
        else:
            return {"error": f"Postcode {postcode} has letter {postcode[2]} in third position and the allowed letters are {allowed}"}
    else:
        return f"Postcode {postcode} doesnt match the format A9A to be validated"

#The only letters to appear in the fourth position are 
# A, B, E, H, M, N, P, R, V, W, X and Y when the structure starts with AA9A.
def verify_fourth_position(postcode):
    allowed = ["A", "B", "E", "H", "M", "N", "P", "R", "V", "W", "X", "Y"]
    if postcode[0].isalpha() and postcode[1].isalpha() and postcode[2].isdigit() and postcode[3].isalpha(): 
        if postcode[3] in allowed:
            return f"Postcode {postcode} have allowed letters in fourth position"
        else:
            return {"error": f"Postcode {postcode} has letter {postcode[3]} in fourth position and the allowed letters are {allowed}"}
    else:
        return f"Postcode {postcode} doesnt match the format AA9A to be validated"

#The final two letters do not use C, I, K, M, O or V, 
# so as not to resemble digits or each other when hand-written.
def verify_unit(postcode):
    not_allowed = ["C", "I", "K", "M", "O", "V"]
    if postcode[-2:-1].isalpha() and postcode[-1:].isalpha() and postcode[-2:-1] not in not_allowed and postcode[-1:] not in not_allowed:
        return f"Postcode {postcode} have allowed letters in unit position"
    return {"error": f"Postcode {postcode} has invalid unit"}
        

#Postcode sectors are one of ten digits: 0 to 9, 
# with 0 only used once 9 has been used in a post town, save for Croydon and Newport (see above).

special_postcodes = {
    "B1 1HQ": "HSBC UK headquarters at 1 Centenary Square, Birmingham",
    "BN88 1AH": "Amex House",
    "BS98 1TL": "TV Licensing[50]",
    "BX1 1LT": "Lloyds Bank formerly known as Lloyds TSB Bank[51]—non-geographic address",
    "BX2 1LB": "Bank of Scotland (part of Lloyds Banking Group)[52]—non-geographic address",
    "BX3 2BB": "Barclays Bank[53]—non-geographic address",
    "BX4 7SB": "TSB Bank",
    "BX5 5AT": "VAT Central Unit of HM Revenue and Customs[54] (Roman numeral VAT = 5AT)—non-geographic address",
    "CF10 1BH": "Lloyds Banking Group (formerly Black Horse Finance)",
    "CF99 1NA": "Senedd (formerly National Assembly for Wales)",
    "CO4 3SQ": "University of Essex (Square 3)",
    "CV4 8UW": "University of Warwick",
    "CV35 0DB": "Aston Martin after their long line of iconic sports cars that bear the DB moniker",
    "E14 5EY": "Ernst & Young, a Big 4 professional services firm[55]",
    "DA1 1RT": "Dartford F.C. (nicknamed The Darts)",
    "DE99 3GG": "Egg Banking",
    "DE55 4SW": "Slimming World",
    "DH98 1BT": "British Telecom",
    "DH99 1NS": "National Savings certificates administration",
    "E14 5HQ": "HSBC headquarters at 8 Canada Square, Canary Wharf",
    "E14 5JP": "JP Morgan",
    "E16 1XL": "ExCeL London[56]",
    "E20 2AQ": "Olympic Aquatics Centre",
    "E20 2BB": "Olympic Basketball Arena",
    "E20 2ST": "Olympic Stadium",
    "E20 3BS": "Olympic Broadcast Centre",
    "E20 3EL": "Olympic Velodrome",
    "E20 3ET": "Olympic Eton Manor Tennis Courts",
    "E20 3HB": "Olympic Handball Arena (now the Copper Box)",
    "E20 3HY": "Olympic Hockey Stadium",
    "E98 1SN": "The Sun newspaper",
    "E98 1ST": "The Sunday Times newspaper",
    "E98 1TT": "The Times newspaper",
    "EC2N 2DB": "Deutsche Bank",
    "EC4Y 0HQ": "Royal Mail Group Ltd headquarters",
    "EH12 1HQ": "Royal Bank of Scotland headquarters",
    "EH99 1SP": "Scottish Parliament[57] (founded in 1999)",
    "G58 1SB": "National Savings Bank (the district number 58 also approximates the outline of the initials SB)",
    "GIR 0AA": "Girobank (now Santander Corporate Banking)",
    "IV21 2LR": "Two Lochs Radio",
    "L30 4GB": "Girobank (alternative geographic postcode)",
    "LS98 1FD": "First Direct bank",
    "M50 2BH": "BBC Bridge House",
    "M50 2QH": "BBC Quay House",
    "N1 9GU": "The Guardian newspaper",
    "N81 1ER": "Electoral Reform Services[46][58]",
    "NE1 4ST": "St James' Park Stadium, Newcastle United",
    "NG80 1EH": "Experian Embankment House",
    "NG80 1LH": "Experian Lambert House",
    "NG80 1RH": "Experian Riverleen House",
    "NG80 1TH": "Experian Talbot House",
    "PH1 5RB": "Royal Bank of Scotland Perth Chief Office",
    "PH1 2SJ": "St Johnstone Football Club",
    "S2 4SU": "Sheffield United Football Club",
    "S6 1SW": "Sheffield Wednesday Football Club",
    "S14 7UP": "The World Snooker Championships at the Crucible Theatre, Sheffield;[59] 147 UP refers to a maximum lead (from a maximum break) in snooker",
    #"SA99": "Driver and Vehicle Licensing Agency—All postcodes starting with SA99 are for the DVLA offices in the Morriston area of Swansea, the final part of the postcode relates to the specific office or department within the DVLA",
    "SE1 0NE": "One America Street, the London headquarters of architectural firm TP Bennett",
    "SE1 8UJ": "Union Jack Club",
    "SM6 0HB": "Homebase Limited",
    "SN38 1NW": "Nationwide Building Society",
    "SR5 1SU": "Stadium of Light, Sunderland AFC",
    "SW1A 0AA": "House of Commons (Palace of Westminster; see below for House of Lords)",
    "SW1A 0PW": "House of Lords (Palace of Westminster; see above for House of Commons)",
    "SW1A 1AA": "Buckingham Palace (the Monarch)",
    "SW1A 2AA": "10 Downing Street (the Prime Minister)",
    "SW1A 2AB": "11 Downing Street (Chancellor of the Exchequer)",
    "SW1H 0TL": "Transport for London (Windsor House, 50 Victoria Street)",
    "SW1P 3EU": "European Commission and European Parliament office (European Union)",
    "SW1W 0DT": "The Daily Telegraph newspaper",
    "SW11 7US": "Embassy of the United States, London",
    "SW19 5AE": "All England Lawn Tennis and Croquet Club (Venue of the Wimbledon Championships)",
    "TW8 9GS": "GlaxoSmithKline",
    "W1A 1AA": "BBC Broadcasting House",
    "W1D 4FA": "Betgenius, the former address of The Football Association",
    "W1N 4DJ": "BBC Radio 1 (disc jockey)",
    "W1T 1FB": "Facebook"
}

special_postcode_list = []
for postcode in special_postcodes.keys():
    special_postcode_list.append(postcode)