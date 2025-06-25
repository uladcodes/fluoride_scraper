# Selenium: my main tool for browser automation here
from selenium import webdriver # My MARIO – launches and drives the browser
from selenium.common import NoSuchElementException # If the element is not found, don't crash – just move on
# Precise targeting – what and where to look for
from selenium.webdriver.common.by import By # Specifies how to locate elements (by ID, class, etc.)
# Smart waiting logic – don’t rush
from selenium.webdriver.support.ui import WebDriverWait # Checks every 0.5s for the element, up to a timeout
from selenium.webdriver.support import expected_conditions as EC # Defines what condition we are waiting for (e.g., visibility)
# Bridge between Python and Chrome
from selenium.webdriver.chrome.service import Service # Connects Python to ChromeDriver
# Manual pause
from time import sleep # Use for fixed wait (don’t mix with WebDriverWait on the same element!)
# Data structure and export
import pandas as pd # Handles table data (DataFrames), great for saving to CSV/Excel
# String filtering
import re # Extracts specific patterns from raw text (e.g., only numbers or selected words)

data = [] # A list to collect scraped data before saving it to Excel
# Define the path to the ChromeDriver executable (the "door" that connects Python to your browser)
service = Service(r"chromedriver.exe") # NOTE: update the path to your local ChromeDriver executable
driver = webdriver.Chrome(service=service) # Create a new Chrome browser window controlled by Selenium
# Set the URL that contains ALL the toothpaste product cards
url = "https://www.colgate.com/en-us/products/toothpaste" # NOTE: This URL may change over time - make sure to use the current Colgate toothpaste page
driver.get(url) # Open the URL in the browser

try:       # Try to accept the cookie popup if it appears
    accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept All')]")
    accept_button.click()
    print("Cookies accepted!") # Mission complete — now we can continue
    sleep(2) # Short pause to let the page settle
except NoSuchElementException:
    print("No cookies popup!") # Great, no need to deal with it this time
# Locate all product cards on the page using CSS selector
cards = driver.find_elements(By.CSS_SELECTOR, ".grid-item-product")
print(f"Found {len(cards)} product cards.") # Show how many were found — should be 45
# Save all product links from each card (just in case we need to revisit them one by one)
links = []

for card in cards:    # Loop through each product card to extract individual product page links
    try:
        # Find the clickable link inside the card
        link_element = card.find_element(By.CLASS_NAME, "product-detail-link")
        link = link_element.get_attribute("href")
        links.append(link) # Save the link
    except Exception as e:
        print(f"Skipping card: {e}") # If anything breaks, skip and report
        continue
for i, link in enumerate(links): # Loop through all collected product links and visit each one
    try:
        print(f"\nLoading card {i + 1} of {len(links)}") # Show progress in terminal
        driver.execute_script("window.scrollTo(0, 0);") # Scroll to top in case an ad or popup blocks the view
        driver.get(link) # Navigate to the product page

        try: # Try to remove the popup window (e.g., customer feedback modal) using JavaScript
            driver.execute_script("""
            let popup = document.querySelector('.mopinion-modal');
            if (popup) popup.remove();
            """) # Use JavaScript inside Selenium to remove an annoying modal
            print("Popup removed with JS!")
        except Exception as e:
            print(f"Error removing popup or loading page: {e}")  # Catch any general error that might happen while navigating to the link
            sleep(5)
            continue
        def open_three_dots(driver):  # Opens the hidden menu on mobile version by clicking the product title element (3 dots)
            try:    # Wait for the "three dots" element to be clickable
                three_dots = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "product-detail-title-mobile"))
                )
                driver.execute_script("arguments[0].click();", three_dots)
                print("Three dots clicked")
                sleep(1)
            except Exception as e:
                print(f"Failed to click three dots: {e}")
            # Scroll to top of the page — helps prevent stuck state or missing elements
            driver.execute_script("window.scrollTo(0, 0);")
            sleep(1)
            open_three_dots(driver) # Call function to open 3-dots menu (mobile product title)
        try:
            # This was the hardest part of the whole project!
            # The website used non-standard HTML structure, so I had to extract the name manually from raw HTML using regex.
            print("looking for name...")
            sleep(5)  # Giving the page a bit more time before searching (can be adjusted or removed)
            # Wait up to 12 sec until the name element appears in DOM
            name_element = WebDriverWait(driver, 12).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-detail-title"))
            )
            # Get the full HTML of the element and extract clean text
            raw_name = name_element.get_attribute("outerHTML").strip()
            # Use regex to get only the text between tags (like <h1>TEXT</h1>)
            match_name = re.search(r">(.*?)<", raw_name)
            name = match_name.group(1).strip() if match_name else "N/A"
            print(f"Toothpaste name: {name}")
        except Exception as e:
            print(f"Name not found: {e}")
            name = "N/A"
            sleep(2)

            print("Looking for stars...") # Step to find the star rating of the product
        try:
            # Wait up to 10 seconds for the rating container to appear
            stars_element = WebDriverWait(driver, 10). until(
                EC.presence_of_element_located((By.CLASS_NAME, "bv_avgRating_component_container"))
            )
            # Get the raw HTML of the rating element
            raw_stars = stars_element.get_attribute("outerHTML").strip()
            # Extract the number of stars using split magic (fragile but works here)
            # Basically splits like this: '...>4.6<...' -> ['...', '4.6<...'] -> '4.6'
            stars = raw_stars.split(">")[1].split("<")[0].strip()
            print(f"Stars found: {raw_stars}")
        except Exception as e:
            print(f"Stars not found: {e}")
            stars = "N/A"
            sleep(1)

            print("Looking for reviews...") # Step to extract number of reviews for the product
        try:
            # Wait up to 5 seconds for the <meta> tag inside the reviews container to appear
            reviews_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.bv_numReviews_component_container meta"))
            )
            # Get the number of reviews from the 'content' attribute of the <meta> tag
            reviews = reviews_element.get_attribute("content")
            print(f"Reviews found: {reviews}")
        except Exception as e:
            print(f"Reviews not found: {e}")
            reviews = "N/A"
            sleep(1)

            print("Trying to open Ingredients section...")
        try:
            # Find the "Ingredients" section button using XPath and click it via JavaScript
            ingredients_button = driver.find_element(By.XPATH, "//button[.//span[text()='Ingredients']]")
            driver.execute_script("arguments[0].click();", ingredients_button)
            print("Ingredients section opened with JS.")
            sleep(1)
        except Exception as e:
            print(f"Couldn't click ingredients section: {e}")
        try:
            # Wait for the ingredients content segments to appear
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "segment"))
            )
            segments = driver.find_elements(By.CLASS_NAME, "segment")
            print(f"Found {len(segments)} segments")
        except Exception as e:
            print(f"Segments not found: {e}")
            segments = []
        # Set default in case no ingredient is found
        active_ingredients = "N/A"
        # Loop through the segments to find "Active Ingredient" and extract the next block
        for i in range(len(segments)):
            if "Active Ingredient" in segments[i].text:
                if i + 1 < len(segments):
                    active_ingredients = segments[i + 1].text.strip()
                    print(f"Active Ingredients found: {active_ingredients}")
                    break
        # Print and store the collected data for this product
        print("_" * 65)
        print("Final parsed data:")
        print(f"Name:             {name}")
        print(f"Stars:            {stars}")
        print(f"Reviews:          {reviews}")
        print(f"Active Ingredients:\n{active_ingredients}")
        print("-" * 65)
        # Save the parsed data into the list (to later export as a table)
        data.append({
            "Name": name,
            "Stars": stars,
            "Reviews": reviews,
            "Active Ingredients": active_ingredients
        })

        driver.back() # Go back to the main product list page to load the next card
        sleep(3) # Wait a bit to avoid overloading the site or missing elements

    except Exception as e:
        print(f"Error while parsing card {i + 1}: {e}")
        continue
# FINAL STEP: Convert data to Excel
df = pd.DataFrame(data) # Convert the list of dictionaries into a DataFrame (table)
df["Contains Fluoride"] = df["Active Ingredients"].str.lower().str.contains("fluoride") # Add a new column: check if "fluoride" is present in Active Ingredients
df.to_excel("colgate_toothpastes.xlsx", index=False) # Save the DataFrame to an Excel file (no index column)
print("File saved as colgate_toothpastes.xlsx")
# Close the browser
driver.quit()