from requests_html import HTMLSession
import page_parser as parser

def load_page(website):
    '''
        Loads a webpage and attempts to render any Javascript on the page

        Args:
            website (str): The web address to load

        Returns:
            HTML: The rendered webpage as an HTML document that is ready to be parsed. (See requests-html documentation and requests documentation)

        Raises:
            Exception: Exception will be raised if the provided website is unable to be rendered
    '''

    # create an HTML Session object
    session = HTMLSession()
    
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
    p = load_page("http://71.45.49.173/")
    parser.gather_page_metadata(p)