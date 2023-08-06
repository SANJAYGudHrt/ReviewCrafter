from flask import Flask, render_template, Response
import requests
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)


def scrape_amazon_reviews(product_urls):
    all_reviews = []

    for url in product_urls:
        page_num = 1
        while True:
            response = requests.get(url, params={'pageNumber': page_num})
            soup = BeautifulSoup(response.content, 'html.parser')

            review_elements = soup.select('.review')
            if not review_elements:
                break

            for element in review_elements:
                user_name = element.select_one('.a-profile-name').get_text(strip=True)
                review = {
                    'user_name': user_name,
                    'rating': element.select_one('.a-icon-alt').get_text(strip=True),
                    'body': element.select_one('.review-text-content').get_text(strip=True)
                }
                all_reviews.append(review)

            page_num += 1

    return all_reviews


@app.route('/')
def index():
    product_urls = [
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber=3",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_4?ie=UTF8&reviewerType=all_reviews&pageNumber=4",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_5?ie=UTF8&reviewerType=all_reviews&pageNumber=5",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_6?ie=UTF8&reviewerType=all_reviews&pageNumber=6",
    ]

    reviews = scrape_amazon_reviews(product_urls)
    return render_template('index.html', reviews=reviews)


@app.route('/download_csv', methods=['POST'])
def download_csv():
    product_urls = [
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber=3",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_4?ie=UTF8&reviewerType=all_reviews&pageNumber=4",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_5?ie=UTF8&reviewerType=all_reviews&pageNumber=5",
        "https://www.amazon.in/Samsung-Storage-Battery-Octa-Core-Processor/product-reviews/B0BZCWLJHK/ref=cm_cr_getr_d_paging_btm_next_6?ie=UTF8&reviewerType=all_reviews&pageNumber=6",
    ]

    reviews = scrape_amazon_reviews(product_urls)

    response = Response(content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename="amazon_reviews.csv"'

    csv_writer = csv.DictWriter(response.stream, fieldnames=['user_name', 'rating', 'body'])
    csv_writer.writeheader()

    for review in reviews:
        csv_writer.writerow({'user_name': review['user_name'], 'rating': review['rating'], 'body': review['body']})

    return response


if __name__ == '__main__':
    app.run(debug=True)
