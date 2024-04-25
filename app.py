from bs4 import BeautifulSoup
import pandas as pd
from final_flipkart import main_fk
import json
import requests
from flask import Flask, render_template, request,jsonify
#pip install bs4 pandas requests matplotlib wordcloud flask openpyxl xlml lxml html.parser requests bs4 pandas
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        product_name = request.form['product-name']
        return render_template('searching.html', product_name=product_name)
    else:
        return 'Invalid request'


@app.route('/start_scraping', methods=['POST'])

def start_scraping():
    if request.method == 'POST':
        global product_name
        product_name = request.json['product_name']
        global reviews
        reviews = main_fk(product_name)  # Assuming main_fk returns the list of reviews
        
        return render_template('reviews.html', product_name=product_name, reviews=reviews)
    else:
        return 'Invalid request'



@app.route('/reviews')
def show_reviews():
    return render_template('reviews.html', product_name=product_name, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)
