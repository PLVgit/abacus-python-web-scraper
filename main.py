from abacus_scraper import AbacusScraper  # Importa la clase AbacusScraper desde el archivo abacus_scraper.py

# URL base de la página web de Abacus
base_url = 'https://www.abacus.coop/es/libros/libros-recomendados/libros-mas-leidos'

# Crea una instancia de AbacusScraper
scraper = AbacusScraper(base_url)

# Obtén las URL de todas las páginas
scraper.get_next_page_urls()

# Obtén las URL de todos los libros de todas las páginas
scraper.get_book_urls()

# Extrae los detalles de los libros
scraper.scrape_book_details()

# Crea un DataFrame a partir de los datos extraídos
scraper.create_dataframe()

# Exporta el DataFrame a un archivo CSV
scraper.export_to_csv('dataset.csv')
