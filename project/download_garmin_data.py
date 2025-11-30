import requests
import time
from datetime import date, timedelta # Added for date handling

# --- Configuration ---
# WARNING: Always ensure you have the explicit legal right and authorization
# (e.g., API key, documented method, or accessing your own data through a
# dedicated, sanctioned method) before scraping or accessing proprietary APIs.
# Using session cookies obtained manually is generally against service Terms of Use.

# Base URL template for the API call. The date placeholder will be filled dynamically.
# Original structure: /gc-api/download-service/files/wellness/YYYY-MM-DD
BASE_API_URL_TEMPLATE = "https://connect.garmin.com/gc-api/download-service/files/wellness/{date_str}"

# 1. Define the custom headers required for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': '*/*',
    'connect-csrf-token': 'a1a8707d-bce4-4d59-99ec-27ff220c41e2'
}

# 2. Define the cookies required for authentication
# Replace the placeholder values with the actual session tokens you have.
cookies = {
    'SESSIONID': 'MDIwZTk2MTAtODY3Yy00M2YyLTg1NGQtMzU5OTEyNWUwOWQw',
    'session': 'Fe26.2*1*a7b08a9ecea3ee70bd5496eee8a1802ab18f2d50ffc36ff26195ba4c884860b2*y5G9Q5-ui0AXR7jnhrfuOQ*lNn9UVVb2jVc60WiwS2Btgc-au-LdpXIpqKvRXFgL9bkNkWO1XyMiPItO-pswroc4dtojH-NvXeV4SOtZfapZxsBdnrQ-WBI-tcdwCm1THyOzz7iAyTu0CXtIB2YI8d5QtNmqvQUhWUGvJclj0wGRMaZDJj9QrRn5zAgT0ql30EuadN9Hxhe4vmu9y9nxUGkQNE-_nhPWMDvg1zB5mTRWGJ4NN33Vg-JWe_tGK959dWJVXLiCh48ylJKyzf7OnEfPcC-p9oAFXb6Y7Y0j4SUe8SJgAlRLkMJVAVyn4UOfQmPo-ebCuiuuE2A-PPo7t0-O_lzNoSvnuBRVtIXBw-Y9Cvj8Fk14jjZAAoF6cLEu0un-1ffzb4ko8x2_LD6XzL5LR4hNeEugLxHr05UE41ZNMNDameEaCyd5mHEVt_odTW9uqUSjJQ8XnJxuApJMvibxQgOnoaqO5V_XquzY6ajY85XDMPJCb7PF5EMICkyKfr6aM6KgxjyylpZ7-TDKHxDG5ChFJ1uq_mvo1E7qq8HuE3JgX6rgVlS8CXS02XlII_KdxLw8zefmBE67rVFNIBvPEvRTBYaP2GRKhIAKdoVgRnqeb9SCTVaUeRrz9qkva9NyGdQ3vAasaLr2_QFQMVo9lz6qWQdZrnOFXczrYPT7GxsKOcj987aDXJjU5hlgav9_MDbp5R9I1uya87ouPYpJA4ISYHIyaZuxiZ7DO17L_M5qGovfz3_zNbChkGnt25daxYDy26rqb-8JyRfEFpIxGR51dusEZI7ZjNWVzt7iAy_ski6PnHoSLZeKlJuXoZwitPNhmYXKlG_oSlLJ4LBNrCIslQY85CDvfsNAdtoAwToOf64_M0guiy5YqYD6tVlwYsXLTA2R0j-gKbwYcTa63E6MZTD7PTrOl8KCgavrFlurGpth2j0To4ZCtCjj00G4rLiQNGef_BN2LAb0JC8D5Mmq-PPymTsQvJZMx9KH971H3bLiuL_dpjn_9Sj_ndTQrCraXwrljawLg9ighHlJDzB-lMhWlXEY0JE4uxXK-jMMwvx20cmuFG_Weej7oL1cZeBVH0Xt1ccfXhGBpDaxeh2jCTE-SbQ9mVUwwPJgkAvzXbizgQJHwV9d8IU-Z_Dy3Sxt8KBRiZFvsBOYjKPdWQMestuYlzzfaog_ESdHIrEXgLs9lwi90e2rfhjDgUFXO368g8-tOAhOB6L0Gb9b8Fg4NmsWBiPiwm3Xhf8KErT43t3aHRqC7mGSHufIrnP8Q5bArKPDCc5oBETCeVBsF3nmjkl6JqQk8abm6rXs2bu2sRkshG1-nk36nSDvvkoqSvq7MtJQNVqPkZpR8FWFA5E9hR-0JsBWBsFvL8HOP22wLpYnYjH49RVcyzf6De7CNQH2b1McGz7Xc1BaS9EW35gSBPN8fFaOOc-dwNpsZaaJXXIXzfcI3Z7P6XjLvlFZj-gNmlKPJf5vNlfhTlsypzJRsCa4eetw4d3agy_orW-nlf3mhVBMj6Yr-ar44tEUk48ew1Rvk8ghGa_bLxuZIwrf0UD2qeU4Cttug-rzVvAz8HKhgWXcshbaxd7PJho1hm4XxU0iNJUczLr6STdhDYe-haJi6Ia6zSh00B7cz669zibTO32hgI1ruqgByd08e17Xntm9J1gzevGQMl-BwqBiFmPCJ0JIzN-SffEfoBfWjzp6QllQzzn0epQ5XZTQmwPc7Vt_xcpAVA1NAgjWPIqS_NfA4d8yLRaLeVhNuE9cu-RedTPv7pKpKvbsChXliwMnhBZRnjQpyACxos4NYZVlOJsJvKpjA-JtRTZmV8xbPEgz55wvUfPKb44msSwvH1Re3t0CXS2tSTn3WohRiuW2LC4PDIkKs0EJoLrTb90WLnmstOK4xESgd_eBIa9bb1ucD4JuKLBoXxf6nW-qH3mTt2SBlCJ8Tp3s1gX07bmuexpLpdMuxWBb7CeS51RrYHhga_wip34KTf3wBr71JxW_Rb_nQxyt3lWAdwrVsAa4REu7SlHkCPawwm5NlOe4JZfs0VRynJFuhCHef-PyoFFDuUHFcZsBCY-mylWXeEu2vcUe8NjknfZ_wYPF7-TamEP7kFae6-qgWz1tDvzAYxGWT9GjbbyA6ctekbQBZrCZ54USN-hJ7HsZuWjaddrsCd11Z96nVLV8BfrTRcjRHhFd8bXaZafWZLVXIH3PeUwRqgUFG6OdT9ISQuLFhbdw4J2AEdKpKCUvAOr-jvRX9LdxR0_fuLV3ejKyXp8eO6owWgFsmYF6ot1xqC3UThRSjt-LsxYO-IfPBVJ2Jg7bvjKuLUkalcy9_SxxqHCFZ3IjmmBwykAbYLqfC14TmsRGl8w9Uws0r02wD4CZlEDW2rMpdgEYBYrYbTJezF79vAa776fN1apC9R_zub3tCVrxxD7sLqtv024cnbkErTI*1771313728842*a7fbbfb4f677115b0a7ec9846f35efbd9a2dbb5b94529b97048e2fc1a75b778a*yW0ej6EP6Yqj1VUodf7PZxHq-SuGGFQ2IhBzAjVau1s~2',
    'JWT_WEB': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQxMjE5NDAsImlzcyI6ImF1dGgwIiwicm9sZXMiOlsiNCIsIjciLCI4IiwiOSIsIjI4Il19.kJn56XZeCLkaOazzGnw7OjJZrCDuiTILFFSEyLpHQb8',
    'ADRUM_BTa': 'R:42|g:7923c020-8d25-4e13-8329-9175b0f1d1e5|n:garmin_869629ee-d273-481d-b5a4-f4b0a8c4d5a3',
    'GARMIN-SSO-CUST-GUID': '57dbf333-b034-4eca-a63b-37aab31ae934',
    'ADRUM_BT1': 'R:42|i:1292379|e:2|t:1764114741787'
}

# --- Function to make the API call for a single date ---
def fetch_api_data(url, cookies, headers, output_filename):
    """
    Makes a GET request to the specified API and saves the response content.
    """
    print(f"\nAttempting to fetch data from: {url}")

    # Simple retry mechanism for transient network errors
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Use requests.get() with cookies and headers arguments
            response = requests.get(url, cookies=cookies, headers=headers, timeout=15)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                print(f"[{url.split('/')[-1]}] Success (Status 200 OK).")

                # The API returns a file (wellness data), so we save the raw content
                with open(output_filename, 'wb') as f:
                    f.write(response.content)

                print(f"[{url.split('/')[-1]}] Data saved to {output_filename}")
                return # Exit on success

            elif response.status_code == 401:
                print(f"[{url.split('/')[-1]}] Error: 401 Unauthorized. Check if your cookies are current and valid.")
                return # Unauthorized is usually not retryable
            elif response.status_code == 404:
                print(f"[{url.split('/')[-1]}] Error: 404 Not Found (No data for this date?).")
                return # Not found is not retryable
            else:
                print(f"[{url.split('/')[-1]}] Request failed with status code: {response.status_code}. Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt) # Exponential backoff

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"[{url.split('/')[-1]}] Network error: {e}. Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)
            else:
                print(f"[{url.split('/')[-1]}] Failed after {max_retries} attempts. Last error: {e}")

# --- New function to handle multiple dates ---
def fetch_data_for_date_range(start_date_str: str, end_date_str: str, base_url_template: str, cookies: dict, headers: dict):
    """
    Iterates through a date range, constructing the URL and fetching data for each day.
    """
    print("-" * 50)
    print("Starting batch data fetch for date range...")
    print("-" * 50)

    try:
        # Convert string dates to date objects
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
    except ValueError:
        print("Error: Date strings must be in ISO format (YYYY-MM-DD).")
        return

    # Iterate through every date from start_date to end_date (inclusive)
    current_date = start_date
    while current_date <= end_date:
        # 1. Format the current date into the required YYYY-MM-DD string
        date_str = current_date.isoformat()

        # 2. Construct the full URL using the template
        full_url = base_url_template.format(date_str=date_str)

        # 3. Define a unique output filename for each day
        output_file = f"downloaded_zips/wellness_data_{date_str}.zip"

        # 4. Call the single-fetch function
        fetch_api_data(full_url, cookies, headers, output_file)

        # Move to the next day
        current_date += timedelta(days=1)

    print("\n" + "=" * 50)
    print("Batch fetching complete.")
    print("=" * 50)


# --- Main execution block ---
if __name__ == "__main__":

    # --- Example Usage for the new batch method ---
    # Define the range of dates you want to fetch.
    START_DATE = "2025-01-27"
    END_DATE = "2025-11-25"

    # Call the new function to fetch data for the date range
    fetch_data_for_date_range(
        start_date_str=START_DATE,
        end_date_str=END_DATE,
        base_url_template=BASE_API_URL_TEMPLATE,
        cookies=cookies,
        headers=headers
    )