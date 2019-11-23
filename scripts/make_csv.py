import json
import pandas as pd


with open("../data/companies.json", "r") as f:
    companies = json.load(f)

for company in companies:
    # clean founders info
    cleaned = []
    for finfo in company["founders_info"]:
        # remove names
        if len(finfo) > 30:
            cleaned.append(finfo)

    before = len(company["founders_info"])
    company["total_founders"] = len(company["founders"]) or len(cleaned)
    company["founders_info"] = cleaned

df = pd.DataFrame(data=companies, columns=list(companies[0].keys()))
df.to_csv("../data/companies.csv", index=False)
