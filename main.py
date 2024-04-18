import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run parts of the multipurpose application.")
    parser.add_argument('--scrape', action='store_true', help='Run the web scraping part.')
    parser.add_argument('--process', action='store_true', help='Run the HTML processing part.')
    return parser.parse_args()

def main():
    args = parse_arguments()
  
    if args.scrape:
        from scraper import process_html
        process_html()
        
    if args.process:
        from processer import run_scraping
        run_scraping()

if __name__ == '__main__':
    main()