# scrape_site.py

"""This module provides web scraper for the project"""
import requests
from bs4 import BeautifulSoup, SoupStrainer


def url_builder(category=None, sub_category=""):
    site_base = "https://www.facultyplus.com/category"
    site_link = "/".join([site_base, category, sub_category])
    return requests.get(site_link)


def get_results(page):
    result_only = SoupStrainer("div", class_="td-ss-main-content")
    soup = BeautifulSoup(page.content, "html.parser", parse_only=result_only)
    results = soup.find_all("div", class_=["td_module_16 td_module_wrap td-animation-stack td_module_no_thumb",
                                           "td_module_16 td_module_wrap td-animation-stack"])
    return results


def check_a_tag(tag):
    return tag.name == "a" and not tag.has_attr("class")


def parse_results(tag):
    a_tag = tag.find(check_a_tag)
    time_tag = tag.time
    return [a_tag["title"], str(time_tag.string), a_tag["href"]]


def create_dataset(page, file_name):
    with open(file_name, "w", encoding="UTF-8") as tsv:
        for tag in get_results(page):
            tsv.write("\t".join(parse_results(tag)))
            tsv.write("\n")


if __name__ == "__main__":
    page = url_builder("jobs-by-location", "tamilnadu")
    create_dataset(page, "jobs_by_loc.tsv")

    page = url_builder("arts-and-science")
    create_dataset(page, "jobs_by_category.tsv")

