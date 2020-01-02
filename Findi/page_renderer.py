from requests_html import HTMLSession

def load_page(website):
    # create an HTML Session object
    session = HTMLSession()
    
    # website = "http://71.45.49.173/"
    # Use the object above to connect to needed webpage
    resp = session.get(website)
    
    # Run JavaScript code on webpage
    try:
        resp.html.render(timeout=10, sleep=3)
    except Exception as e:
        print(f"Unable to load Javascript, failed with Exception {e}")
    
    rendered_page = resp.html

    return rendered_page

if __name__ == "__main__":
    load_page("http://71.45.49.173/")