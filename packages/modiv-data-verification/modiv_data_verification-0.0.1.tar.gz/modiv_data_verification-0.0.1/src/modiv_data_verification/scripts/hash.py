import pandas as pd
import hashlib
  
def hash_ids(host_path):
    try:
        df = pd.read_csv(host_path)
    except:
        message = "Invalid CSV File"
        print(message)
        return message
    for index, row in df.iterrows():
        prop_hash_id = str(row['property_location']) + str(row['mod_iv_year']) + str(row['mod_iv_munis_name']) + str('NJ') + str(row['mod_iv_county_name']) + str(row['property_id_blk']) + str(row['property_id_lot']) + str(row['property_id_qualifier'])
        x = hashlib.new('sha256')
        arr = bytes(prop_hash_id, 'utf-8')
        x.update(arr)
        j = x.hexdigest()
        df.at[index, 'hash_id'] = j
    return df