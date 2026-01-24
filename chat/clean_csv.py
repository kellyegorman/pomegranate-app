import pandas as pd
import csv

# Read with more lenient settings
df = pd.read_csv(
    './chat/data.csv',
    quoting=csv.QUOTE_ALL,
    escapechar='\\',
    on_bad_lines='warn', 
    engine='python'
)

df.to_csv('./chat/data_fixed.csv', index=False, quoting=csv.QUOTE_ALL)
print(f"Fixed CSV saved with {len(df)} rows")