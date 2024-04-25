from bs4 import BeautifulSoup
import pandas as pd #to export into excel sheets
import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS

#run this
#pip install openpyxl xlml lxml html.parser requests bs4 pandas
#pip install bs4 pandas requests matplotlib wordcloud flask flask_cors
#pip install bs4 pandas requests matplotlib wordcloud flask openpyxl xlml lxml html.parser requests bs4 pandas
def main_fk(product_name="iphone 15 pro"):


        main_url = extract_first(product_name)
        soup =get_soup(main_url)
        print(main_url)
        # print(soup)
        total_reviews = get_total_reviews(soup)
        # #count -> no. of pages we need ot loop considering 10 reviews per page
        if(total_reviews==0):
            print("NO REVIEWS FOR THE PRODUCT GIVEN")
        else:
            count = total_reviews//10+1 if total_reviews%10!=0 else total_reviews//10 if total_reviews%10==0 else 1
            print(count," times we have to scrape for all reviews.. each page 10 revs")
            revs=[]
            global mini_revs
            mini_revs=[]
            if count>1:
                for i in range(1,count+1):
                    revs+=extract(get_soup(main_url,i))
            
            else:
                revs+=extract(soup)

            df = pd.DataFrame(revs)
            df.to_excel("new.xlsx",index=False)
            # phrases = [' '.join(pair) for pair in zip(mini_revs[:-1], mini_revs[1:])]

            # Join the phrases into a single string
            text = ' '.join(mini_revs)

            wc = WordCloud(
                background_color="black",
                stopwords=STOPWORDS,
                height=600,
                width=800,
                prefer_horizontal=1
            ).generate(text)
            wc.to_file("wc.png")
            return revs

def extract_first(product_name):
    # product_name = input("What are you looking for ? ").lower().strip()
    base_url = "https://www.flipkart.com/search?q="
    
    final_url = (base_url+product_name).replace(" ","+")
    print(final_url)
    base_soup = get_soup(final_url)
    return extract_link_from_search(base_soup)


def extract_link_from_search(soup):

    anchor_tag = soup.find("a", class_="CGtC98") 

    if not anchor_tag:
        anchor_tag = soup.find("a", class_="rPDeLR")
    if not anchor_tag:
        anchor_tag = soup.find("a", class_="VJA3rP")

    main_link = anchor_tag["href"].split("&lid=")[0]

    final_main_link = "https://www.flipkart.com"+main_link
    print(final_main_link)
    return final_main_link


def get_soup(review_url,page_number=1):
    
    review_url = review_url.replace("/p/","/product-reviews/")+f"&page={page_number}"


    user_name = "muralimanas30"
    password = "IamMurali591_"
    payload = {
        "source":"universal",
        "url":review_url,
        
    }

    response = requests.request("POST" , 'https://realtime.oxylabs.io/v1/queries', auth=(user_name,password),json=payload)  
    print(response.status_code) #404 or 200 etc..
    response_html = response.json()['results'][0]['content']
    soup = BeautifulSoup(response_html , "lxml")     #using beautiful soup
    # print(soup.prettify)
    return soup
    
    

def extract(soup):

    
    reviews= soup.find_all("div",class_="col EPCmJX Ma1fCG")      #getting container with reviews
    
    revs = []

    for review in reviews:
        
        customer_name = review.find_all("p",class_="_2NsDsF AwS1CA")[0].text

        mini_review = str(review.find("p",class_="z9E0IG").text).strip()
        if len(mini_review)==0:
            mini_review = str(review.find("p",class_="_11pzQk").text).strip()
        print(mini_review)    
        mini_revs.append(mini_review.replace(" ","_"))
        mini_revs.append(mini_review.replace("-","_"))

        
        rating = review.find("div",class_="XQDdHH")
        if not rating:
            rating = review.find("div",class_="XQDdHH Ga3i8K")
        
        if not rating:
            rating = review.find("div",class_="XQDdHH Js30Fc Ga3i8K")
        rating = str(rating.text).strip() + " out of 5"

        date = str(review.find_all("p",class_="_2NsDsF")[1].text).strip()

        review_body = str(review.find("div",class_="ZmyHeo").text).split("READ MORE")[0].strip()

        d1 = {
            "Product":str(soup.title.text).split("Reviews:")[0].strip(),
            "customer_name":customer_name.upper(),
            "rating":rating,
            "mini_review":mini_review,      #dict wtih field and appended to list "revs"
            "date":date,
            # "link":review_link,
            "review_body":review_body
        }
        print( 
              " Product       :  "+d1["Product"],
              " customer_name :  "+d1["customer_name"],
              " rating        :  "+d1["rating"],
              " mini-review   :  "+d1["mini_review"],
              " review-body   :  "+d1["review_body"],
              " date          :  "+d1["date"],
              sep="\n",end="\n\n*****************************\n")
        revs.append(d1)

    return revs 
        #list with 10 reviews , which would be concatenated with other previous reviews in main()


def get_total_reviews(soup):
    
    pages = soup.find("span", class_="Wphh3N")
    if not pages:
        pages = soup.find("span",class_="Wphh3N d4OmzS")
    if not pages:
        pages = soup.find("div",class_="atZ055")
    pages = pages.text.strip()
    print(pages)
    try:
        pages = int(pages.split("&")[1].split("Reviews")[0].strip().replace(",",""))
    except:
        pages = int(pages.split("and")[1].split("reviews")[0].strip().replace(",",""))
    print(pages," reviews in total")
    return pages
        #figuring out no. of reviews we have and no. of pages theyd take


if __name__=="__main__":
    main_fk()