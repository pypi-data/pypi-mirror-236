import pandas as pd
  
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





code =      """
            id = str(row['Block']) + str(row['Lot']) + str(row['Qual']) + str(row['Property Location'] + '2022')
            h = hashlib.new('sha256')
            arr = bytes(id, 'utf-8')
            h.update(arr)
            i = h.hexdigest()
            
            hash_id
            property_location_id #(token_id)
            
            prop_hash_id = str(row['Property Location']) + str('ORANGE CITY TWP') + str('NJ') + str('ESSEX') + str(row['Block']) + str(row['Lot']) + str(row['Qual'])
            x = hashlib.new('sha256')
            arr = bytes(prop_hash_id, 'utf-8')
            x.update(arr)
            j = x.hexdigest()
            
            property_location_hash_id

            #mod_iv_recordid
            #mod_iv_year
            #mun_code_id
            #mod_iv_county_name
            #mod_iv_munis_name
            #gis_pin
            #county_district
            property_id_blk = str(row['Block'])
            property_id_lot = str(row['Lot'])
            property_id_qualifier = str(row['Qual'])
            #qualification_code_name
            #record_id
            #sub_record_id
            #last_trans_date_MMDDYY
            #last_trans_update_number
            #tax_acct_number
            property_class = str(row['Property Class'])
            property_class_code_name = str(row['Property Class Name'])
            property_location = str(row['Property Location'])
            building_description = str(row['Building Desc'])
            land_description = str(row['Land Desc'])
            calculated_acreage = int(row['Sq. Ft.'])/43560
            #additional_lots_1
            #additional_lots_2
            #zoning
            #tax_map_page_number
            owner_name = str(row["Owner's Name"])
            owner_street_address = str(row['Street'])
            owner_city = str(row['City/State/Zip']).split(',')[0]
            owner_state = str(row['City/State/Zip']).split(',')[1]
            #owner_zip_code
            #owner_zip_code_plus_four
            #number_of_owners
            #deduction_amount
            #filler
            #bank_code
            #mortgage_account_number
            deed_book = str(row['Deed Book'])
            deed_page = str(row['Deed Page'])
            #sales_price_code
            
            try:
                date_and_time = str(row['Sale Date'])
                date_str = date_and_time.split(" ")[0]
                format_str = '%m/%d/%y' # The format
                datetime_obj = datetime.datetime.strptime(date_str, format_str)
                sale_date = datetime_obj.date()
                sale_date = "'" + str(sale_date) + "'"
            except:
                sale_date = "null"    
            sql = sql + str(sale_date) + ", " #deed_date_MMDDYY
            
            sale_price = str(row['Sale Price'])
            #sale_assessment
            sale_sr1a_non_usable_code = str(row['NU Code'])
            #number_of_dwellings
            #number_of_commercial_dwell
            #multiple_occupancy_code
            #percentage_owned_code
            #rebate_code
            #additional_rebate_code
            #delquency_code
            #epl_own
            #epl_own_name_of_owner
            #epl_use
            #epl_use_name
            #epl_description
            #epl_description_name
            #initial_date_MMDDYY
            #further_date_MMDDYY
            #statute_number
            #facility_name
            building_class_code = str(row['Building Class'])
            #building_class_code_dwelling_type
            building_class_code_class = str(row['Class 4 Code'])
            year_constructed = str(row['Yr. Built'])
            #assessment_code
            land_value = str(row['Land Assmnt'])
            improvement_value = str(row['Building Assmnt'])
            net_taxable_value = str(row['Total Assmnt'])
            #sptax_code_1
            #sptax_code_1_id
            #sptax_code_1_name
            #sptax_code_2
            #sptax_code_2_id
            #sptax_code_2_name
            #sptax_code_3
            #sptax_code_3_id
            #sptax_code_3_name
            #sptax_code_4
            #sptax_code_4_id
            #sptax_code_4_name
            #exemption_code_1
            #exemption_amount_1
            #exempt_code_1_name
            #exemption_code_2
            #exemption_amount_2
            #exempt_code_2_name
            #exemption_code_3
            #exemption_amount_3
            #exempt_code_3_name
            #exemption_code_4
            #exemption_amount_4
            #exempt_code_4_name
            #senior_citizen_count
            #veteran_count
            #widows_of_veterans_count
            #surviving_spouse_count
            #disable_person_count
            #user_field_1
            #user_field_2
            #old_property_id
            old_block = str(row['Prior Block'])
            old_lot = str(row['Prior Lot'])
            #old_qualifier
            #census_tract
            #census_block
            #property_use_code
            #property_use_code_name
            #property_flags
            #tenant_rebate_response_flg
            #tenant_rebate_base_year
            #tenant_rebate_base_yr_tax
            #tenant_rebate_base_yr_tax_text
            #tenant_rebate_base_yr_net_val
            #filler_1
            last_year_total_tax = str(row['Taxes 1'])
            #current_year_total_tax
            #school_tax_overage
            #taxes_non_municipal_half1
            #taxes_non_municipal_half1_text
            #taxes_non_municipal_half2
            #taxes_non_municipal_half2_text
            #taxes_municipal_half1
            #taxes_municipal_half1_text
            #taxes_municipal_half2
            #taxes_municipal_half2_text
            #taxes_non_municipal_half3
            #taxes_non_municipal_half3_text
            #taxes_municipal_half3
            #taxes_municipal_half3_text
            #taxes_bill_status_flag
            #taxes_estimated_qtr3_tax
            #prior_year_net_value
            #statement_of_state_aid_amt
            """