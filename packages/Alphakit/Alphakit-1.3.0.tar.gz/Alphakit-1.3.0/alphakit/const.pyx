# -*- coding: utf-8 -*-
BARRA_INDUSTRY = [
    'Bank', 'RealEstate', 'Health', 'Transportation', 'Mining', 'NonFerMetal',
    'HouseApp', 'LeiService', 'MachiEquip', 'BuildDeco', 'CommeTrade',
    'CONMAT', 'Auto', 'Textile', 'FoodBever', 'Electronics', 'Computer',
    'LightIndus', 'Utilities', 'Telecom', 'AgriForest', 'CHEM', 'Media',
    'IronSteel', 'NonBankFinan', 'ELECEQP', 'AERODEF', 'Conglomerates'
]
BARRA_COUNTRY = ['COUNTRY']
BARRA_RISKFACTOR = [
    'BETA', 'MOMENTUM', 'SIZE', 'EARNYILD', 'RESVOL', 'GROWTH', 'BTOP',
    'LEVERAGE', 'LIQUIDTY', 'SIZENL'
]
BARRA_ALL = BARRA_INDUSTRY + BARRA_COUNTRY + BARRA_RISKFACTOR
BARRA_SIZEIND = BARRA_INDUSTRY + BARRA_COUNTRY + ['SIZE', 'SIZENL']

BARRA_ALL_K = list('f_' + i for i in BARRA_ALL)
BARRA_SIZEIND_K = list('f_' + i for i in BARRA_SIZEIND)