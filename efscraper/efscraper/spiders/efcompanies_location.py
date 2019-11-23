import scrapy


class EFCompaniesSpider(scrapy.Spider):
    name = "efcompanies_location"

    start_urls = [
        "https://www.joinef.com/companies/location/berlin/",
        "https://www.joinef.com/companies/location/hong-kong/",
        "https://www.joinef.com/companies/location/london/",
        "https://www.joinef.com/companies/location/new-york/",
        "https://www.joinef.com/companies/location/paris/",
        "https://www.joinef.com/companies/location/singapore/"
    ]

    def parse(self, response):
        companies = response.css("div.company")
        for company in companies:
            company_name = company.css("div.company__name span::text").get()

            if "/page/" in response.url:
                company_location = response.url.split("/")[-4]
            else:
                company_location = response.url.split("/")[-2]

            yield {
                "company_name": company_name,
                "company_location": company_location
            }

        next_page = response.css("span.paging__link--next a::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
