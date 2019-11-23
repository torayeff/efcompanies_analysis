import scrapy


class EFCompaniesSpider(scrapy.Spider):
    name = "efcompanies_cohort"

    start_urls = ['https://www.joinef.com/companies/cohort/asia-4/',
                  'https://www.joinef.com/companies/cohort/ef1-london/',
                  'https://www.joinef.com/companies/cohort/ef2-london/',
                  'https://www.joinef.com/companies/cohort/ef3-london/',
                  'https://www.joinef.com/companies/cohort/ef4-london/',
                  'https://www.joinef.com/companies/cohort/ef5-london/',
                  'https://www.joinef.com/companies/cohort/ef6-london/',
                  'https://www.joinef.com/companies/cohort/ef7-london/',
                  'https://www.joinef.com/companies/cohort/ef8-london/',
                  'https://www.joinef.com/companies/cohort/ef9-london/',
                  'https://www.joinef.com/companies/cohort/efsg1-singapore/',
                  'https://www.joinef.com/companies/cohort/efsg2-singapore/',
                  'https://www.joinef.com/companies/cohort/efsg3-singapore/',
                  'https://www.joinef.com/companies/cohort/europe-10/',
                  'https://www.joinef.com/companies/cohort/europe-11/']

    def parse(self, response):
        companies = response.css("div.company")
        for company in companies:
            company_name = company.css("div.company__name span::text").get()

            if "/page/" in response.url:
                company_cohort = response.url.split("/")[-4]
            else:
                company_cohort = response.url.split("/")[-2]

            yield {
                "company_name": company_name,
                "company_cohort": company_cohort
            }

        next_page = response.css("span.paging__link--next a::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
