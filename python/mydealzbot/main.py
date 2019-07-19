import logging
import sys

import mydealz_config
import telegram_bot
import mydealz_thread_db
import mydealz_main

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    config = mydealz_config.Config("data/mydealz_conf.json")
    thread_db = mydealz_thread_db.MydealzThreadDatabase() \
        if config.value("use_db") else None

    scrape_main = mydealz_main.MydealzScraperMain(config)
    articles_index = scrape_main.scrape_index()

    filter_main = mydealz_main.MydealzFilterMain(config, thread_db)
    filtered_index = filter_main.filter_index_articles(articles_index)

    message = mydealz_main.MydealzMessage()
    message.add_index(filtered_index["index"])
    message.add_look_for(filtered_index["look_for"])
    message.send_message()

    thread_db.insert_articles([a.id for a in filtered_index["index"]])

if __name__ == "__main__":
    main()
