from bs4 import BeautifulSoup
import json
import os

from dateutil import parser
from datetime import datetime
import pytz
import pandas as pd

from datetime import datetime
import pytz
from dateutil import parser

def parse_datetime(time_str):
    time_str = " ".join(time_str.split()).replace(',', '')

    time_str = time_str.split(" AND")[0]

    if "CEST" in time_str:
        tz_end_index = time_str.find("CEST") + len("CEST")
    else:
        tz_end_index = len(time_str)

    current_year = datetime.now().year
    tzinfos = {"CEST": pytz.timezone("Europe/Berlin")}

    datetime_part = time_str[:tz_end_index]
    full_datetime_str = f"{datetime_part} {current_year}"

    try:
        parsed_datetime = parser.parse(full_datetime_str, tzinfos=tzinfos)
    except ValueError as e:
        parsed_datetime = datetime(1900, 1, 1, 0, 0)

    return parsed_datetime





def process_html():
    save_file = "events.json"

    directory_path = os.path.join(os.getcwd(), "page_sources")
    print(directory_path)
    if not os.path.exists(directory_path):
        exit()

    events = []
    for file_loc in os.listdir(directory_path):
        try:
            print(file_loc)
            full_file_path = os.path.join(directory_path, file_loc)
            with open(full_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            event_blocks = soup.find_all('div', class_="x6s0dn4 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1olyfxc x9f619 x78zum5 x1e56ztr xyamay9 x1pi30zi x1l90r2v x1swvt13 x1gefphp")

            #for event in event_blocks:
            #
            #    title_link = event.find('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv x1s688f")
            #    image_tag = event.find('img')
            #    time_span = event.find('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84")
            #    location_info = event.find('div', class_="x1gslohp")
            #    event_info = {
            #        "title": title_link.text,
            #        "nation" : file_loc.split("_")[0],
            #        "url": title_link['href'],
            #        "image_url": image_tag['src'],
            #        "time": parse_datetime(time_span.text.strip()),
            #        "location": location_info.text.strip().split("UppsalaEvent")[0]
            #    }
            #    events.append(event_info)
            #print(f"Successfully processed {file_loc}")
            #
            for event in event_blocks:
                title_link = event.find('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv x1s688f")  # Update class name if needed
                image_tag = event.find('img')
                time_span = event.find('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84") 
                location_info = event.find('div', class_="x1gslohp") 
                
                if title_link and title_link.text :
                    x = title_link.text 
                    if "Bamba " in x:
                        print()
                        print(time_span.text.strip())
                        print()
               
                
               

                parsed_time = parse_datetime(time_span.text.strip()) if time_span and time_span.text else None
                time = parsed_time.time() if parsed_time else ""
                date = parsed_time.date() if parsed_time else ""
                event_info = {
                    "title": " ".join(title_link.text.split()) if title_link and title_link.text else None,
                    "date": str(date),
                    "time": str(time),
                    "category" : "",
                    "nation": file_loc.split("_")[0] if file_loc else "",
                    "description" : "",
                    "image_url": image_tag['src'] if image_tag and 'src' in image_tag.attrs else "",
                    "frequency" : "",
                    "link": title_link['href'] if title_link and 'href' in title_link.attrs else "",
                    "location":"".join(location_info.text.strip().split("UppsalaEvent")[0]).split() if location_info and location_info.text else "",
             

                }
                events.append(event_info)




        except Exception as e:
            print(f"Error processing {file_loc}: {e}")

    df = pd.DataFrame.from_dict(events)
    
    df = df.dropna(subset=['title'])
    df.to_excel("events.xlsx")

    #df.to_json('events.json', orient='records', indent=4)

    p = df.to_dict(orient='records')## HÄR ÄR DET NÅGOT LURT
    with open('events.json', 'w', encoding="utf-16") as f:
        json.dump(p, f, ensure_ascii=False, indent=4)



    print(f"Dumped: {len(df)} events to events.xlsx")
    

