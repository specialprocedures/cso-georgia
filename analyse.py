#%%
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import jsonlines
from datetime import date

sns.set()


# %%

with jsonlines.open("companyinfo/items.json", "r") as f:
    lst = [obj for obj in f]


def parse_jsonl(lst):
    csos = []
    people = []
    for item in lst:
        corp = item["corporation"]

        corp_out = {}
        for field in ["name", "idCode", "address", "email"]:
            corp_out[field] = corp[field]

        if corp.get("registrationDate"):
            corp_out["registrationDate"] = corp["registrationDate"]["date"]
        csos.append(corp_out)

        affils = item["corporationAffiliations"]

        for affil in affils:
            affil["corpId"] = corp["idCode"]
            people.append(affil)

    return csos, people


# def extract_loc(x):
#     if isinstance(x, str):
#         try:
#             loc = x.split(",")[1]
#         except IndexError:
#             return x

#         loc = re.sub(r".\.|ქალაქი", "", loc).strip()
#         return loc


csos, people = [pd.DataFrame(i) for i in parse_jsonl(lst)]
# %%
csos["date"] = pd.to_datetime(csos["registrationDate"], errors="coerce")
#%%

# %%


fig, ax = plt.subplots(figsize=(15, 5))
to_plot = (
    csos.query("(date > 1990) and (date < 2021)")
    .groupby("date")["idCode"]
    .count()
    .resample("M")
    .sum()
    .rolling(3)
    .mean()
    .reset_index()
)
sns.lineplot(x="date", y="idCode", data=to_plot, ax=ax)

key_dates = [
    ("Civil Code\nof Georgia\n(1999)", date(1999, 1, 1), 150),
    ("Rose Revolution\n(2003)", date(2003, 11, 3), 155),
    ("Saakashvili\nDemonstrations\n(2007)", date(2007, 11, 1), 185),
    ("Parliamentary\nElections\n(2012)", date(2012, 10, 1), 185),
    ("Parliamentary\nElections\n(2016)", date(2016, 10, 1), 210),
]

for t, d, h in key_dates:
    ax.text(x=d, y=h, s=t, fontdict={"ha": "center"})


ax.xaxis.set_major_locator(mdates.YearLocator(base=5))
ax.set_xlim(date(1990, 1, 1), date(2021, 4, 1))
ax.set_ylim(0, 250)
ax.set_xlabel("")
ax.set_ylabel("New CSO registrations (monthly)")
plt.figtext(0.9, -0.02, "Source: Public Registry via companyinfo.ge", ha="right")
plt.savefig("registrations.png", bbox_inches="tight")
plt.show()
# %%

multi = people.drop_duplicates(subset=["personId", "corpId"])[
    "personName"
].value_counts()

# %%
adj = (
    csos[["idCode", "name", "email"]]
    .merge(
        people[["personName", "personId", "corpId"]],
        left_on="idCode",
        right_on="corpId",
    )
    .drop_duplicates()
)

adj = adj[adj.personName.isin(multi[multi > 1].index)]
nodes = (
    pd.concat(
        [
            pd.DataFrame(adj[["idCode", "name", "email"]].values).assign(type="org"),
            pd.DataFrame(adj[["personId", "personName"]].values).assign(type="person"),
        ],
        axis=0,
    )
    .rename(columns={0: "id", 1: "label", 2: "email"})
    .drop_duplicates(subset=["id"])
)

edges = adj[["idCode", "personId"]].rename(
    columns={"idCode": "source", "personId": "target"}
)

nodes.to_csv("nodes.csv", index=False)
edges.to_csv("edges.csv", index=False)
