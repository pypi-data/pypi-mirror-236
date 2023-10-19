from  modiv_data_verification.scripts.validate_address import validate_addresses
from modiv_data_verification.scripts.schema import Schema
from modiv_data_verification.scripts.hash import hash_ids

#from  scripts.validate_address import validate_addresses
#from scripts.schema import Schema
#from scripts.hash import hash_ids
import sys
import pandas as pd
import os

#from schemas.schema import Schema


#balcony-modiv-etl/unprocessed
#balcony-modiv-etl/batched
#balcony-modiv-etl/schema-verified
#balcony-modiv-etl/address-verified
#balcony-modiv-etl/mapped


class Verify():
    def __init__(self, host_path, filename, destination_path, usps_user_id):
        self.host_path = host_path
        self.usps_user_id = usps_user_id
        self.filename = filename
        self.schema_id, self.year, self.city, self.state, self.county = self.parse_filename(self.filename)
        self.destination_path = destination_path

    def verify_schema_map_columns(self):
        schema_verifier = Schema(self.schema_id, str(self.year), self.city, self.state, self.county)
        df, err = schema_verifier.validate_dataframe_schema(self.host_path)
        df = schema_verifier.map_columns(df, self.schema_id)
        df.to_csv(self.destination_path, index=False)
        #return df, err

#    def batch_file(self, df):
#        batch_size = 1000
#        batches = [df[i:i + batch_size] for i in range(0, len(df), batch_size)]
#        path = self.host_path.split('.')[0]
#        path.replace('unprocessed','batched')
#        for i, batch in enumerate(batches):
#            batch.to_csv(path + '_' + str(i) + '.csv', index=False)

#    def rename_columns(self):
#        df = map_columns(self.host_path, self.schema_id)
#        df.to_csv('002_2022_ESSEX_ABC_ColumnsRenamed.csv', index=False)
#        #return df

    def validate_address(self):
        df = validate_addresses(self.host_path, self.usps_user_id)
        df.to_csv(self.destination_path, index=False)
        #return df, err

    def hash_modiv_records(self):
        df = hash_ids(self.host_path)
        df.to_csv(self.destination_path, index=False)
        #return df
    
    def parse_filename(self):
        file = self.filename.split("/")[-1]
        schema = file.split('_')[0]
        year = file.split('_')[1]
        city = file.split('_')[2]
        state = file.split('_')[3]
        county = file.split('_')[4].split('.')[0]
        return schema, year, city, state, county


#verify = Verify('002_2022_ESSEX_ABC.csv', "329INSTR4397")
#verify.verify_schema()

#verify = Verify('002_2022_ESSEX_ABC_SchemaVerified.csv', "329INSTR4397")
#verify.rename_columns()

#verify = Verify('002_2022_ESSEX_ABC_ColumnsRenamed.csv', "329INSTR4397")
#verify.validate_address()

#verify = Verify('002_2022_ESSEX_ABC_AddressesVerified.csv', "329INSTR4397")
#verify.hash_modiv_records()


#verify = Verify("002")
#verify._verify_new_records(sys.argv[1], sys.argv[2])

#df, err = verify_schema(df)
#df = rename_columns(df)
#df, err = validate_address(df)
#df = hash_modiv_records(df)
#return df
    