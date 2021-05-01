# -*- coding: utf-8 -*-
"""
Created on Sat May  1 18:43:02 2021

@author: Amruta
"""
from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'