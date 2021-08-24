#%%
import requests
import jsonlines
from math import ceil

# %%
url = "https://api.companyinfo.ge/api/corporations/"
search_url = url + "search"

params = {"legalForm": 7, "page": 1}

r = requests.get(search_url, params=params)
# %%
initial_request = r.json()
total_items = initial_request["totalItems"]
total_pages = ceil(total_items / initial_request["itemPerPage"])

out = []
for page in range(1, total_pages + 1):
    params["page"] = page
    r = requests.get(search_url, params=params)

    for item in r.json()["items"]:
        company_id = item["id"]
        company_request = requests.get(url + str(company_id))
        with jsonlines.open("companies.jsonl", mode="a") as f:
            f.write(company_request.json())


# %%
