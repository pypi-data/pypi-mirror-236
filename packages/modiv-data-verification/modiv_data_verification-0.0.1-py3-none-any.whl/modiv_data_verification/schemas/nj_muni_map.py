import pandas as pd

nj_mun_map = {201: 'ALLENDALE BORO',
    202: 'ALPINE BORO',
    203: 'BERGENFIELD BORO',
    204: 'BOGOTA BORO',
    205: 'CARLSTADT BORO',
    206: 'CLIFFSIDE PARK BORO',
    207: 'CLOSTER BORO',
    208: 'CRESSKILL BORO',
    209: 'DEMAREST BORO',
    210: 'DUMONT BORO',
    211: 'ELMWOOD PARK BORO',
    212: 'E RUTHERFORD BORO',
    213: 'EDGEWATER BORO',
    214: 'EMERSON BORO',
    215: 'ENGLEWOOD CITY',
    216: 'ENGLEWOOD CLIFFS BORO',
    217: 'FAIRLAWN BORO',
    218: 'FAIRVIEW BORO',
    219: 'FORT LEE BORO',
    220: 'FRANKLIN LAKES BORO',
    221: 'GARFIELD CITY',
    222: 'GLEN ROCK BORO',
    223: 'HACKENSACK CITY',
    224: 'HARRINGTON PARK BORO',
    225: 'HASBROUCK HGHTS BORO',
    226: 'HAWORTH BORO',
    227: 'HILLSDALE BORO',
    228: 'HOHOKUS BORO',
    229: 'LEONIA BORO',
    230: 'LITTLE FERRY BORO',
    231: 'LODI BORO',
    232: 'LYNDHURST TWP',
    233: 'MAHWAH TWP',
    234: 'MAYWOOD BORO',
    235: 'MIDLAND PARK BORO',
    236: 'MONTVALE BORO',
    237: 'MOONACHIE BORO',
    238: 'NEW MILFORD BORO',
    239: 'NORTH ARLINGTON BORO',
    240: 'NORTHVALE BORO',
    241: 'NORWOOD BORO',
    242: 'OAKLAND BORO',
    243: 'OLD TAPPAN BORO',
    244: 'ORADELL BORO',
    245: 'PALISADES PARK BORO',
    246: 'PARAMUS BORO',
    247: 'PARK RIDGE BORO',
    248: 'RAMSEY BORO',
    249: 'RIDGEFIELD BORO',
    250: 'RIDGEFIELD PARK VILLAGE',
    251: 'RIDGEWOOD VILLAGE',
    252: 'RIVEREDGE BORO',
    253: 'RIVERVALE TWP',
    254: 'ROCHELLE PARK TWP',
    255: 'ROCKLEIGH BORO',
    256: 'RUTHERFORD BORO',
    257: 'SADDLE BROOK TWP',
    258: 'SADDLE RIVER BORO',
    259: 'SO HACKENSACK TWP',
    260: 'TEANECK TWP',
    261: 'TENAFLY BORO',
    262: 'TETERBORO BORO',
    263: 'UPPER SADDLE RIV BORO',
    264: 'WALDWICK BORO',
    265: 'WALLINGTON BORO',
    266: 'WASHINGTON TWP',
    267: 'WESTWOOD BORO',
    268: 'WOODCLIFF LAKE BORO',
    269: 'WOOD RIDGE BORO',
    270: 'WYCKOFF TWP'}

schema001_map = {'BLOCK':'property_id_blk', 'LOT':'property_id_lot', 'QUALIFIER':'property_id_qualifier', 'PROPERTY_CCDD':'mun_code_id',
        'PROPERTY_LOCATION':'property_location', 'PROPERTY_CLASS':'property_class', 'OWNER_ADDRESS':'street_address',
        'OWNER_CITYSTATE':'city_state', 'OWNER_ZIP':'zip_code', 'VALUES_IMPROVTAXABLEVALUE':'improvement_value',
        'VALUES_LANDTAXABLEVALUE':'land_value', 'VALUES_NETTAXABLEVALUE':'net_taxable_value',
        'EXEMPTION_AMOUNT_1':'exemption_amount_1', 'EXEMPTION_AMOUNT_2':'exemption_amount_2', 'EXEMPTION_AMOUNT_3':'exemption_amount_3',
        'EXEMPTION_AMOUNT_4':'exemption_amount_4', 'NUMBER_BUILDINGSF':'number_of_dwellings', 'PROPERTY_CONSTRUCTIONYEAR':'year_constructed',
        'PROPERTY_BUILDINGCLASS':'building_class_code', 'OLD_OLDBLOCK':'old_block', 'OLD_OLDLOT':'old_lot',
        'OLD_OLDQUALIFIER':'old_qualifier', 'NONE_LASTTRANSACTIONDT':'last_trans_date_MMDDYY', 'PROPERTY_ZONING':'zoning',
        'PROPERTY_TAXACCOUNT':'tax_acct_number', 'OWNER_MORTGAGEACCOUNT':'mortgage_account_number', 'OWNER_BILLINGCODE':'assessment_code',
        'EXEMPT_SPECIALTAXCODE_1':'sptax_code_1', 'EXEMPT_SPECIALTAXCODE_2':'sptax_code_2',
        'EXEMPT_SPECIALTAXCODE_3':'sptax_code_3', 'EXEMPT_SPECIALTAXCODE_4':'sptax_code_4',
        'CUSTOM_ACREAGE_2DECIMALS':'calculated_acreage1', 'TAXMAP_NUMERIC':'tax_map_page_number', 'PROPERTY_ADDITIONALLOT1':'additional_lots_1',
        'PROPERTY_ADDITIONALLOT2':'additional_lots_2', 'PROPERTY_LANDDIMENSION':'land_description',
        'PROPERTY_BUILDINGDESCRIPTION':'building_description', 'PROPERTY_CLASS4USECODE':'property_class_code_name',
        'PROPERTY_ACREAGE':'calculated_acreage2', 'EXEMPT_OWNERSHIP':'epl_own', 'EXEMPT_PURPOSE':'epl_use',
        'EXEMPT_DESCRIPTION':'epl_description', 'EXEMPT_STATUTE':'statute_number', 'EXEMPT_INITIALFILINGDATE':'initial_date_MMDDYY',
        'EXEMPT_FURTHERFILINGDATE':'further_date_MMDDYY', 'EXEMPT_FACILITYNAME':'facility_name',
        'CUSTOM_20_TAX_PRIORYRNETTAX_2DECIMALS':'prior_year_net_value', 'CURRENTSALE_DATE':'deed_date_MMDDYY',
        'CURRENTSALE_DEEDBOOK':'deed_book', 'CURRENTSALE_DEEDPAGE':'deed_page', 'CURRENTSALE_PRICE':'sale_price',
        'CURRENTSALE_NUC ':'sales_price_code'}

schema_mapper_dict = {"001":{"state":"NJ", "current_modiv_year":2023, "schema_map":schema001_map, "muni_map":nj_mun_map}}


columns = ['hash_id', 
        'property_location_id', 
        'property_location_hash_id', 
        'mod_iv_recordid', 
        'mod_iv_year', 
        'mun_code_id', 
        'mod_iv_county_name', 
        'mod_iv_munis_name', 
        'gis_pin', 
        'county_district', 
        'property_id_blk', 
        'property_id_lot', 
        'property_id_qualifier', 
        'qualification_code_name', 
        'record_id',
        'sub_record_id', 
        'last_trans_date_MMDDYY', 
        'last_trans_update_number', 
        'tax_acct_number', 
        'property_class', 
        'property_class_code_name', 
        'property_location', 
        'building_description', 
        'land_description', 
        'calculated_acreage', 
        'additional_lots_1', 
        'additional_lots_2', 
        'zoning', 
        'tax_map_page_number', 
        'owner_name', 
        'street_address', 
        'city',
        'state', 
        'zip_code', 
        'zip_code_plus_four', 
        'number_of_owners', 
        'deduction_amount', 
        'filler', 
        'bank_code', 
        'mortgage_account_number', 
        'deed_book', 
        'deed_page', 
        'sales_price_code', 
        'deed_date_MMDDYY', 
        'sale_price', 
        'sale_assessment', 
        'sale_sr1a_non_usable_code', 
        'number_of_dwellings', 
        'number_of_commercial_dwell', 
        'multiple_occupancy_code', 
        'percentage_owned_code', 
        'rebate_code', 
        'additional_rebate_code', 
        'delquency_code', 
        'epl_own', 
        'epl_own_name_of_owner', 
        'epl_use', 
        'epl_use_name', 
        'epl_description', 
        'epl_description_name', 
        'initial_date_MMDDYY', 
        'further_date_MMDDYY', 
        'statute_number', 
        'facility_name', 
        'building_class_code', 
        'building_class_code_dwelling_type', 
        'building_class_code_class', 
        'year_constructed', 
        'assessment_code', 
        'land_value', 
        'improvement_value', 
        'net_taxable_value', 
        'sptax_code_1', 
        'sptax_code_1_id', 
        'sptax_code_1_name', 
        'sptax_code_2', 
        'sptax_code_2_id', 
        'sptax_code_2_name', 
        'sptax_code_3', 
        'sptax_code_3_id', 
        'sptax_code_3_name', 
        'sptax_code_4', 
        'sptax_code_4_id', 
        'sptax_code_4_name', 
        'exemption_code_1', 
        'exemption_amount_1', 
        'exempt_code_1_name', 
        'exemption_code_2', 
        'exemption_amount_2', 
        'exempt_code_2_name', 
        'exemption_code_3', 
        'exemption_amount_3', 
        'exempt_code_3_name', 
        'exemption_code_4', 
        'exemption_amount_4', 
        'exempt_code_4_name', 
        'senior_citizen_count', 
        'veteran_count', 
        'widows_of_veterans_count', 
        'surviving_spouse_count', 
        'disable_person_count', 
        'user_field_1', 
        'user_field_2', 
        'old_property_id', 
        'old_block', 
        'old_lot', 
        'old_qualifier', 
        'census_tract', 
        'census_block', 
        'property_use_code', 
        'property_use_code_name', 
        'property_flags', 
        'tenant_rebate_response_flg', 
        'tenant_rebate_base_year', 
        'tenant_rebate_base_yr_tax', 
        'tenant_rebate_base_yr_tax_text', 
        'tenant_rebate_base_yr_net_val', 
        'filler_1', 
        'last_year_total_tax', 
        'current_year_total_tax', 
        'school_tax_overage', 
        'taxes_non_municipal_half1', 
        'taxes_non_municipal_half1_text', 
        'taxes_non_municipal_half2', 
        'taxes_non_municipal_half2_text', 
        'taxes_municipal_half1', 
        'taxes_municipal_half1_text', 
        'taxes_municipal_half2', 
        'taxes_municipal_half2_text', 
        'taxes_non_municipal_half3', 
        'taxes_non_municipal_half3_text', 
        'taxes_municipal_half3', 
        'taxes_municipal_half3_text', 
        'taxes_bill_status_flag', 
        'taxes_estimated_qtr3_tax', 
        'prior_year_net_value', 
        'statement_of_state_aid_amt']

def schema_mapper(source_data, schema_id):
    df = pd.DataFrame(columns=columns)
    #print("Empty DF Columns: ", df.columns)
    #print("Source Data Columns: ", source_data.columns)
    source_data.rename(schema_mapper_dict[schema_id]["schema_map"], axis=1, inplace=True)
    #print(mapped_df.head())
    mapped_df = source_data
    #print("Mapped DF Columns: ", mapped_df.columns)
    try:
        mapped_df['state'] = mapped_df['city_state'].str.split(",").str[1]
    except:
        mapped_df['state'] = schema_mapper_dict[schema_id]["state"]

    mapped_df['state'] = mapped_df['state'].str.replace('.', '')
    mapped_df['state'] = mapped_df['state'].str.replace(' ', '')
    try:
        mapped_df['city'] = mapped_df['city_state'].str.split(",").str[0]
    except:
        mapped_df['city'] = ""

    mapped_df['city'] = mapped_df['city'].str.strip()

    mapped_df["mod_iv_munis_name"] = mapped_df["mun_code_id"].map(schema_mapper_dict[schema_id]["muni_map"])
    mapped_df['mod_iv_year'] = schema_mapper_dict[schema_id]["current_modiv_year"]

    mapped_df = mapped_df.drop('city_state', axis=1)

    df = pd.concat([df, mapped_df], ignore_index=True)

    
    return df

def address_verification(mapped_df):
        USERID = "329INSTR4397"
        revision = "1"
        usps_payload={}
        usps_headers = {}

        for index, row in mapped_df.iterrows():
            usps_address2 = str(row['property_location'])
            usps_address1 = ""
            usps_state = str(row['state'])
            usps_city = str(row['city'])
            usps_zip5 = str(row['zip_code'])
    
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
                address2 = str(row['PROPERTY_LOCATION'])
            try:
                state = dict_data['AddressValidateResponse']['Address']['State']
            except:
                state = "NJ"
            try:
                city = dict_data['AddressValidateResponse']['Address']['City']
            except:
                city = str(row['city'])
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
            mapped_df.at[index, 'property_location_hash_id'] = str(i)

        return mapped_df