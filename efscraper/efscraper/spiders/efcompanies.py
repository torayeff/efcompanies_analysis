import scrapy


class EFCompaniesSpider(scrapy.Spider):
    name = "efcompanies"

    start_urls = [
        "https://www.joinef.com/companies/"
    ]

    def parse(self, response):
        companies = response.css("div.company")
        for company in companies:
            company_name = company.css("div.company__name span::text").get()
            company_short_desc = company.css("div.company__description span::text").get()
            company_cat = company.css("div.company__cat span::text").get()

            detailbio = company.css("div.detailbio")
            founders_names = detailbio.css("span.detailbio__founders::text").getall()
            total_founders = len(founders_names)
            company_url = detailbio.css("div.detailbio__website a::attr(href)").get()

            excerpt = []
            for p in detailbio.css("div.margin--top p"):
                if len(p.css("::text")) != 0:
                    excerpt.append(p)

            company_long_desc = " ".join(excerpt[0].css("::text").getall())

            founders_info = []
            for p in excerpt[1:]:
                founders_info.append(" ".join(p.css("::text").getall()))

            yield {
                "company_name": company_name,
                "company_cat": company_cat,
                "company_url": company_url,
                "company_short_desc": company_short_desc,
                "company_long_desc": company_long_desc,
                "total_founders": total_founders,
                "founders_names": founders_names,
                "founders_info": founders_info
            }

        next_page = response.css("span.paging__link--next a::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
