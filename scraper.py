from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

def run_scraping(save_file="events.json",  
           urls=
           {    
                "snerikes" : "https://www.facebook.com/snerikes/events",
                "stockholm" : "https://www.facebook.com/stockholmsnation/events"
                #add all
            }
    ):
    all_nation_url = urls
    driver = webdriver.Chrome(ChromeDriverManager().install())



    x = 0
    try:
        for key, url in all_nation_url.items(): 
            driver.get(url)
            time.sleep(10)


            print("Page Title:", driver.title)

            html_content = driver.page_source

            with open(f'page_sources/{key}_page_source.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            x+=1


    finally:
        driver.quit()

    print(f"HTML content saved, {x} items")