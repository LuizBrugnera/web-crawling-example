import requests
from bs4 import BeautifulSoup

# URL base do site
base_url = "https://books.toscrape.com/catalogue/"

# Função para realizar o crawling
def crawl_books():
    # URL inicial
    next_page = "page-1.html"
    all_books = []  # Lista para armazenar informações de todos os livros
    
    while next_page:
        # Monta a URL completa
        url = base_url + next_page
        print(f"Acessando: {url}")
        
        # Solicitação HTTP para a página
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Erro ao acessar {url}: {response.status_code}")
            break
        
        # Analisa o HTML da página
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Encontra os livros na página
        books = soup.find_all("article", class_="product_pod")
        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            availability = book.find("p", class_="instock availability").text.strip()
            
            # Adiciona as informações à lista
            all_books.append({
                "title": title,
                "price": price,
                "availability": availability
            })
        
        # Encontra o link para a próxima página
        next_page_tag = soup.find("li", class_="next")
        next_page = next_page_tag.a["href"] if next_page_tag else None
    
    # Exibe o resultado
    print(f"Total de livros coletados: {len(all_books)}")
    for book in all_books[:5]:  # Exibindo os primeiros 5 livros como exemplo
        print(f"Título: {book['title']}")
        print(f"Preço: {book['price']}")
        print(f"Disponibilidade: {book['availability']}")
        print("-" * 40)

# Executa o crawling
crawl_books()
