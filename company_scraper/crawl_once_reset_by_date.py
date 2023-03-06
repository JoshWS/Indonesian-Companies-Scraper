#!.venv/bin/python

import os

import fire
from scrapy.utils.project import data_path
from sqlitedict import SqliteDict


def reset_by_date(scraper_name, date_string, test=True):
    """
    Selectively remove request from the crawl_once database.
    date_string needs to in escaped quotes.
    \"2017-10-22\" removes all requests made after 2017-10-21
    \"2017-10\" Removes everything and including October 2017.
    \"2017\" Removes all request from 2017 and later.

    To get a list of scrapy scrapers type: scrapy list

    :param scraper_name: string
    :param date_string: string
    :param test: Bool
    :returns: None
    """
    path = data_path("crawl_once", createdir=False)
    dbpath = os.path.join(path, "%s.sqlite" % scraper_name)
    if test:
        print("Running in test mode.")
        print("To remove the requests set flag: --test=False")
    with SqliteDict(filename=dbpath, tablename="requests", autocommit=True) as mydict:
        count = 0
        for key, value in mydict.iteritems():
            if str(value) > str(date_string):
                print(f"Removed request:{key} with timestamp: {value}")
                if not test:
                    mydict.pop(key)
                count += 1
    if test:
        print(f"Total {count} requests.")
        print("Running in test mode.")
        print("To remove the requests set flag: --test=False")
    else:
        print(f"Removed {count} requests.")


def show_all(scraper_name):
    """
    List all the request for the given scraper in the crawl_once database.
    :param scraper_name: string
    """
    path = data_path("crawl_once", createdir=False)
    dbpath = os.path.join(path, "%s.sqlite" % scraper_name)
    with SqliteDict(filename=dbpath, tablename="requests", autocommit=True) as mydict:
        count = 0
        for key, value in mydict.iteritems():
            print(key, value)
            count += 1
    print(f"Total {count} requests.")


def main():
    fire.Fire({"reset": reset_by_date, "show": show_all})


if __name__ == "__main__":
    main()
