#%%

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# %%

# Read in
df = pd.read_json("cso-georgia.json")
#%%
# Remove branch offices, bit odd this but 'is None' ain't implemented
# NaN == NaN == False
df.query("branch == ''", inplace=True)
for col in ["id", "title"]:
    df.drop_duplicates(subset=col, inplace=True)

# %%
pd.to_datetime(df["year"].replace("", None)).value_counts().sort_index().plot.bar()
# %%
df["region"].value_counts()

# %%
