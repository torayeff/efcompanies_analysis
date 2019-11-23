import json

with open("companies_info.json", "r") as f:
    companies = json.load(f)

with open("companies_location.json", "r") as f:
    locations = json.load(f)

with open("companies_cohort.json", "r") as f:
    cohorts = json.load(f)

for company in companies:
    cname = company["company_name"]

    # add location
    for locs in locations:
        if cname == locs["company_name"]:
            company["company_location"] = locs["company_location"]

    for cohort in cohorts:
        if cname == cohort["company_name"]:
            company["company_cohort"] = cohort["company_cohort"]

with open("companies.json", "w") as f:
    json.dump(companies, f)
