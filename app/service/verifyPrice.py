from service.email import send_email


def verifyPrice(book, updated_book):
    print('Verifying price...')
    if book['price'] and updated_book.price:
        percent = float(book['price']) / float(updated_book.price)  # Correct (assuming 'price' is an attribute)
        if percent > 1.2:
            send_email(book, updated_book, percent)
    return