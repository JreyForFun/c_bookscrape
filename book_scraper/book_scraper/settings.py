BOT_NAME = "book_scraper"

SPIDER_MODULES = ["book_scraper.spiders"]
NEWSPIDER_MODULE = "book_scraper.spiders"

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 0.5

# enable all 3 pipelines
ITEM_PIPELINES = {
    "book_scraper.pipelines.SQLitePipeline":  100,
    "book_scraper.pipelines.MySQLPipeline":   200,
    "book_scraper.pipelines.MongoDBPipeline": 300,
}

# mysql settings
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "book_db"

# mongodb settings
MONGO_URI = "mongodb://localhost:27017"
MONGO_DATABASE = "book_db"

# sqlite settings
SQLITE_DB_PATH = "books.db"

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
