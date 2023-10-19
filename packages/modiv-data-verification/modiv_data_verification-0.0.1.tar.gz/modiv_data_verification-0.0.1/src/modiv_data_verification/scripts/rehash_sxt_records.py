#input: space and time query (json)

import pandas as pd
import json
import requests
import xmltodict
import hashlib

def rehash(content, usps_user_id):
    data = json.dumps(content)
    df = pd.read_json(data)

    #USERID = "329INSTR4397"
    revision = "1"
    usps_payload={}
    usps_headers = {}

    for index, row in df.iterrows():
        usps_address2 = str(row['ADDRESS2'])
        usps_address1 = str(row['ADDRESS1'])
        if usps_address1 == "None":
            usps_address1 = ""
        #usps_state = "NJ"
        usps_state = str(row['STATE'])
        usps_city = str(row['TOWN'])
        usps_zip5 = str(row['ZIP5'])
    
        xmlBody = '<AddressValidateRequest USERID="' + USERID +'"><Revision>' + revision + '</Revision><Address><Address1>'  + usps_address1 + '</Address1><Address2>' + usps_address2 + '</Address2><City>' + usps_city + '</City><State>' + usps_state + '</State><Zip5>' + usps_zip5 + '</Zip5><Zip4></Zip4></Address></AddressValidateRequest>'
        usps_url = "http://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=" + xmlBody
        response = requests.request("GET", url=usps_url, headers=usps_headers, data=usps_payload)
        dict_data = xmltodict.parse(response.content)
    
        try:
            address1 = dict_data['AddressValidateResponse']['Address']['Address1']
        except:
            address1 = ""
        try:
            address2 = dict_data['AddressValidateResponse']['Address']['Address2']
        except:
            address2 = str(row['ADDRESS2'])
        try:
            state = dict_data['AddressValidateResponse']['Address']['State']
        except:
            state = "NJ"
        try:
            city = dict_data['AddressValidateResponse']['Address']['City']
        except:
            city = str(row['TOWN'])
        try:
            zip5 = dict_data['AddressValidateResponse']['Address']['Zip5']
        except:
            zip5 = ""
        try:
            zip4 = dict_data['AddressValidateResponse']['Address']['Zip4']
        except:
            zip4 = ""
       
        if type(address1) == str:
            pass
        else:
            address1 = ""
        if type(address2) == str:
            pass
        else:
            address2 = ""
        if type(city) == str:
            pass
        else:
            city = ""
        if type(state) == str:
            pass
        else:
            state = ""
        if type(zip5) == str:
            pass
        else:
            zip5 = ""
        if type(zip4) == str:
            pass
        else:
            zip4 = ""
                
        myString = (str(address1) + ' ' + str(address2) + ' ' + str(city) + ' ' + str(state) + ' ' + str(zip5) + ' ' + str(zip4))
        h = hashlib.new('sha256')
        arr = bytes(myString, 'utf-8')
        h.update(arr)
        i = h.hexdigest()

        df.at[index, 'new_address1'] = str(address1)
        df.at[index, 'new_address2'] = str(address2)
        df.at[index, 'new_city2'] = str(city)
        df.at[index, 'new_state'] = str(state)
        df.at[index, 'new_zip5'] = str(zip5)
        df.at[index, 'new_zip4'] = str(zip4)
        df.at[index, 'new_hash_id'] = str(i)
    
    return df