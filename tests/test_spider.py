from eaj_scraper.spiders.ufrn_news import UfrnNewsSpider


def test_spider_configuration_is_polite():
    settings = UfrnNewsSpider.custom_settings or {}
    assert UfrnNewsSpider.allowed_domains == ["ufrn.br", "www.ufrn.br"]
    assert UfrnNewsSpider.start_urls[0].endswith("keyword=EAJ")
    assert "noticias-busca" in UfrnNewsSpider.api_url
    assert settings.get("CONCURRENT_REQUESTS", 1) <= 2
