import pytest
from bs4 import BeautifulSoup

from main import scrape_page, get_user_data



def test_scrape_page_returns_soup_on_valid_url(requests_mock):

    requests_mock.get("https://xkcd.com/", text="<h1>Webcomic</h2><p>comic comic comic</p>")

    result = scrape_page("https://xkcd.com/")

    assert isinstance(result, BeautifulSoup)


def test_scrape_page_raises_error_if_unable_to_fetch_page(requests_mock):

    requests_mock.get("https://xkcd.com/", status_code=404)

    with pytest.raises(ValueError):
        scrape_page("https://xkcd.com/")


def test_get_user_data_returns_appropriate_dict():

    html_text = """
        <div>
            <div class="s-user-card--link">
                <a href="/link">Name</a>
            </div>
        </div>
    """

    fake_question = BeautifulSoup(html_text,
                                  features="html.parser").find("div")

    result = get_user_data(fake_question)

    assert isinstance(result, dict)
    assert "name" in result
    assert "link" in result
    assert {
        "name": "Name",
        "link": "/link"
    }


def test_get_user_data_returns_appropriate_dict_without_link(fake_question_no_user_link):

    result = get_user_data(fake_question)

    assert isinstance(result, dict)
    assert "name" in result
    assert "link" in result
    assert {
        "name": "Name",
        "link": None
    }