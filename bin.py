import scraper
import write_database

#python C:\Users\Kyle\Desktop\2scraper\bin.py

ignore_errors = True

if __name__ == "__main__":
    results = scraper.load_all_hero_data()
    if(ignore_errors == True):
        write_database.DatabaseWriter(results, ignore_errors)
    else:
        print("\n*** ERRORS DETECTED, NOT WRITING DATABSE! ***")
