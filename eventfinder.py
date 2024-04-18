from bs4 import BeautifulSoup
import json
import os


save_file = "events.json"

directory_path = os.path.join(os.getcwd(), "page_sources")
if not os.path.exists(directory_path):
    exit()

    
for file_loc in os.listdir(directory_path):
    print(file_loc)
    
    full_file_path = os.path.join(directory_path, file_loc)

    with open(full_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()


    soup = BeautifulSoup(html_content, 'html.parser')

    event_blocks = soup.find_all('div', class_="x6s0dn4")

    events = []
    for event in event_blocks:
        title_link = event.find('a')
        image_tag = event.find('img')
        time_span = event.find('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84")
        location_info = event.find('div', class_="x1gslohp")

        if title_link and image_tag and time_span and location_info:
            event_info = {
                "title": title_link.text.strip(),
                "url": title_link['href'],
                "image_url": image_tag['src'],
                "time": time_span.text.strip(),
                "location": location_info.text.strip()
            }
            events.append(event_info)

    with open(save_file, 'w') as f:
        json.dump(events, f, indent=4)
        
    print(f"Dumped: {len(events)} events from {file} to {save_file}")



print("Events extracted and saved to 'events.json'")