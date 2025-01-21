# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:42:29 2025

@author: Muhammed
"""

"""
PROJENİN ANA AMACI
ÜRÜN FİYATLARININ SCRAPİNG YÖNTEMİYLE ÇEKİLMESİ
ÇEKİLECEK SİTELER:
    GETİR
    MİGROS
    CARREFOUR
    ŞOK
    TRENDYOL
    HEPSİBURADA
    AMAZON
ÜRÜNLERİN BELİRLİ KATEGORİLERE AYRILMASI
BİRİM FİYATLARININ DA HESAPLANMASI
ÜRÜNLERE BELİRLİ İD VERİLEREK GÜNLÜK OLARAK DÜZENLİ ÇEKİLMESİ

"""
########## MODULES #######
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


########## HEADERS #######
headers1={
    "x-language": "tr"
}
headers2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"    
}


########## GETİR #########

getirBaseUrl = "https://getirx-client-api-gateway.getirapi.com/category/products?countryCode=TR&categorySlug="
getirUrls = {
    "su": "su-icecek-ewknEvzsJc",
    "meyve": "meyve-sebze-VN2A9ap5Fm",
    "sut": "sut-urunleri-JGtfnNALTJ",
    "firindan": "firindan-q357eEdgBs",
    "atistirmalik": "atistirmalik-BaaxwkyV1y",
    "dondurma": "dondurma-Aw6YFhRWBI",
    "temelgida": "temel-gida-IQH9bir3bX",
    "kahvaltilik": "kahvalti-iat0l1yrkf",
    "yiyecek": "yiyecek-0VLJmBhnI3",
    "fit": "fit-form-A9ciT987qU",
}

def veriDonustur():
    
    productType = []
    name=[]
    price=[]
    shortDesc=[]
    
    try:
        for i in range(len(x["data"]["category"]["subCategories"])):
            for k in range(len(x["data"]["category"]["subCategories"][i]["products"])):
                productType.append(x["data"]["category"]["subCategories"][i]["name"])
                name.append(x["data"]["category"]["subCategories"][i]["products"][k]["name"])
                price.append(x["data"]["category"]["subCategories"][i]["products"][k]["price"])
                try:
                    shortDesc.append(x["data"]["category"]["subCategories"][i]["products"][k]["shortDescription"])
                except:
                    d = x["data"]["category"]["subCategories"][i]["products"][k]["name"].split("(")[-1][:-1]
                    shortDesc.append(d)

        icecekDict = {"productType": productType,"name":name, "shortDesc": shortDesc, 
                    "price": price}
        dfIcecek = pd.DataFrame(icecekDict)
        return dfIcecek
    except:
        pass

dfUrun = pd.DataFrame()
for k in getirUrls.keys():
    
    r = requests.get(getirBaseUrl+getirUrls[k], headers=headers1)
    x = r.json()
    df = veriDonustur()
    dfUrun = pd.concat([dfUrun,df])