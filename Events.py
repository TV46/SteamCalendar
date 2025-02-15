from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_steam_sales():
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no browser window)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")  # Suppress logs

    # Install and launch Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open SteamDB sales history page
    url = "https://steamdb.info/sales/history/"
    driver.get(url)

    try:
        # Wait until the table appears
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-sales-history tbody"))
        )

        # Find sales table rows
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table-sales-history tbody tr")

        sales = []
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) < 2:
                continue

            sale_name = columns[0].text.strip()
            sale_date = columns[1].text.strip()
            sales.append((sale_name, sale_date))

        # Print results
        if sales:
            print("\n📢 Upcoming Steam Sales:")
            for sale in sales:
                print(f"{sale[0]} - {sale[1]}")
        else:
            print("⚠️ No sales found. The page structure may have changed.")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

# Run the script
get_steam_sales()
