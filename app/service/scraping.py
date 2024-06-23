from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

from model.book import Book

async def get_book_data(url): 
    try:
        print("Scraping ", url)
        user_agent = UserAgent().random
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        sleep(.5)

        driver.get(url)

        driver.implicitly_wait(3)
        sleep(5)

        try:
            title = driver.find_element(by=By.ID, value="productTitle").text
        except:
            title = driver.find_element(by=By.ID, value="title").text
        try:
            url_image = driver.find_element(by=By.ID, value="landingImage").get_attribute('src')
        except:
            url_image = driver.find_element(by=By.ID, value="main-image").get_attribute('src')
        try:
            url_image = driver.find_element(by=By.ID, value="landingImage").get_attribute('src')
        except:
            url_image = driver.find_element(by=By.ID, value="main-image").get_attribute('src')
        try:
            author = driver.find_element(by=By.CLASS_NAME, value="author").text
        except:
            author = driver.find_element(by=By.CLASS_NAME, value="contributorLink").text      

        price_whole = driver.find_element(by=By.CLASS_NAME, value="a-price-whole").text
        price_fraction = driver.find_element(by=By.CLASS_NAME, value="a-price-fraction").text


        book = Book(url, title, url_image, author, price_whole + '.' + price_fraction)
        print("\n\n" ,book.url, book.name, book.url_image, book.author, book.price,"\n\n" )

        return book
   
    except Exception as error:
        print(error)

        sleep(1)
        return await get_book_data(url)
    finally:
        if driver:
            driver.quit()


    
    


