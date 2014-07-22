#! /usr/bin/env python -u
# coding=utf-8
from time import sleep
import re
import traceback
import json
from nltk import OrderedDict
from selenium.webdriver.support import wait

__author__ = 'xl'

from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


def get_number(driver):
    if driver.page_source.find("did not match any documents.") >= 0:
        return 0
    try:
        text = driver.find_element_by_id("resultStats").text
        result = re.search("([\d,]*?) result", text).group(1)
        return int(result.replace(",", ""))
    except:
        return 0


def search_google(queries):
    driver = None
    try:
        # driver = webdriver.Remote(
        #     command_executor='http://127.0.0.1:4444/wd/hub',
        #     desired_capabilities=DesiredCapabilities.CHROME)
        # driver = webdriver.Chrome('./chromedriver', chrome_options=["--no-startup-window"])
        driver = WebDriver("./filtering/phantomjs")

        driver.get("http://www.google.com")
        w = wait.WebDriverWait(driver, 5)
        sleep(1)
        w.until(lambda x: driver.execute_script("return document.readyState;") == "complete")

        # elem = driver.find_elements_by_name("q")[0]
        # elem.click()
        # elem.send_keys(queries[0]["q"])
        # elem.send_keys(Keys.RETURN)
        # sleep(1)
        # w.until(lambda x: driver.execute_script("return document.readyState;") == "complete")
        # queries[0]["response"] = get_number(driver)

        for keyword in queries:
            elem = driver.find_elements_by_name("q")[0]
            elem.click()
            elem.clear()
            elem.send_keys(keyword["q"])
            elem.send_keys(Keys.RETURN)
            sleep(1)
            w.until(lambda x: driver.execute_script("return document.readyState;") == "complete")
            keyword["response"] = get_number(driver)
            driver.save_screenshot("%s.png" % keyword["pr"])
        # return ret

    except:
        traceback.print_exc()
        if driver:
            driver.save_screenshot("test.png")

    finally:
        if driver:
            driver.close()


def get_matrix(name):
    results = OrderedDict()
    with open("./filtering/PRs.json", "r") as fp:
        lines = json.load(fp)
    PRs = {}

    for line in lines:
        cat = line["cat"]
        if cat not in PRs:
            PRs[cat] = []
        PRs[cat].append(line)

    queries = []
    for pr in sorted(PRs):
        index = 0
        while index < len(PRs[pr]):
            q = {
                "pr": pr,
                "q": name + " " + " OR ".join(["site:%s" % (site["link"],) for site in PRs[pr][index:index + 10]])
            }
            queries.append(q)
            index += 10

    search_google(queries)
    for query in queries:
        pr = query['pr']
        results[pr] = query['response'] + results.get(pr, 0)

    for pr in results:
        results[pr] /= 1.0 * len(PRs[pr])

    return results


if __name__ == "__main__":
    print get_matrix("heartbleed")