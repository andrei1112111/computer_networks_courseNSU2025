from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import csv


browser = webdriver.Safari()
wait = WebDriverWait(browser, 10)

num_pages = 5
questions_per_page = 2

parsed_questions = [
    ("page_number", "question_number", "title_tag", "question_link", "votes", "answers", "views", "text")  # head
]


browser.get("https://stackoverflow.com/questions")

for page in range(1, num_pages + 1):
    wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "s-post-summary")))

    questions = browser.find_elements(By.CLASS_NAME, "s-post-summary")[:questions_per_page]

    for index, question in enumerate(questions, start=1):
        title_tag = question.find_element(By.CLASS_NAME, "s-link")
        question_link = title_tag.get_attribute("href")

        stats_items = question.find_elements(By.CLASS_NAME, "s-post-summary--stats-item")
        votes = stats_items[0].text.strip()
        answers = stats_items[1].text.strip().split("\n")[0]
        views = stats_items[2].text.strip().split("\n")[0]

        question_text_element = question.find_element(By.CLASS_NAME, "s-post-summary--content-excerpt")
        question_text = question_text_element.text.strip() if question_text_element else "No description available"

        parsed_questions.append(
            (page, index, title_tag.text.strip(), question_link, votes, answers, views, question_text)
        )

    try:
        next_button = browser.find_element(By.CSS_SELECTOR, "a.s-pagination--item[rel='next']")
        browser.execute_script("arguments[0].click();", next_button)
    except Exception as e:
        print(e.__class__.__name__)
        break


browser.quit()

with open('stackoverflow_questions.csv', 'w', newline='') as f:
    csv.writer(f).writerows(parsed_questions)
