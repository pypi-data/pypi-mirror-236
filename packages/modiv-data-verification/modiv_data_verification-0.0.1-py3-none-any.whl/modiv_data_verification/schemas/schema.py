import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import InListValidation


schema_dict = {"001": Schema([
            Column('BLOCK', [InListValidation(['int'])], allow_empty=True),
            Column('LOT', [InListValidation(['int'])], allow_empty=True),
            Column('QUALIFIER', [InListValidation(['float'])], allow_empty=True),
            Column('CARD', [InListValidation(['int'])], allow_empty=True),
            Column('PROPERTY_CCDD', [InListValidation(['int'])], allow_empty=True),
            Column('PROPERTY_LOCATION', [InListValidation(['str'])], allow_empty=True),
            Column('PROPERTY_CLASS', [InListValidation(['str'])], allow_empty=True),
            Column('OWNER_ADDRESS', [InListValidation(['str'])], allow_empty=True),
            Column('OWNER_CITYSTATE', [InListValidation(['str'])], allow_empty=True),
            Column('OWNER_ZIP', [InListValidation(['int'])], allow_empty=True),
            Column('VALUES_IMPROVTAXABLEVALUE', [InListValidation(['int'])], allow_empty=True),
            Column('VALUES_LANDTAXABLEVALUE', [InListValidation(['int'])], allow_empty=True),
            Column('VALUES_NETTAXABLEVALUE', [InListValidation(['int'])], allow_empty=True),
            Column('EXEMPTION_AMOUNT_1', [InListValidation(['int'])], allow_empty=True),
            Column('EXEMPTION_AMOUNT_2', [InListValidation(['int'])], allow_empty=True),
            Column('EXEMPTION_AMOUNT_3', [InListValidation(['int'])], allow_empty=True),
            Column('EXEMPTION_AMOUNT_4', [InListValidation(['int'])], allow_empty=True),
            Column('NUMBER_BUILDINGSF', [InListValidation(['int'])], allow_empty=True),
            Column('PROPERTY_CONSTRUCTIONYEAR', [InListValidation(['int'])], allow_empty=True),
            Column('PROPERTY_BUILDINGCLASS', [InListValidation(['float'])], allow_empty=True),
            Column('OLD_OLDBLOCK', [InListValidation(['float'])], allow_empty=True),
            Column('OLD_OLDLOT', [InListValidation(['float'])], allow_empty=True),
            Column('OLD_OLDQUALIFIER', [InListValidation(['float'])], allow_empty=True),
            Column('NONE_LASTTRANSACTIONDT', [InListValidation(['str'])], allow_empty=True),
            Column('PROPERTY_ZONING', [InListValidation(['str'])], allow_empty=True),
            Column('PROPERTY_TAXACCOUNT', [InListValidation(['float'])], allow_empty=True),
            Column('OWNER_MORTGAGEACCOUNT', [InListValidation(['float'])], allow_empty=True),
            Column('OWNER_BILLINGCODE', [InListValidation(['int'])], allow_empty=True),
            Column('EXEMPT_SPECIALTAXCODE_1', [InListValidation(['float'])], allow_empty=True), 
            Column('EXEMPT_SPECIALTAXCODE_2', [InListValidation(['float'])], allow_empty=True),
            Column('EXEMPT_SPECIALTAXCODE_3', [InListValidation(['float'])], allow_empty=True),
            Column('EXEMPT_SPECIALTAXCODE_4', [InListValidation(['float'])], allow_empty=True),
            Column('CUSTOM_ACREAGE_2DECIMALS', [InListValidation(['float'])], allow_empty=True),
            Column('TAXMAP_NUMERIC', [InListValidation(['float'])], allow_empty=True),
            Column('PROPERTY_ADDITIONALLOT1', [InListValidation(['float'])], allow_empty=True),
            Column('PROPERTY_ADDITIONALLOT2', [InListValidation(['float'])], allow_empty=True),
            Column('PROPERTY_LANDDIMENSION', [InListValidation(['str'])], allow_empty=True),
            Column('PROPERTY_BUILDINGDESCRIPTION', [InListValidation(['str'])], allow_empty=True),
            Column('PROPERTY_CLASS4USECODE', [InListValidation(['float'])], allow_empty=True), 
            Column('PROPERTY_ACREAGE', [InListValidation(['int'])], allow_empty=True),
            Column('EXEMPT_OWNERSHIP', [InListValidation(['int'])], allow_empty=True),
            Column('EXEMPT_PURPOSE', [InListValidation(['int'])], allow_empty=True),
            Column('EXEMPT_DESCRIPTION', [InListValidation(['int'])], allow_empty=True),
            Column('EXEMPT_STATUTE', [InListValidation(['float'])], allow_empty=True),
            Column('EXEMPT_INITIALFILINGDATE', [InListValidation(['float'])], allow_empty=True),
            Column('EXEMPT_FURTHERFILINGDATE', [InListValidation(['float'])], allow_empty=True),
            Column('EXEMPT_FACILITYNAME', [InListValidation(['float'])], allow_empty=True),
            Column('CUSTOM_20_TAX_PRIORYRNETTAX_2DECIMALS', [InListValidation(['float'])], allow_empty=True),
            Column('CURRENTSALE_DATE', [InListValidation(['str'])], allow_empty=True),
            Column('CURRENTSALE_DEEDBOOK', [InListValidation(['float'])], allow_empty=True),
            Column('CURRENTSALE_DEEDPAGE', [InListValidation(['float'])], allow_empty=True),
            Column('CURRENTSALE_PRICE', [InListValidation(['int'])], allow_empty=True),
            Column('CURRENTSALE_NUC ', [InListValidation(['float'])], allow_empty=True)
            ]),
            "002": Schema([
            Column('MICROSYSTEM NAME', [InListValidation(['str'])]),
            Column('Municipality', [InListValidation(['str'])]),
            Column('City', [InListValidation(['str'])]),
            Column('State', [InListValidation(['str'])]),
            Column('Block', [InListValidation(['int'])]),
            Column('Lot', [InListValidation(['int'])]),
            Column('Qual', [InListValidation(['str'])]),
            Column('Property Location', [InListValidation(['str'])]),
            Column('Property Class', [InListValidation(['str'])]),
            Column('Property Class Name', [InListValidation(['str'])]),
            Column("Owner's Name", [InListValidation(['str'])]),
            Column("Owner's Mailing Address", [InListValidation(['str'])]),
            Column('City/State/Zip', [InListValidation(['str'])]),
            Column('Sq. Ft.', [InListValidation(['float', 'int'])]),
            Column('Yr. Built', [InListValidation(['int'])]),
            Column('Building Class', [InListValidation(['str'])]),
            Column('Prior Block', [InListValidation(['int', 'float'])]),
            Column('Prior Lot', [InListValidation(['int', 'float'])]),
            Column('Prior Qual', [InListValidation(['str'])]),
            Column('Updated', [InListValidation(['str'])]),
            Column('Zone', [InListValidation(['str'])]),
            Column('Account', [InListValidation(['str'])]),
            Column('Mortgage Account', [InListValidation(['str'])]),
            Column('Bank Code', [InListValidation(['str'])]),
            Column('Sp Tax Cd', [InListValidation(['str'])]),
            Column('Sp Tax Cd.1', [InListValidation(['str'])]),
            Column('Sp Tax Cd.2', [InListValidation(['str'])]),
            Column('Sp Tax Cd.3', [InListValidation(['str'])]),
            Column('Map Page', [InListValidation(['float', 'int'])]),
            Column('Additional Lots', [InListValidation(['str'])]),
            Column('Land Desc', [InListValidation(['str'])]),
            Column('Building Desc', [InListValidation(['str'])]),
            Column('Class 4 Code', [InListValidation(['str'])]),
            Column('Acreage', [InListValidation(['float', 'int'])]),
            Column('EPL Own', [InListValidation(['str'])]),
            Column('EPL Use', [InListValidation(['str'])]),
            Column('EPL Desc', [InListValidation(['str'])]),
            Column('EPL Statute', [InListValidation(['str'])]),
            Column('EPL Init', [InListValidation(['str'])]),
            Column('EPL Further', [InListValidation(['str'])]),
            Column('EPL Facility Name', [InListValidation(['str'])]),
            Column('Taxes 1', [InListValidation(['float', 'int'])]),
            Column('Taxes 2', [InListValidation(['float', 'int'])]),
            Column('Taxes 3', [InListValidation(['float', 'int'])]),
            Column('Taxes 4', [InListValidation(['float', 'int'])]),
            Column('Sale Date', [InListValidation(['str'])]),
            Column('Deed Book', [InListValidation(['int'])]),
            Column('Deed Page', [InListValidation(['float', 'int'])]),
            Column('Sale Price', [InListValidation(['float', 'int'])]),
            Column('NU Code', [InListValidation(['str'])]),
            Column('Ratio', [InListValidation(['str'])]),
            Column('Type/Use', [InListValidation(['str'])]),
            Column('Year', [InListValidation(['int'])]),
            Column('Owner', [InListValidation(['str'])]),
            Column('Street', [InListValidation(['str'])]),
            Column('City/State/Zip.1', [InListValidation(['str'])]),
            Column('Land Assmnt', [InListValidation(['float', 'int'])]),
            Column('Building Assmnt', [InListValidation(['float', 'int'])]),
            Column('Exempt', [InListValidation(['float', 'int'])]),
            Column('Total Assmnt', [InListValidation(['float', 'int'])]),
            Column('Assessed', [InListValidation(['float', 'int'])]),
            Column('Year.1', [InListValidation(['int'])]),
            Column('Owner.1', [InListValidation(['str'])]),
            Column('Street.1', [InListValidation(['str'])]),
            Column('City/State/Zip.2', [InListValidation(['str'])]),
            Column('Land Assmnt.1', [InListValidation(['float', 'int'])]),
            Column('Building Assmnt.1', [InListValidation(['float', 'str'])]),
            Column('Exempt.1', [InListValidation(['float', 'int'])]),
            Column('Total Assmnt.1', [InListValidation(['float', 'int'])]),
            Column('Assessed.1', [InListValidation(['float', 'int'])]),
            Column('Year.2', [InListValidation(['int'])]),
            Column('Owner.2', [InListValidation(['str'])]),
            Column('Street.2', [InListValidation(['str'])]),
            Column('City/State/Zip.3', [InListValidation(['str'])]),
            Column('Land Assmnt.2', [InListValidation(['float', 'int'])]),
            Column('Building Assmnt.2', [InListValidation(['float', 'int'])]),
            Column('Exempt.2', [InListValidation(['float', 'int'])]),
            Column('Total Assmnt.2', [InListValidation(['float', 'int'])]),
            Column('Assessed.2', [InListValidation(['float', 'int'])]),
            Column('Year.3', [InListValidation(['int'])]),
            Column('Owner.3', [InListValidation(['str'])]),
            Column('Street.3', [InListValidation(['str'])]),
            Column('City/State/Zip.4', [InListValidation(['str'])]),
            Column('Land Assmnt.3', [InListValidation(['float', 'int'])]),
            Column('Building Assmnt.3', [InListValidation(['float', 'int'])]),
            Column('Exempt.3', [InListValidation(['float', 'int'])]),
            Column('Total Assmnt.3', [InListValidation(['float', 'int'])]),
            Column('Assessed.3', [InListValidation(['float', 'int'])]),
            Column('Latitude', [InListValidation(['float', 'int'])]),
            Column('Longitude', [InListValidation(['float', 'int'])]),
            Column('Neigh', [InListValidation(['str'])]),
            Column('VCS', [InListValidation(['str'])]),
            Column('StyDesc', [InListValidation(['str'])]),
            Column('Style', [InListValidation(['str'])]),
            Column('Make a Payment URL', [InListValidation(['str'])]),
            Column('VACANT and ABANDONED', [InListValidation(['str'])]),
            Column('Transaction Hash', [InListValidation(['str'])]),
            Column('Transaction Hash URL', [InListValidation(['str'])])
            ])}

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




#schema_mapper_dict = {"001":{"state":"NJ", "unstack":False, "schema_map":schema001_map, "muni_map":nj_mun_map},
#                      "002":{"state":"NJ", "unstack":False, "schema_map":schema002_map, "muni_map":nj_mun_map}}

schema_mapper_dict = {"001":{"state":"NJ", "unstack":False, "muni_map":nj_mun_map},
                      "002":{"state":"NJ", "unstack":False, "muni_map":nj_mun_map}}


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

class Schema():
    def __init__(self, schema_id, year, county):
        self.schema_id = schema_id
        self.year = year
        self.county = county

    def validate_dataframe_schema(self, csv_file):
        df = pd.read_csv(csv_file)
        validate_schema = schema_dict[self.schema_id]
        errors = validate_schema.validate(df)
        #for error in errors:
        #    print(error)
        #if not errors:
        #    return True
        #else:
        #    return False
        df['county'] = self.county
        df['year'] = str(self.year)
        return df, True

    def schema_mapper(self, validated_data):
        df = pd.DataFrame(columns=columns)
        #print("Empty DF Columns: ", df.columns)
        #print("Source Data Columns: ", source_data.columns)
        schema_mapper_dict[self.schema_id]["mod_iv_year"] = str(self.year)
        validated_data.rename(schema_mapper_dict[self.schema_id]["schema_map"], axis=1, inplace=True)
        #print(mapped_df.head())
        #print("Mapped DF Columns: ", mapped_df.columns)
        try:
            validated_data['state'] = validated_data['city_state'].str.split(",").str[1]
        except:
            validated_data['state'] = schema_mapper_dict[schema_id]["state"]

        validated_data['state'] = validated_data['state'].str.replace('.', '')
        validated_data['state'] = validated_data['state'].str.replace(' ', '')
        try:
            validated_data['city'] = validated_data['city_state'].str.split(",").str[0]
        except:
            validated_data['city'] = ""

        validated_data['city'] = validated_data['city'].str.strip()

        validated_data["mod_iv_munis_name"] = validated_data["mun_code_id"].map(schema_mapper_dict[schema_id]["muni_map"])
        validated_data['mod_iv_year'] = schema_mapper_dict[schema_id]["current_modiv_year"]

        validated_data = validated_data.drop('city_state', axis=1)

        df = pd.concat([df, validated_data], ignore_index=True)

        
        return df


    def map_columns(host_path, schema_id):
        columns=['hash_id','property_location_id','property_location_hash_id', 'mod_iv_recordid',
                                      'mod_iv_year','mun_code_id','mod_iv_county_name','mod_iv_munis_name','gis_pin','county_district',
                                      'property_id_blk','property_id_lot','property_id_qualifier','qualification_code_name',
                                      'record_id','sub_record_id','last_trans_date_MMDDYY','last_trans_update_number',
                                      'tax_acct_number','property_class','property_class_code_name','property_location',
                                      'bulding_description','land_description','calculated_acreage','additional_lots_1',
                                      'additional_lots_2','zoning','tax_map_page_number','owner_name','owner_street_address',
                                      'owner_city','owner_state','owner_zip_code','owner_zip_code_plus_four',
                                      'number_of_owners','deduction_amount','filler','bank_code','mortgage_account_number',
                                      'deed_book','deed_page','sales_price_code','deed_date_MMDDYY','sale_price',
                                      'sale_assessment','sale_sr1a_non_usable_code','number_of_dwellings','number_of_commercial_dwell',
                                      'multiple_occupancy_code','percentage_owned_code','percentage_owned_code',
                                      'rebate_code','additional_rebate_code','delquuncy_code','epl_own','epl_own_name_of_owner',
                                      'epl_use','epl_use_name','epl_description','epl_description_name','inital_date_MMDDYY',
                                      'further_date_MMDDYY','statute_number','facility_name','building_class_code',
                                      'building_class_code_dwelling_type','building_class_code_class','year_constructed',
                                      'assessment_code','land_value','improvement_value','net_taxable_value',
                                      'sptax_code_1','sptax_code_1_id','sptax_code_1_name',
                                      'sptax_code_2','sptax_code_2_id','sptax_code_2_name',
                                      'sptax_code_3','sptax_code_3_id','sptax_code_3_name',
                                      'sptax_code_4','sptax_code_4_id','sptax_code_4_name',
                                      'exemption_code_1','exemption_amount_1','exempt_code_1_name',
                                      'exemption_code_2','exemption_amount_2','exempt_code_2_name',
                                      'exemption_code_3','exemption_amount_3','exempt_code_3_name',
                                      'exemption_code_4','exemption_amount_4','exempt_code_4_name',
                                      'senior_citizen_count','veteran_count','widows_of_veterans_count',
                                      'surviving_spouse_count','disable_person_count','user_field_1',
                                      'user_field_2','old_property_id','old_block','old_lot','old_qualifier',
                                      'census_tract','census_block','property_use_code','property_use_code_name',
                                      'property_flags','tenant_rebate_response_flg','tenant_rebate_base_year',
                                      'tenant_rebate_base_yr_tax','tenant_base_yr_tax_text','tenant_rebate_base_yr_net_val',
                                      'filler_1','last_year_total_tax','current_year_total_tax','school_year_overage',
                                      'taxes_non_municipal_half1','taxes_non_municipal_half1_test','taxes_non_municipal_half2',
                                      'taxes_non_municipal_half2_text','taxes_municipal_half1','taxes_municipal_half1_text',
                                      'taxes_municipal_half2','taxes_municipal_half2_text','taxes_non_municipal_half3',
                                      'taxes_non_municipal_half3_text','taxes_municipal_half3','taxes_municipal_half3_text',
                                      'taxes_bill_status_flag','taxes_estimated_qtr3_tax','prior_year_net_value'
                                      'statement_of_state_aid_amt','City','State']         


        if schema_id == "001":
        column_map = {'BLOCK':'property_id_blk', 'LOT':'property_id_lot', 'QUALIFIER':'property_id_qualifier', 'PROPERTY_CCDD':'mun_code_id',
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
    
    elif schema_id == "002":
        df = pd.read_csv(host_path)
        df['Owner City'] = [str(x).split(',')[-0] for x in df['City/State/Zip.1']]
        df['Owner State'] = [str(x).split(',')[-1] for x in df['City/State/Zip.1']]
        #df['Square Feet'] = [int(x)/43560 for x in df['Sq. Ft.']]
        #df['Square Feet']=df[['Sq. Ft.']].apply(pd.to_numeric,errors='coerce').fillna(0).eval(df['Sq. Ft.']/43560)
        #df['Square Feet']=df[['Sq. Ft.']].apply(lambda x: x/43560).fillna(0)
        
        df['Sq. Ft.'] = pd.to_numeric(df['Sq. Ft.'], errors='coerce').astype('Int64').fillna(0)
        df['Square Feet'] = [int(x)/43560 for x in df['Sq. Ft.']]
        
        df = df.drop(columns=['City/State/Zip', 'Sq. Ft.', 'City/State/Zip.1'])
        column_map = {'hash_id':'hash_id','property_loaction_id':'property_location_id','property_location_hash_id':'property_location_hash_id',
                        'Block':'property_id_blk','Lot':'property_id_lot','Qual':'property_id_qualifier',
                        'Property Class':'property_class','Property Class Name':'property_class_code_name',
                        'Property Location':'property_location','Building Desc':'building_description',
                        'Land Desc':'land_description','Square Feet':'calculated_acreage',"Owner's Name":'owner_name',
                        'Street':'owner_street_address','Owner City':'owner city','Owner State':'owner state',
                        'Deed Book':'deed_book','Deed Page':'deed_page','Sale Date':'sale_date','Sale Price':'sale_price',
                        'NU Code':'sale_sr1a_non_usable_code','Building Class':'building_class_code',
                        'Class 4 Code':'building_class_code_class','Yr. Built':'year_constructed',
                        'Land Assmnt':'land_value','Building Assmnt':'improvment_value','Total Assmnt':'net_taxable_value',
                        'Prior Block':'old_block','Prior Lot':'old_lot', 'Prior Qual':'old_qualifier','Taxes 1':'last_year_total_tax','year':'mod_iv_year','county':'mod_iv_county_name'}

        df = df.rename(columns=column_map)
        
        df = df.drop(columns=['MICROSYSTEM NAME','Municipality',"Owner's Mailing Address",'Updated','Zone','Account','Mortgage Account','Bank Code','Sp Tax Cd','Sp Tax Cd.1','Sp Tax Cd.2','Sp Tax Cd.3','Map Page','Additional Lots','Acreage','EPL Own','EPL Use','EPL Desc','EPL Statute','EPL Init','EPL Further','EPL Facility Name','Taxes 2','Taxes 3','Taxes 4','Ratio','Type/Use','Year','Owner','Exempt','Assessed','Year.1','Owner.1','Street.1','City/State/Zip.2','Land Assmnt.1','Building Assmnt.1','Exempt.1','Total Assmnt.1','Assessed.1','Year.2','Owner.2','Street.2','City/State/Zip.3','Land Assmnt.2','Building Assmnt.2','Exempt.2','Total Assmnt.2','Assessed.2','Year.3','Owner.3','Street.3','City/State/Zip.4','Land Assmnt.3','Building Assmnt.3','Exempt.3','Total Assmnt.3','Assessed.3','Latitude','Longitude','Neigh','VCS','StyDesc','Style','Join','Make a Payment URL','VACANT and ABANDONED ', 'Transaction Hash ','Transaction Hash URL'])

        for column in columns:
            if column not in df.columns:
                df[column]=None
        return df
