import requests
from bs4 import BeautifulSoup
import pandas as pd

class AbacusScraper:
    def __init__(self, base_url):
        # Initializes the global variables
        self.base_url = 'https://www.abacus.coop/es/libros/libros-recomendados/libros-mas-leidos'
        self.page_urls = []
        self.book_urls = []
        self.book_data = []
        self.df = None

    def get_next_page_urls(self):
        response = requests.get(self.base_url)

        # Find pagination elements
        soup = BeautifulSoup(response.content, 'html.parser')

        paginator_div = soup.find('div', class_='paginator')


        page_links = paginator_div.find_all('a', class_='order-pagination')

        data_pages = [int(link['data-page']) for link in paginator_div.find_all('a', attrs={'data-page': True})]


        max_page = max(data_pages)

        self.page_urls.append(self.base_url)
 
        for page_num in range(2, max_page + 1):
            page_url = f"{self.base_url}?pageNo={page_num}"
            self.page_urls.append(page_url)

    def get_book_urls(self):
        # Generates the links for scraping individual books
        for link in self.page_urls:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')

        
            book_containers = soup.find_all('div', class_='image-container')
            for container in book_containers:
                book_link = container.find('a')['href']  # Buscar dentro de cada contenedor de libro
                full_book_link = 'https://www.abacus.coop' + book_link
                self.book_urls.append(full_book_link)


    def scrape_book_details(self):
        for url in self.book_urls:
            # Send GET request to the book URL
            response = requests.get(url)

        # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

        # Extract book information
            title_element = soup.find('h1', class_='product-name')
            title = title_element.text.strip() if title_element else None

            author_element = soup.find('p', class_='product-topinfo author')
            author = author_element.text.strip() if author_element else None

            description_element = soup.find('div', class_='description book-description')
            description = description_element.text.strip() if description_element else None

            actual_price_element = soup.find('span', class_='sales')
            actual_price = actual_price_element.text.strip() if actual_price_element else None

            prev_price_element = soup.find('span', class_='strike-through list')
            prev_price = prev_price_element.get_text().strip() if prev_price_element else None

            pages_element = soup.find('span', class_='label', string='Páginas/Hojas:')
            pages = pages_element.find_next_sibling('span', class_='value').text.strip() if pages_element else None

            year_element = soup.find('span', class_='label', string='Año de edición:')
            year = year_element.find_next_sibling('span', class_='value').text.strip() if year_element else None

            language_element = soup.find('span', class_='label', string='Idioma:')
            language = language_element.find_next_sibling('span', class_='value').text.strip() if language_element else None

            publisher_element = soup.find('span', class_='label', string='Editorial:')
            publisher = publisher_element.find_next_sibling('span', class_='value').text.strip() if publisher_element else None

            image_element = soup.find('div', class_='img-container')
            image = image_element.find('img')['src'] if image_element else None


            book_data = {
                'title': title,
                'author': author,
                'description': description,
                'actual_price': actual_price,
                'prev_price': prev_price,
                'pages': pages,
                'year': year,
                'language' : language,
                'publisher': publisher,
                'image': image
                        }

            self.book_data.append(book_data)

    def create_dataframe(self):
        # Create a Pandas DataFrame from the book data
        self.df = pd.DataFrame(self.book_data)

    def export_to_csv(self, filename):
        # Export the DataFrame to a CSV file
        self.df.to_csv(filename, index=True)
