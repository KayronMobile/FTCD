BOT_NAME = "eaj_scraper"

SPIDER_MODULES = ["eaj_scraper.spiders"]
NEWSPIDER_MODULE = "eaj_scraper.spiders"

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 2.0
RANDOMIZE_DOWNLOAD_DELAY = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
RETRY_ENABLED = True
RETRY_TIMES = 2
DOWNLOAD_TIMEOUT = 30

USER_AGENT = "projeto-eaj-academico/1.0 (contato: substitua-seu-email)"
FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    "data/noticias_eaj.csv": {
        "format": "csv",
        "overwrite": True,
        "encoding": "utf-8",
    }
}
