from flask import Flask
import json
import pytest

from .. import app

def test_status_code_200():
    client = app.test_client()
    url = '/postcodes'
    response = client.get(url)
    assert response.status_code == 200