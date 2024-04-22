from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options


def run_scraping(save_location="page_sources",  
                 urls = {   'snerikes' : 'https://www.facebook.com/snerikes/events', 'stockholm' : 'https://www.facebook.com/stockholmsnation/events' }


    ):
    options = Options()
     # Example argument; adjust according to your needs
    # Add other options as needed

    driver = webdriver.Chrome(options=options)
    all_nation_url = {
    "Stockholms nation" : "https://www.facebook.com/stockholmsnation/events",
    "Uplands nation" : "https://www.facebook.com/uplandsnation/events",
    "Gästrike-Hälsinge nation" : "https://www.facebook.com/ghnation/events",
    "Östgöta nation" : "https://www.facebook.com/ostgotanation/events",
    "Västgöta nation" : "https://www.facebook.com/vastgotanation/events",
    "Södermanland-Nerikes nation" : "https://www.facebook.com/snerikes/events",
    "Västmanlands-Dala nation" : "https://www.facebook.com/VDala/events",
    "Smålands nation" : "https://www.facebook.com/smalandsuppsala/events",
    "Göteborgs nation" : "https://www.facebook.com/goteborgsnation/events",
    "Kalmar nation" : "https://www.facebook.com/kalmar.nation.uppsala/events",
    "Värmlands nation" : "https://www.facebook.com/VarmlandsNation/events",
    "Norrlands nation" : "https://www.facebook.com/norrlands.nation/events",
    "Gotlands nation" : "https://www.facebook.com/gotlandsnation/events",


    #add all
    }

    x = 0
    try:
        for key, url in all_nation_url.items(): 
            driver.get(url)
            time.sleep(5)


            print("Page Title:", driver.title)
            html_content = driver.page_source

            with open(f'page_sources/{key}_page_source.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            x+=1
    finally:
        driver.quit()
    print(f"HTML content saved, {x} items")