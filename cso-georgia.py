#%%
import requests
import re
import json

#%%
org_types = ["ngo", "international", "platforms"]

reg_map = {
    1: "Abkhazia",
    2: "Samegrelo-Zemo Svaneti",
    3: "Racha-Lechkhumi",
    4: "Imereti",
    5: "Guria",
    6: "Ajara",
    7: "Mtskheta-Tianeti",
    8: "Shida-Kartli",
    9: "Samtskhe-Javakheti",
    10: "Kvemo-Kartli",
    11: "Kakheti",
    12: "Tbilisi",
}

out = []
for org_type in org_types:
    r = requests.get(f"https://csogeorgia.org/en/organizations/{org_type}")

    pattern = re.compile(r"var regions = (.*);")
    raw_string = pattern.findall(r.text)[0]
    d = json.loads(raw_string)

    for region in d:
        for org in region["organizations"]:
            org["type"] = org_type
            org["region"] = reg_map[org["region_id"]]
            out.append(org)

with open("cso-georgia.json", "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=4)
# %%
