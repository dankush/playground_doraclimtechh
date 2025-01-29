import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# Constants
API_URL = 'https://air.sviva.gov.il/home/MonitorsVal'
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'ASP.NET_SessionId=tiqkt4zklpmz1kaoxqnda5su; _ga=GA1.1.1441635063.1738095169; __RequestVerificationToken=YiRzB0C6l1CO5x_4lZO3To_-x84XK43benv3KDjPx2myCUxww0ZvpMxFfX7Y6MECa2ZwD4t6c4damklk3M1lZ7kxkXs7EwZBZW2gqw6nDwc1; __FormVerificationToken=Jr6q1e3DB7iSrlEMlzS7Dksl1QmhUp9CCFmDx21P6PX8DLG7mJ5olQjs_UqL7fzf-1KFoNHIDYEkJlS9LmmbqBuPDYacKCCiozsidM29PAs1; _ga_WGE8CEE6C3=GS1.1.1738095168.1.1.1738095313.0.0.0',
    'origin': 'https://air.sviva.gov.il',
    'priority': 'u=1, i',
    'referer': 'https://air.sviva.gov.il/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-requestverificationtoken': 'Jr6q1e3DB7iSrlEMlzS7Dksl1QmhUp9CCFmDx21P6PX8DLG7mJ5olQjs_UqL7fzf-1KFoNHIDYEkJlS9LmmbqBuPDYacKCCiozsidM29PAs1'
}

# Function to create the payload for a specific date
def create_payload(date):
    payload = (
        'UserStation=%7B%22IP%22%3Anull%2C%22STA_O3Factor%22%3A0%2C%22STA_O3BFactor%22%3A0%2C%22GIS_Monitors%22%3Anull%2C%22GIS_channel%22%3Anull%2C%22GIS_Units%22%3Anull%2C%22GIS_LastRecivedValues%22%3Anull%2C%22FileName%22%3Anull%2C%22ImageDescription%22%3Anull%2C%22ImageStatus%22%3Anull%2C%22NonContinuous%22%3Afalse%2C%22STA_ImageData%22%3A%22System.Byte%5B%5D%22%2C%22AQSCODE%22%3Anull%2C%22STA_Notes%22%3A%22%22%2C%22asix%22%3Anull%2C%22DateVal%22%3A%22{date} 22%3A00%22%2C%22IndexIcon%22%3Anull%2C%22dateDisplay%22%3A%22{date_display} 22%3A00%22%2C%22environment%22%3A%22%22%2C%22StGroup%22%3Anull%2C%22StGroupName%22%3A%22%D7%A9%D7%A4%D7%9C%D7%94+%D7%A4%D7%A0%D7%99%D7%9E%D7%99%D7%AA%22%2C%22CBO_ItemIndex%22%3A0%2C%22Active%22%3A1%2C%22ListIndex%22%3Anull%2C%22display%22%3Atrue%2C%22Active_%22%3Afalse%2C%22serialCode%22%3A64%2C%22DisplayName%22%3Anull%2C%22name%22%3A%22%D7%9E%D7%95%D7%93%D7%99%D7%A2%D7%99%D7%9F%22%2C%22location%22%3A%22%D7%9E%D7%AA%D7%A7%D7%9F+%D7%9E%D7%A7%D7%95%D7%A8%D7%95%D7%AA+%D7%9E%D7%95%D7%93%D7%99%D7%A2%D7%99%D7%9F%22%2C%22city%22%3A%22%D7%9E%D7%95%D7%93%D7%99%D7%A2%D7%99%D7%9F%22%2C%22county%22%3Anull%2C%22height%22%3A%22262%22%2C%22latitude%22%3A%2231.89295205%22%2C%22longitude%22%3A%2234.99531847%22%2C%22IndexColor%22%3A%22%23FFFF00%22%2C%22IndexName%22%3A%22%D7%91%D7%99%D7%A0%D7%95%D7%A0%D7%99%D7%AA%22%2C%22timebase%22%3A5%2C%22owner%22%3A%22%D7%97%D7%91%D7%A8%D7%AA+%D7%97%D7%A9%D7%9E%D7%9C%22%2C%22IndexValue%22%3A38.0%2C%22UseMapView%22%3A1%2C%22UseIndex%22%3Atrue%2C%22IndexValueDateTime%22%3Anull%2C%22STA_Target%22%3A%22%D7%9B%D7%9C%D7%9C%D7%99%D7%AA%22%2C%22TargetId%22%3A0%2C%22RegionId%22%3A0%2C%22monitors%22%3A%5B%7B%22channel%22%3A1%2C%22type%22%3A49%2C%22value%22%3A%223.5%22%2C%22Lastvalue%22%3A%223.5%22%2C%22state%22%3A1%2C%22name%22%3A%22SO2%22%2C%22unit%22%3A%22%C2%B5g%2Fm%C2%B3%22%2C%22stationSerialCode%22%3A64%2C%22stationName%22%3A%22%D7%9E%D7%95%D7%93%D7%99%D7%A2%D7%99%D7%9F%22%2C%22owner%22%3A%22%D7%97%D7%91%D7%A8%D7%AA+%D7%97%D7%A9%D7%9E%D7%9C%22%2C%22Color%22%3A%2200E400%22%2C%22IndexIcon%22%3Anull%2C%22indexVal%22%3A99%2C%22TimeBase%22%3A60%2C%22StationTimeBase%22%3A0%2C%22DateVal%22%3A%22{date} 22%3A00%22%2C%22NumericFormat%22%3A5.1%2C%22Pollutantname%22%3A%22SO2%22%2C%22Description%22%3A%22%D7%92%D7%95%D7%A4%D7%A8%D7%99%D7%AA+%D7%93%D7%95+%D7%97%D7%9E%D7%A6%D7%A0%D7%99%D7%AA%22%2C%22asix%22%3Anull%2C%22isPolPos%22%3Afalse%2C%22PollutantTimeBase%22%3A60%2C%22PollutantID%22%3A4%2C%22PctValid%22%3A75%2C%22Active%22%3A1%2C%22UseMapView%22%3A1%2C%22isIndex%22%3Atrue%2C%22indexName%22%3A%22%D7%98%D7%95%D7%91%D7%94%22%2C%22StationTag%22%3A%2225%22%2C%22ShortName%22%3A%22%D7%9E%D7%95%D7%93%D7%99%D7%A2%D7%99%D7%9F%22%2C%22County%22%3A%22%D7%A9%D7%A4%D7%9C%D7%94+%D7%A4%D7%A0%D7%99%D7%9E%D7%99%D7%AA%22%2C%22MON_Desc%22%3A%22%22%2C%22AQSCODE%22%3Anull%2C%22MonitorTitle%22%3Anull%2C%22MON_EndDate%22%3A%2231%2F12%2F9999+23%3A59%3A59%22%2C%22MON_StartDate%22%3A%2231%2F12%2F9999+23%3A59%3A59%22%2C%22Exceedance15Min%22%3A-9999%2C%22Exceedance1hLow%22%3A-9999%2C%22Exceedance1hHigh%22%3A-9999%2C%22Exceedance8h%22%3A-9999%2C%22Exceedance1440h%22%3A-9999%2C%22ExceedanceYears%22%3A-9999%2C%22ExceedanceNumDays%22%3A0%2C%22ExceedanceNumMinutes%22%3A0%2C%22ExceedanceNum8Hours%22%3A0%2C%22ExceedanceNumHours%22%3A0%2C%22Exceedance8hYear%22%3A0%2C%22Exceedance1hYear%22%3A0%2C%22Exceedance15MinYear%22%3A0%2C%22Exceedance1440hYear%22%3A0%2C%22ExceedanceYearsYear%22%3A0%2C%22StationActive%22%3Afalse%2C%22LowRange%22%3Anull%2C%22HighRange%22%3Anull%7D%5D%2C%22monitorsDataDateTime%22%3Anull%2C%22StationTag%22%3Anull%2C%22ShortName%22%3Anull%2C%22pollutant%22%3Anull%7D&days=1&type=&UserDate={user_date}&AddTime=&Monthly=false&MonitorsVal=false&SelectedPollutant=&ForIndex=True&id=-1&timebase=5'
    )
    date_display = datetime.strptime(date, '%Y/%m/%d').strftime('%d/%m/%Y')
    return payload.format(date=date, date_display=date_display, user_date=date)

# Function to fetch data for a specific date
def fetch_data(session, date):
    payload = create_payload(date)
    try:
        response = session.post(API_URL, headers=HEADERS, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed for date {date}: {e}")
        return None

# Function to process the response and extract S_64_0 values
def process_response(data):
    if not data or "ListDic" not in data:
        return None
    records = data["ListDic"]
    s_64_0_values = [record["S_64_0"] for record in records if "S_64_0" in record]
    if not s_64_0_values:
        return None
    average = sum(s_64_0_values) / len(s_64_0_values)
    return average

def main():
    # Calculate the date three months ago
    today = datetime.today()
    three_months_ago = today - timedelta(days=90)

    # Prepare a list of dates from three_months_ago to today
    date_list = [(three_months_ago + timedelta(days=x)).strftime('%Y/%m/%d') for x in range(0, (today - three_months_ago).days +1)]

    # Initialize a session
    session = requests.Session()

    # List to store results
    results = []

    for date in date_list:
        print(f"Fetching data for {date}...")
        data = fetch_data(session, date)
        average = process_response(data)
        if average is not None:
            results.append({
                'date': date,
                'daily_avg_S_64_0': average
            })
            print(f"Date: {date}, Daily Avg S_64_0: {average}")
        else:
            print(f"No data available for {date}.")
        # Optional: sleep to avoid hitting rate limits
        time.sleep(1)  # Sleep for 1 second between requests

    # Create a DataFrame
    df = pd.DataFrame(results)

    # Save to CSV
    df.to_csv('daily_avg_S_64_0_last_3_months.csv', index=False)
    print("Data saved to daily_avg_S_64_0_last_3_months.csv")

if __name__ == "__main__":
    main()