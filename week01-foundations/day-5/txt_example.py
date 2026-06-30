
with open("notes.txt", "w") as file:
    file.write("Hello Krish!\n")
    file.write("Welcome to Day 5.")

with open("notes.txt", "r") as file:
    content = file.read()

print(content)

open("file.txt", "w")

import json

student = {
    "name": "Krish",
    "age": 21,
    "city": "Mumbai"
}

with open("student.json", "w") as file:
    json.dump(student, file, indent=4)

import json

with open("student.json", "r") as file:
    data = json.load(file)

print(data)
print(data["name"])

import csv

rows = [
    ["name", "age", "city"],
    ["Krish", 21, "Mumbai"],
    ["John", 22, "Pune"]
]

with open("students.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(rows)

import csv

with open("students.csv", "r") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)

data = {
    "location": {
        "city": "Mumbai",
        "country": "India"
    },
    "weather": {
        "temperature": 30,
        "humidity": 80
    }
}

city = data["location"]["city"]

temperature = data["weather"]["temperature"]

print(city)
print(temperature)

response = {
    "main": {
        "temp": 29,
        "humidity": 75
    },
    "weather": [
        {
            "main": "Clouds"
        }
    ]
}

temp = response["main"]["temp"]

humidity = response["main"]["humidity"]

condition = response["weather"][0]["main"]

print(temp)
print(humidity)
print(condition)

import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/users"
)

print(response.status_code)

import requests

try:
    response = requests.get(
        "https://wrong-url.com",
        timeout=5
    )

    response.raise_for_status()

    print(response.json())

except requests.exceptions.Timeout:
    print("Request timed out")

except requests.exceptions.RequestException as e:
    print("Request failed:")
    print(e)

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

print(api_key)

import json
import os

from dotenv import load_dotenv

load_dotenv()

data = {
    "name": "Krish",
    "course": "Python"
}

with open("practice.json", "w") as file:
    json.dump(data, file, indent=4)

with open("practice.json", "r") as file:
    loaded = json.load(file)

print(loaded)

print(os.getenv("API_KEY"))


