import requests
from bs4 import BeautifulSoup
import regex as re
import json

__SUB_GROWTH_REGEX = "(?<=element: 'subscriber-growth',.*data: \[)(.+?)(?=\])"
__TOTAL_SUB_REGEX = "(?<=element: 'total-subscribers',.*data: \[)(.+?)(?=\])"
__RANK_REGEX = "(?<=rankData.*\[)(.+?)(?=\])"
__NEW_REDDITS_BY_DAY_REGEX = "(?<=element: 'new-reddits-by-day',.*data: \[)(.+?)(?=\])"
__TOTAL_SUBREDDITS_BY_DAY_REGEX = "(?<=element: 'total-subreddits',.*data: \[)(.+?)(?=\])"

# ==========================================================
# HELPERS
# ==========================================================


# search by regex and deserialize into json
def __search_by_regex_and_deserialize(regexp, soup):
    regex_match = re.search(regexp, soup).group(0).replace(" ", "")
    jsonized_regex_match = regex_match.replace("'", '"').replace(
        "y", '"y"').replace("a", '"a"')
    return json.loads("[{}]".format(jsonized_regex_match))


# less messy way of generating a subreddit specific url
def __format_subreddit_url(subreddit):
    return "https://redditmetrics.com/r/{}".format(subreddit)


# get soup of given url
def __get_soup(url):
    return BeautifulSoup(requests.get(url).text, "lxml")


# extract <script> tags
def __get_script_soup(subreddit):
    soup = __get_soup(__format_subreddit_url(subreddit))
    return str.join(" ", str(soup.find_all("script")).splitlines())


# get ranking table on the subreddit page
def __get_subreddit_ranking_table(subreddit):
    soup = __get_soup(__format_subreddit_url(subreddit))
    table = soup.find_all(
        "table", {"class": "ranking-table"})
    [ranks] = [x.find_all("h2", {"class": "rank"}) for x in table]
    return ranks


# getting data from the homepage table
def __get_from_table(url, table_id, time):
    soup = __get_soup(url)
    table = soup.find_all(
        "table", {"class": "table table-bordered"})[table_id]
    table_trs = table.find_all("tr")

    subreddit_names = []
    subreddit_scores = []
    for tr in table_trs:
        for td in tr.find_all("td", {"class": time}):
            anchor = td.find("a")
            span = td.find("span")
            if anchor is not None:
                subreddit_names.append(anchor.text.strip())
            if span is not None:
                subreddit_scores.append(span.text.strip())

    data_dict = dict(zip(subreddit_names, subreddit_scores))

    indexed_dict = {}
    for idx, key in enumerate(data_dict):
        indexed_dict[idx + 1] = {key, data_dict[key]}

    return indexed_dict

# ==========================================================
# SUBREDDIT-SPECIFIC METHODS
# ==========================================================

def subreddit_get_subscriber_growth_data(subreddit):
    return __search_by_regex_and_deserialize(__SUB_GROWTH_REGEX,
                                             __get_script_soup(subreddit))


def subreddit_get_total_subscriber_data(subreddit):
    return __search_by_regex_and_deserialize(__TOTAL_SUB_REGEX,
                                             __get_script_soup(subreddit))


def subreddit_get_rank_data(subreddit):
    return __search_by_regex_and_deserialize(__RANK_REGEX,
                                             __get_script_soup(subreddit))


def subreddit_get_current_subscribers(subreddit):
    return __get_subreddit_ranking_table(subreddit)[0].text


def subreddit_get_current_rank(subreddit):
    return __get_subreddit_ranking_table(subreddit)[1].text

# ==========================================================
# GENERAL METHODS
# ==========================================================


def get_fastest_growing_today():
    return __get_from_table("https://redditmetrics.com/", 0, "tod")


def get_fastest_growing_week():
    return __get_from_table("https://redditmetrics.com/", 0, "week")


def get_fastest_growing_month():
    return __get_from_table("https://redditmetrics.com/", 0, "moth")


def get_non_default_reddits_today():
    return __get_from_table("https://redditmetrics.com/", 1, "tod")


def get_non_default_reddits_week():
    return __get_from_table("https://redditmetrics.com/", 1, "week")


def get_non_default_reddits_month():
    return __get_from_table("https://redditmetrics.com/", 1, "moth")


def get_top_new_reddits_today():
    return __get_from_table("https://redditmetrics.com/", 2, "tod")


def get_top_new_reddits_week():
    return __get_from_table("https://redditmetrics.com/", 2, "week")


def get_top_new_reddits_month():
    return __get_from_table("https://redditmetrics.com/", 2, "moth")


def get_new_reddits_trending_month():
    return __get_from_table("https://redditmetrics.com/", 3, "tod")


def get_new_reddits_trending_3_months():
    return __get_from_table("https://redditmetrics.com/", 3, "week")


def get_new_reddits_trending_6_months():
    return __get_from_table("https://redditmetrics.com/", 3, "moth")


def get_top_n_reddits(n):
    # get the first page (/top), which contains the top 100 subreddits
    subreddit_names = []
    subreddit_subscribers = []

    soup = __get_soup("https://redditmetrics.com/top")
    table = soup.find_all(
        "table", {"class": "table table-bordered"})[0]
    table_trs = table.find_all("tr")
    for tr in table_trs:
        for td in tr.find_all("td"):
            for anchor in td.find_all("a"):
                subreddit_names.append(anchor.text)
        for td in tr.find_all("td")[2:]:
            subreddit_subscribers.append(td.text)

    # if the offset is > 100, continue with the offset algo
    if n > 100:
        mod_n = n % 100
        how_many_times_100 = int(n/100)

        offsets = [100] * how_many_times_100 + [mod_n]

        last_offset = 0
        for offset in offsets:
            soup = __get_soup(
                "https://redditmetrics.com/top/offset/{}".format(last_offset + offset))
            table = soup.find_all(
                "table", {"class": "table table-bordered"})[0]
            table_trs = table.find_all("tr")

            for tr in table_trs:
                for td in tr.find_all("td"):
                    for anchor in td.find_all("a"):
                        subreddit_names.append(anchor.text)
                for td in tr.find_all("td")[2:]:
                    subreddit_subscribers.append(td.text)
            last_offset += offset

    clean_subreddit_subscribers = [
        x for x in subreddit_subscribers if x.replace(",", "").isdigit()]

    data_dict = dict(zip(subreddit_names, clean_subreddit_subscribers))

    indexed_dict = {}
    for idx, key in enumerate(data_dict):
        if idx <= n:
            indexed_dict[idx] = {key, data_dict[key]}
        else:
            break

    return indexed_dict

