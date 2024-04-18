from bs4 import BeautifulSoup
import json
import os

def process_html():
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
    
        event_blocks = soup.find_all('div', class_="x6s0dn4 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1olyfxc x9f619 x78zum5 x1e56ztr xyamay9 x1pi30zi x1l90r2v x1swvt13 x1gefphp")
        print()
    
        events = []
        for event in event_blocks:
        
            title_link = event.find('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv x1s688f")
            image_tag = event.find('img')
            time_span = event.find('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84")
            location_info = event.find('div', class_="x1gslohp")
    
            event_info = {
                "title": title_link.text,
                "url": title_link['href'],
                "image_url": image_tag['src'],
                "time": time_span.text.strip(),
                "location": location_info.text.strip()
            }
            events.append(event_info)
    
        with open(save_file, 'w') as f:
            json.dump(events, f, indent=4)
            
        print(f"Dumped: {len(events)} events from {file_loc} to {save_file}")
    
    
    
    print(f"Events extracted and saved to '{file_loc}'")