import pytest

@pytest.fixture
def fake_question_no_user_link():
    html_text = """
            <div>
                <div class="s-user-card--link">
                    Name
                </div>
            </div>
        """

    fake_question = BeautifulSoup(html_text,
                                features="html.parser").find("div")
    
    return fake_question
