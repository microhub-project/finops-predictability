import pandas as pd

def filter_days(original_file, final_file):
    df = pd.read_csv(original_file, delimiter=';')

    new_df = df[df['infra_multiplier'] > 1.29]

    new_df.to_csv(final_file, sep=';', index=False)
    
def group_months():
    df = pd.read_csv('yearly-data.csv', delimiter=';')

    monthly_summary = round((df.groupby('month', as_index=False)[
        'infra_multiplier'
    ].max()), 2)

    monthly_summary.to_csv('monthly-data.csv', sep=';', index=False)