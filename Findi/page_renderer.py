from requests_html import HTMLSession
import page_parser as parser

def load_page(website):
    '''
        Loads a webpage and attempts to render any Javascript on the page

        Args:
            website (str): The web address to load

        Returns:
            HTML: The rendered webpage as an HTML document that is ready to be parsed. (See requests-html documentation and requests documentation)
            int: If an Exception is raised -1 will be returned

        Raises:
            Exception: Exception will be raised if the provided website is unable to be rendered and will return -1
    '''

    # create an HTML Session object
    session = HTMLSession()
    
    full_web_address = "http://" + website
    resp = session.get(full_web_address)
    
    # Run JavaScript code on webpage
    try:
        resp.html.render(timeout=10, sleep=3)
    except Exception as e:
        print(f"Unable to load Javascript, failed with Exception {e}")
        # return -1
    
    rendered_page = resp.html

    return rendered_page

if __name__ == "__main__":
    p = load_page("http://71.45.49.173/")
    parser.gather_page_metadata(p)