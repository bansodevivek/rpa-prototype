from automation.browser import get_browser
from credentials import LOGIN_URL, USERNAME, PASSWORD

def login():
    print("Launching browser...")
    playwright, browser, page = get_browser()

    print("Navigating to login page...")
    page.goto(LOGIN_URL)

    print("Filling username and password...")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)

    print("Clicking login...")
    page.click('input[type="submit"]')

    content = page.content().lower()
    print("Checking login success...")
    if "logout" in content:
        print("[✅] Login successful.")
    else:
        print("[❌] Login failed.")

    return playwright, browser, page
