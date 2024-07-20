import requests
import datetime

# API credentials
APP_ID = "your_app_id"  # Replace with your Nutritionix API App ID
API_KEY = "your_api_key"  # Replace with your Nutritionix API Key
USERNAME = "your_username"  # Replace with your Sheety API username
PASSWORD = "your_password"  # Replace with your Sheety API password

# Constants for exercise tracking
GENDER = "Male"
WEIGHT_KG = 70
HEIGHT_CM = 187
AGE = 20

# Endpoints for APIs
nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = "https://api.sheety.co/your_sheety_endpoint/workoutTracking/workouts"

# Get user input for exercises
exercise_text = input("What types of exercises did you do: ")

# Headers for Nutritionix API request
headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
    'Content-Type': 'application/json'
}

# Parameters for Nutritionix API request
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

# Send request to Nutritionix API
response = requests.post(url=nutritionix_endpoint, json=parameters, headers=headers)
result = response.json()  # Parse the JSON response

# Get current date and time
today_date = datetime.datetime.now().strftime("%d/%m/%Y")
now_time = datetime.datetime.now().strftime("%X")

# Loop through the exercises returned by Nutritionix API
for exercise in result["exercises"]:
    # Prepare data to log into Google Sheets
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Send request to Sheety API to log exercise data
    sheet_response = requests.post(
        sheety_endpoint,
        json=sheet_inputs,
        auth=(USERNAME, PASSWORD)  # Basic Authentication for Sheety API
    )
    
    # Check the response status
    if sheet_response.status_code != 200:
        print("Error:", sheet_response.json())  # Print error message if request failed
    else:
        print(sheet_response.text)  # Print success message if request succeeded
