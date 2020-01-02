def print_results(rendered_page):
    print(f"Size of webpage: {len(rendered_page.html)} bytes")
    # print(rendered_page)

def gather_page_metadata(rendered_page):
    check_page_title(rendered_page)
    check_for_login(rendered_page)
    check_for_router(rendered_page)
    check_for_camera(rendered_page)
    check_for_storage(rendered_page)

def check_page_title(rendered_page):
    title = rendered_page.find("title", first=True)
    print(title.text)

def check_for_login(rendered_page):
    if rendered_page.search("password"):
        print("login found")

def check_for_router(rendered_page):
    if rendered_page.search("router") or rendered_page.search("access point"):
        print("router/access point found")

def check_for_camera(rendered_page):
    if rendered_page.search("camera"):
        print("camera found")

def check_for_storage(rendered_page):
    if rendered_page.search("storage"):
        print("online storage found")