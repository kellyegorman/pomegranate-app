# was having errors with a few lines being read from data.csv so here is some cleaning logic
import pandas as pd
import csv

# read w/ more lenient settings
df = pd.read_csv(
    './chat/data.csv',
    quoting=csv.QUOTE_ALL,
    escapechar='\\',
    on_bad_lines='warn', 
    engine='python'
)

df.to_csv('./chat/data_fixed.csv', index=False, quoting=csv.QUOTE_ALL)
print(f"Fixed CSV saved with {len(df)} rows")