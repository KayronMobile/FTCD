from datetime import datetime, timezone
from urllib.parse import urljoin

import scrapy

from eaj_scraper.items import NewsItem


class UfrnNewsSpider(scrapy.Spider):
    name = "ufrn_news"
    allowed_domains = ["ufrn.br", "www.ufrn.br"]
    start_urls = [
        "https://www.ufrn.br/imprensa/noticias/filtros?keyword=EAJ"
    ]
    api_url = (
        "https://webcache01-producao.info.ufrn.br/admin/portal-ufrn/"
        "wp-json/wp/v2/noticias-busca/"
    )

    def parse(self, response):
        yield scrapy.Request(
            f"{self.api_url}?_embed&per_page=10&page=1&tags=EAJ",
            callback=self.parse_api,
            cb_kwargs={"page": 1},
            headers={"Accept": "application/json"},
        )

    def parse_api(self, response, page):
        for article in response.json():
            timestamp = article.get("acf", {}).get("data_de_publicacao")
            if not timestamp:
                timestamp = article.get("date")

            if isinstance(timestamp, str) and timestamp.isdigit():
                timestamp = int(timestamp)

            if isinstance(timestamp, str):
                year = int(timestamp[:4])
            else:
                year = datetime.fromtimestamp(timestamp, tz=timezone.utc).year

            yield NewsItem(
                titulo=article["title"]["rendered"].strip(),
                ano=year,
                url=urljoin(
                    "https://www.ufrn.br/",
                    f"imprensa/noticias/{article['id']}/{article['slug']}",
                ),
            )

        total_pages = int(response.headers.get("X-WP-TotalPages", 1))
        if page < total_pages:
            yield scrapy.Request(
                f"{self.api_url}?_embed&per_page=10&page={page + 1}&tags=EAJ",
                callback=self.parse_api,
                cb_kwargs={"page": page + 1},
                headers={"Accept": "application/json"},
            )
