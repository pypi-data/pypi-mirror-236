#inputs: reverified sxt table and verified df from bucket

import pandas as pd

def merge(raw_df, sxt_df):
    merged_df = pd.merge(raw_df,sxt_df, how='left',left_on="hash_id", right_on="new_hash_id")
    return merged_df


def mapped(merged_df):
    mapped_values = merged_df[merged_df['new_hash_id'].notnull()]
    return mapped_values

def unmapped(merged_df):
    unmapped_values = merged_df[merged_df['new_hash_id'].isnull()]
    return unmapped_values