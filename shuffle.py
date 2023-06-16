import pandas as pd

# Shuffle the table rows
def shuffle_table(table):    
    df = pd.DataFrame(table)
    table = df.sample(frac=1)
    table = table.values.tolist()
    
    return table