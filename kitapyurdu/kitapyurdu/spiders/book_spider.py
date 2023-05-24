# Import necessary modules and packages
import scrapy

class BooksSpider(scrapy.Spider):

    # Define a spider named "books"
    name = "books"

    # Counter for the books
    book_count = 1

    # Open the file to write book information
    file = open("books.txt", "a", encoding = "UTF_8")

    # Starting URL for scraping book data
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/best_sellers&page=1&list_id=16&filter_in_stock=1&filter_in_stock=1"
    ]

    # Define the parse method that responsible for parsing the response and extracting the book information
    def parse(self, response):

        # Extract book names
        books = response.css("div.name.ellipsis a span::text").extract()

        # Extract publishers
        publishers = response.css("div.publisher span a span::text").extract()

        # Counter for iterating through books
        i = 0

        # Write book information to the file
        while i < len(books):

            self.file.write(str(self.book_count) + ".\n")
            self.file.write("Book Name: " + books[i] + "\n")
            self.file.write("Publisher: " + publishers[i] + "\n")
            self.file.write("---------------------------------------------------------------------\n")

            # Increment the book counter
            self.book_count += 1

            # Move to the next book
            i += 1

        # Extract the URL of the next page
        next_url = response.css("a.next::attr(href)").extract_first()

        if next_url is not None:
            
            # If there is a next page, send a request to parse it
            yield scrapy.Request(url = next_url, callback = self.parse)

        else:
            
            # If there are no more pages, close the file
            self.file.close()
