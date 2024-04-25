"""A pipeline to extract data from the Mumsnet 'Am I Being Unreasonable' board."""

from os import environ as ENV
from time import sleep
from csv import DictWriter

from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup
from bs4.element import Tag


def scrape_page(url: str) -> BeautifulSoup:
    """Returns a soup object from a URL."""
    res = req.get(url, timeout=5)
    if 200 <= res.status_code < 300:
        soup = BeautifulSoup(res.text, features="html.parser")
        return soup
    raise ValueError("Invalid URL.")


def get_user_data(question: Tag) -> dict:
    """Extracts user data from a question object."""
    user = question.find("div", class_="s-user-card--link")
    user_link = user.find("a")
    
    return {
        "name": user.get_text() if not user_link else user_link.get_text(),
        "link": user_link["href"] if user_link else None
    }


def get_post_tags(question: BeautifulSoup) -> list[str]:
    """Return a list of tag names from a question object."""
    tag_element = question.find("div", class_="s-post-summary--meta-tags")
    tags = tag_element.find_all("li", class_="js-post-tag-list-item")
    return [t.get_text() for t in tags]


def get_question_data(question: BeautifulSoup) -> dict:
    """Returns a dict of question data."""

    title = question.find("h3").find("a")
    

    return {
        "title": title.get_text(),
        "link": title["href"],
        "tags": get_post_tags(question),
        "user": get_user_data(question),
        "posted": question.find("span",
                                class_="relativetime")["title"]
    }


def get_questions_from_page(page_data: BeautifulSoup) -> list[dict]:
    """Returns a list of question dicts extracted from an SE page."""
    elements = page_data.find("div",
                              id="questions").find_all("div",
                                                       class_="s-post-summary--content")

    return [get_question_data(q) for q in elements]


def write_data_to_csv(question_data: list[dict], filename: str) -> None:
    with open(filename, "w") as f:
        writer = DictWriter(f, question_data[0].keys())
        writer.writeheader()
        writer.writerows(question_data)


if __name__ == "__main__":

    load_dotenv()

    questions = []
    for page_num in range(1, int(ENV["MAX_PAGES"]) + 1):
        try:
            page = scrape_page(f"{ENV['BASE_URL']}/questions?tab=newest&page={page_num}")
            questions.extend(get_questions_from_page(page))
            sleep(1)
        except (ValueError, IndexError):
            print("failed on Page {page_num}.")

    write_data_to_csv(questions, ENV["OUTPUT_FILE"])
