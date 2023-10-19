#input: csv file from bucket

import pandas as pd
import requests
import xmltodict
import hashlib

def validate_addresses(host_path, usps_user_id):
    try:
        df = pd.read_csv(host_path)
    except:
        message = "Invalid CSV File"
        print(message)
        return message
    revision = "1"
    usps_payload={}
    usps_headers = {}
    for index, row in df.iterrows():
        usps_address2 = str(row['property_location'])
        usps_address1 = ''
        usps_state = str(row['State'])
        usps_city = str(row["City"])
        usps_zip5 = ''
    
        xmlBody = '<AddressValidateRequest USERID="' + str(usps_user_id) +'"><Revision>' + revision + '</Revision><Address><Address1>'  + usps_address1 + '</Address1><Address2>' + usps_address2 + '</Address2><City>' + usps_city + '</City><State>' + usps_state + '</State><Zip5>' + usps_zip5 + '</Zip5><Zip4></Zip4></Address></AddressValidateRequest>'
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
            address2 = str(row['property_location'])
        try:
            state = dict_data['AddressValidateResponse']['Address']['State']
        except:
            state = "NJ"
        try:
            city = dict_data['AddressValidateResponse']['Address']['City']
        except:
            city = ""
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
    
        #df.at[index, 'address1'] = str(address1)
        #df.at[index, 'address2'] = str(address2)
        #df.at[index, 'city2'] = str(city)
        #df.at[index, 'state'] = str(state)
        #df.at[index, 'zip5'] = str(zip5)
        #df.at[index, 'zip4'] = str(zip4)
        df.at[index, 'property_location_id'] = str(i)
    
    df = df.drop(columns=['City','State'])

    return df