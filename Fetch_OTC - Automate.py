import requests
import json
import os
from datetime import datetime

# משיכת המפתח מסביבת הענן המאובטחת (כדי שלא יהיה חשוף בקוד)
API_KEY = os.environ.get('TASE_API_KEY')

BASE_URL = "https://datawise.tase.co.il"
HEADERS = {
    'accept': 'application/json',
    'accept-language': 'he-IL',
    'apikey': API_KEY
}

def fetch_and_save_otc_data():
    now = datetime.now()
    current_time_str = now.strftime('%d-%m-%Y_%H-%M-%S')
    print(f"[{now.strftime('%H:%M:%S')}] Executing API call...")
    
    transactions_endpoint = f"{BASE_URL}/v1/transactions/otc-transactions-online"
    
    # הגדרת פרמטרי הזמן שגילינו לכיסוי כל יום המסחר
    params = {
        "fromTime": "09:00:00",
        "toTime": "17:30:00"
    }
    
    try:
        # הוספת משתנה ה-params לבקשת ה-GET
        response = requests.get(transactions_endpoint, headers=HEADERS, params=params)
        
        if response.status_code == 200:
            data = response.json()
            filename = f"otc_data_{current_time_str}.json"
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Success! Data successfully saved to '{filename}'")
        else:
            print(f"Failed to fetch data | Status code: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_save_otc_data()
