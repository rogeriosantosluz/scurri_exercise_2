from flask import Flask
import json
import pytest
from ..modules.postcodes import *

from .. import app

simple_postcode = "BB1 1BD"
invalid_postcode = "BLA"
invalid_postcode_many_spaces = "BB1  1BD"
invalid_alphanumeric_postcode = "BLA%"
postcode_examples = ["SW1W 0NY", "PO16 7GZ", "GU16 7HF", "L1 8JQ"]

def test_status_code_200():
    client = app.test_client()
    url = f'/postcodes/{simple_postcode}'
    response = client.get(url)
    assert response.status_code == 200

def test_response_json_has_data():
    client = app.test_client()
    url = f'/postcodes/{simple_postcode}'
    response = client.get(url)
    resp_dict = json.loads(response.text)    
    assert "data" in resp_dict


def test_response_data_has_postcode():
    client = app.test_client()
    url = f'/postcodes/{simple_postcode}'
    response = client.get(url)
    resp_dict = json.loads(response.text)    
    assert "postcode" in resp_dict["data"]

#The postcodes are alphanumeric, 
def test_postcode_alphanumeric():
    assert "error" not in verify_alphanumeric(simple_postcode)
    
def test_invalid_postcode_alphanumeric():
    assert "error" in verify_alphanumeric(invalid_alphanumeric_postcode)
    
# and are variable in length: ranging from six to eight characters (including a space).
def test_postcode_length():
    assert "error" not in verify_length(simple_postcode)
    
def test_invalid_postcode_length():
    assert "error" in verify_length(invalid_postcode)
    
#Each postcode is divided into two parts separated by a single space
def test_postcode_space():
    assert "error" not in verify_space(simple_postcode)
    
def test_invalid_postcode_space():
    assert "error" in verify_space(invalid_postcode)
    
def test_invalid_postcode_many_spaces():
    assert "error" in verify_space(invalid_postcode_many_spaces)
    
#The outward code is the part of the postcode before the single space in the middle. It is between two and four characters long.
def test_valid_outward_code():
    assert "error" not in verify_space(simple_postcode)
    
def test_invalid_outward_code():
    assert "error" in verify_space(invalid_postcode)