import scrapy
import unicodedata


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
            company_url = detailbio.css("div.detailbio__website a::attr(href)").get()

            founders = detailbio.css("span.detailbio__founders::text").getall()

            # parse company and founders info
            txt = ""
            info = []
            for p in detailbio.css("div.margin--top p"):
                if p.css("strong").get() or p.css("b").get():
                    if len(txt) != 0:
                        info.append(txt)  # append previous
                    txt = ""
                txt += " ".join(p.css("::text").getall())
            info.append(txt)

            yield {
                "company_name": company_name,
                "company_cat": company_cat,
                "company_url": company_url,
                "company_short_desc": company_short_desc,
                "company_long_desc": info[0],
                "founders": founders,
                "founders_info": info[1:]
            }

        next_page = response.css("span.paging__link--next a::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
