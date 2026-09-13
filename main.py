import requests
import pandas as pd
import time
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

URL = "https://dummyjson.com/products"
OUTPUT_FILE_1 = "products.csv"
OUTPUT_FILE_2 = "category_report.csv"
MAX_RETRIES = 3

def get_retry_after_seconds(retry_after_value: str) -> float:
    if not retry_after_value:
        return 2.0

    if retry_after_value.isdigit():
        return max(float(retry_after_value), 2.0)

    try:
        target_time = parsedate_to_datetime(retry_after_value)
        now = datetime.now(timezone.utc)
        remaining_seconds = (target_time - now).total_seconds()
        return max(remaining_seconds, 2.0)
    except (ValueError, TypeError):
        return 2.0

def fetch_all_products():
    attempt = 1
    products = []
    total = None
    params = {
        "skip": 0,
        "limit": 100
        }
    with requests.Session() as session:
        while True:
            try:
                response = session.get(URL, timeout=10, params=params)
                response.raise_for_status()
                attempt = 1
            
                response_json = response.json()
                if not isinstance(response_json, dict):
                    print("Invalid API response: expected an object.")
                    return
                products_data = response_json.get("products")
                if not isinstance(products_data, list):
                    print("Invalid API response: products is not a list")
                    return
            
                products.extend(products_data)
                params["skip"] += params["limit"]
                total = response_json.get("total")
                if not isinstance(total, int):
                    print("Invalid API response: total is missing or invalid.")
                    return
                if params["skip"]  >= total:
                    break
            except requests.exceptions.JSONDecodeError as exc:
                print (f"Failed to decode json: {exc}")
                return
            except requests.RequestException as exc:
                response = exc.response
                if response is None:
                    wait_time = 2.0
                elif response.status_code == 429:
                    retry_after = response.headers.get("Retry-After") 
                    wait_time = get_retry_after_seconds(retry_after)
                elif response.status_code >= 500:
                    wait_time = 2.0
                else:
                    print(f"Request failed: {exc}")
                    return
                print(f"Request failed(attempt {attempt}): {exc}")
                if attempt >= MAX_RETRIES:
                    print("All retries failed.")
                    return
                attempt += 1
                time.sleep(wait_time)
        if len(products) != total:
            print(f"Data incomplete: expected {total}, got {len(products)}.")
            return
        return products

def clean_products(products):
    df  = pd.DataFrame(products, columns = ["id", "title", "price", "category", "stock"])
    df.drop_duplicates(subset = "id", inplace = True)
    df.dropna(subset = ["price", "stock"], inplace = True)
    df.sort_values("price", ascending = False, inplace = True)
    return df
    
def save_reports(df):
    df.to_csv(OUTPUT_FILE_1, index = False)
    category_report = (
        df.groupby("category", as_index=False).agg(
            average_price = ("price", "mean"),
            total_stock = ("stock", "sum")
        )    
    )
    category_report.to_csv(OUTPUT_FILE_2, index=False)
    
def main():
    products = fetch_all_products()

    if products is None:
        return
    
    df  = clean_products(products)    
    save_reports(df)

if __name__ == "__main__":
    main()
