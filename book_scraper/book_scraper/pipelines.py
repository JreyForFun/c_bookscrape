import mysql.connector
import pymongo
import sqlite3

# ---- MySQL Pipeline ----
class MySQLPipeline:

    def open_spider(self, spider):
        try:
            self.conn = mysql.connector.connect(
                host=spider.settings.get("MYSQL_HOST", "localhost"),
                port=spider.settings.getint("MYSQL_PORT", 3306),
                user=spider.settings.get("MYSQL_USER", "root"),
                password=spider.settings.get("MYSQL_PASSWORD", ""),
                database=spider.settings.get("MYSQL_DATABASE", "book_db"),
            )
            self.cursor = self.conn.cursor()

            # create the table if it doesnt exist yet
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(512),
                    price DECIMAL(8,2),
                    availability VARCHAR(64),
                    rating TINYINT
                )
            """)
            self.conn.commit()
            print("MySQL connected!")
        except Exception as e:
            print(f"MySQL connection error: {e}")
            self.conn = None

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()
            print("MySQL connection closed.")

    def process_item(self, item, spider):
        if not self.conn:
            return item
        try:
            self.cursor.execute(
                "INSERT INTO books (title, price, availability, rating) VALUES (%s, %s, %s, %s)",
                (item["title"], item["price"], item["availability"], item["rating"])
            )
            self.conn.commit()
        except Exception as e:
            print(f"MySQL insert error: {e}")
        return item


# ---- MongoDB Pipeline ----
class MongoDBPipeline:

    def open_spider(self, spider):
        try:
            mongo_uri = spider.settings.get("MONGO_URI", "mongodb://localhost:27017")
            db_name = spider.settings.get("MONGO_DATABASE", "book_db")

            self.client = pymongo.MongoClient(mongo_uri)
            self.collection = self.client[db_name]["books"]
            print("MongoDB connected!")
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            self.collection = None

    def close_spider(self, spider):
        if hasattr(self, "client"):
            self.client.close()
            print("MongoDB connection closed.")

    def process_item(self, item, spider):
        if self.collection is None:
            return item
        try:
            self.collection.insert_one(dict(item))
        except Exception as e:
            print(f"MongoDB insert error: {e}")
        return item


# ---- SQLite Pipeline ----
class SQLitePipeline:

    def open_spider(self, spider):
        try:
            db_path = spider.settings.get("SQLITE_DB_PATH", "books.db")
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()

            # create table if it doesnt exist
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    price REAL,
                    availability TEXT,
                    rating INTEGER
                )
            """)
            self.conn.commit()
            print(f"SQLite ready at {db_path}")
        except Exception as e:
            print(f"SQLite error: {e}")
            self.conn = None

    def close_spider(self, spider):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("SQLite connection closed.")

    def process_item(self, item, spider):
        if not self.conn:
            return item
        try:
            self.cursor.execute(
                "INSERT INTO books (title, price, availability, rating) VALUES (?, ?, ?, ?)",
                (item["title"], item["price"], item["availability"], item["rating"])
            )
            self.conn.commit()
        except Exception as e:
            print(f"SQLite insert error: {e}")
        return item
