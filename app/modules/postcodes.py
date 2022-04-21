"""
This module aims to validate all the formatting of a postcode
Tests will be run against this module for each validation
"""

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