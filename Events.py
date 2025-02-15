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
    options.add_argument("--headless")  # run headless for CI
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # help in low-resource environments
    options.add_argument("--log-level=3")

    # Use webdriver_manager to automatically handle ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://steamdb.info/sales/history/"
        driver.get(url)

        # Wait until the table is loaded
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-sales-history tbody"))
        )

        # Try to locate the table rows
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table-sales-history tbody tr")

        # If no rows found, raise an exception to trigger our debugging output
        if not rows:
            raise Exception("No rows found in the sales table. The page structure may have changed.")

        sales = []
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) < 2:
                continue
            sale_name = columns[0].text.strip()
            sale_date = columns[1].text.strip()
            sales.append((sale_name, sale_date))

        # Write the output to a text file
        with open("sales_data.txt", "w") as file:
            if sales:
                file.write("📢 Upcoming Steam Sales:\n")
                for sale in sales:
                    file.write(f"{sale[0]} - {sale[1]}\n")
            else:
                file.write("⚠️ No sales found. The page structure may have changed.\n")

    except Exception as e:
        # Write detailed debugging info on error
        with open("sales_data.txt", "w") as file:
            file.write(f"❌ Error: {e}\n")
            file.write("\n--- PAGE SOURCE START ---\n")
            file.write(driver.page_source)
            file.write("\n--- PAGE SOURCE END ---\n")

    finally:
        driver.quit()

if __name__ == "__main__":
    get_steam_sales()
    