from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import random
import time

def add_to_json(new_data, filename="data.json"):
 """
 Adds new data to a JSON file, only if the specified name doesn't already exist.

 Args:
   filename (str): The name of the JSON file to modify.
   new_data (dict): The new data to add to the JSON file, as a dictionary.
 """

 try:
   with open(filename, "r") as file:
     data = json.load(file)
 except FileNotFoundError:
   data = []

 exists = any(item["name"] == new_data["name"] for item in data)

 if not exists:
   data.append(new_data)

   with open(filename, "w") as file:
     json.dump(data, file, indent=4) 
 else:
   # Indicate that the name already exists
   print(f"Name '{new_data['name']}' already exists in {filename}. Data not added.")

def get_value(name, filename="data.json"):
  try:
    with open(filename, "r") as file:
      data = json.load(file)
  except FileNotFoundError:
    data = []
  for item in data:
    if item["name"] == name:
      return item["value"]
  return None

chrome_options = Options()
path = r"adblock.crx"
chrome_options.add_extension(path)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.higherlowergame.com/")

# find element by xpath
driver.find_element(By.XPATH, '//*[@id="root"]/div/span/section/div[2]/div/button[1]').click()

# get value of element by xpath
#highButton = driver.find_element(By.XPATH, '//*[@id="root"]/div/span/span/div/div[2]/div[2]/button[1]')
#lowButton = driver.find_element(By.XPATH, '//*[@id="root"]/div/span/span/div/div[2]/div[2]/button[2]')
# playAgain = driver.find_element(By.XPATH, '//*[@id="game-over-btn"]')



while True:
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//*[@id="game-over-btn"]').click()
        time.sleep(2)
    except:
        pass
    
    leftName = driver.find_element(By.XPATH, '//*[@id="root"]/div/span/span/div/div[2]/div[1]/div[1]/div/div[1]/p[1]').text
    leftAmount = driver.find_element(By.XPATH, '//*[@id="root"]/div/span/span/div/div[2]/div[1]/div[1]/div/div[2]/p[1]').text
    searchTerm = driver.find_element(By.XPATH, '//*[@id="root"]/div/span/span/div/div[2]/div[1]/div[2]/div/div[1]/p[1]').text
    # remove commas from number
    leftAmount = leftAmount.replace(",", "")
    #remove " from starting and ending of string
    searchTerm = searchTerm[1:-1]
    leftName = leftName[1:-1]
    leftVal = {
        "name": leftName,
        "value": leftAmount
    }
    add_to_json(leftVal)
    if get_value(searchTerm) == None:
        print(f"search term not found {searchTerm}")
        # randomly guess between high and low
        guess = random.choice(['//*[@id="root"]/div/span/span/div/div[2]/div[2]/button[1]', '//*[@id="root"]/div/span/span/div/div[2]/div[2]/button[2]'])
        driver.find_element(By.XPATH, guess).click()
        time.sleep(2)
        try:
           playAgain = driver.find_element(By.XPATH, '//*[@id="game-over-btn"]').click()
        except:
            pass
    else:
        if int(leftAmount) < int(get_value(searchTerm)):
            print(f"guessing high")
            driver.find_element(By.XPATH, '//*[@id="root"]/div/span/span/div/div[2]/div[2]/button[1]').click()
        else:
            print(f"guessing low")
            driver.find_element(By.XPATH, '//*[@id="root"]/div/span/span/div/div[2]/div[2]/button[2]').click()
        time.sleep(2)

