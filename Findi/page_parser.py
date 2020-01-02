import datetime

page_data = {}

def print_results():
    print(page_data)

def get_scan_results():
    return page_data

def gather_page_metadata(rendered_page):
    page_data["Scan Date"] = f"{datetime.datetime.now():%m-%d-%Y %H:%M}"
    page_data["Page Title"] = check_page_title(rendered_page)
    page_data["Login Found"] = check_for_login(rendered_page)

    comments = ""
    comments += check_for_router(rendered_page)
    comments += check_for_camera(rendered_page)
    comments += check_for_storage(rendered_page)
    page_data["Comments"] = comments

    page_data["Page Size"] = f"{len(rendered_page.html)} bytes"

    print_results()
    
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