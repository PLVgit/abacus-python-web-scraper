from abacus_scraper import AbacusScraper  # Import the AbacusScraper class from the abacus_scraper.py file

# # Base URL of the Abacus website
base_url = 'https://www.abacus.coop/es/libros/libros-recomendados/libros-mas-leidos'

# Create an instance of AbacusScraper
scraper = AbacusScraper(base_url)

# Get the URLs of all pages
scraper.get_next_page_urls()

# Get the URLs of all books from all pages
scraper.get_book_urls()

# Scrape the book details
scraper.scrape_book_details()

# Create a DataFrame from the extracted data
scraper.create_dataframe()

# Export the DataFrame to a CSV file
scraper.export_to_csv('abacus_llibres_recomanats.csv')
