import argparse
import os

import ast


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run parts of the multipurpose application.")
    parser.add_argument('--scrape', action='store_true', help='Run the web scraping part.')
    parser.add_argument('--process', action='store_true', help='Run the HTML processing part.')
    parser.add_argument('--save-loc', type=str, default=os.getcwd(), help='Directory to save files.')
    
    parser.add_argument('--fullpipeline', help="Full run")
    # Adding predict argument
    
    parser.add_argument('--predict', action='store_true', help='Run the prediction part.')


    args = parser.parse_args()


    
    return args
def main():
    args = parse_arguments()

    if args.scrape:
        from scraper import run_scraping
        run_scraping()
        
    if args.process:
        from processer import process_html
        process_html()

    if args.predict:
        from predictor import predict
        predict()

    if args.fullpipeline:
        from scraper import run_scraping
        from predictor import predict
        from processer import process_html
        from sheets import push_to_sheets
        run_scraping()
        process_html()
        predict()
        push_to_sheets()
    

if __name__ == '__main__':
    main()