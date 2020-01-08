import datetime

def gather_page_metadata(rendered_page):
    '''
        Parses the rendered HTML for the metadata that we want to collect and stores the data in a dictionary

        Currently collects: Scan Date, Page Title, Whether a login is present (bool), What was scanned (router, camera, web storage, or other),
        and the size of the rendered webpage

        Dictonary Keys (in order):
            Scan Date - (str)
            Page Title - (str)
            Login Found - (bool)
            Comments - (str)
            Page Size - (str)
        
        Args:
            rendered_page (HTML): HTML object that is ready to be parsed

        Returns:
            dict: A dictionary containing data gathered on the webpage
    '''

    page_data = {}

    page_data["Scan Date"] = f"{datetime.datetime.now():%m-%d-%Y %H:%M}"

    if rendered_page == -1:
        page_data["Comments"] = "Error occurred when parsing webpage"
        return page_data
    
    page_data["Page Title"] = check_page_title(rendered_page)
    page_data["Login Found"] = check_for_login(rendered_page)

    comments = ""
    comments += check_for_router(rendered_page)
    comments += check_for_camera(rendered_page)
    comments += check_for_storage(rendered_page)

    if comments ==  "":
        comments += "Other device found"

    page_data["Comments"] = comments

    page_data["Page Size"] = f"{len(rendered_page.html)} bytes"

    return page_data
    
def check_page_title(rendered_page):
    title = rendered_page.find("title", first=True)
    return title.text

def check_for_login(rendered_page):
    if rendered_page.search("password"):
        return True
    return False

def check_for_router(rendered_page):
    if rendered_page.search("router") or rendered_page.search("access point"):
        return "Router/Access Point found\n"
    return ""

def check_for_camera(rendered_page):
    if rendered_page.search("camera"):
        return "Camera found\n"
    return ""

def check_for_storage(rendered_page):
    if rendered_page.search("storage"):
        return "Online storage found\n"
    return ""