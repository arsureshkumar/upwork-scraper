from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from time import sleep
import pandas as pd

edgeOptions = Options()
edgeOptions.headless = True

driver = webdriver.Edge(options = edgeOptions)
driver.get("https://www.paulaschoice.com/shop-ingredient")


wait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "root")))

sleep(3)
driver.switch_to.active_element.send_keys(Keys.TAB, Keys.TAB, Keys.ENTER)

wait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[5]/div[1]/div[2]/div[2]/span''')))
for i in range(2, 6):
    more_button = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[5]/div[1]/div[''' + str(i) + ''']/div[2]/span''')
    more_button.click()


links = []

for i in range(2, 6):
    cats = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[5]/div[1]/div[''' + str(i) + ''']/div[2]''')
    links.extend(cats.find_elements(By.TAG_NAME, "a"))

links = [i.get_attribute('href') for i in links]

prod_info_total = pd.DataFrame(columns = ['product', 'description', 'tags'])

for i in links:
    driver.get(i)
    
    try:

        sleep(1)

        products = driver.find_element(By.XPATH, '''/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[5]/div[2]/div[3]''')
        product_links = [i.get_attribute('href') for i in products.find_elements(By.TAG_NAME, "a")]

    except:

        driver.switch_to.active_element.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
        sleep(1)

        products = driver.find_element(By.XPATH, '''/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[5]/div[2]/div[3]''')
        product_links = [i.get_attribute('href') for i in products.find_elements(By.TAG_NAME, "a")]

    for j in product_links:

        try:

            prod_info = {}
            driver.get(j)

            heading = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/h1/div''')
            prod_info['product'] = heading.text

            description = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[3]/div''')
            prod_info['description'] = description.text
            
            prod_info['tags'] = i
            print(prod_info)
            prod_info_total = prod_info_total.append(prod_info, ignore_index = True)

        except:
            
            driver.switch_to.active_element.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
            sleep(1)
            
            prod_info = {}
            driver.get(j)

            heading = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/h1/div''')
            prod_info['product'] = heading.text

            description = driver.find_element(By.XPATH, '''//*[@id="root"]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[3]/div''')
            prod_info['description'] = description.text
            
            prod_info['tags'] = i
            print(prod_info)
            prod_info_total = prod_info_total.append(prod_info, ignore_index = True)

sleep(3)

def tag_processor(url):
    url = url[(url.rfind('=') + 1):]
    url = url.replace('%20', ' ').replace('%26', '&')
    return(url)

prod_info_total['tags'] = prod_info_total['tags'].map(tag_processor)
prod_info_total['tags'] = prod_info_total.groupby(['product','description'])['tags'].transform(lambda x: ', '.join(x))
prod_info_total = prod_info_total.drop_duplicates('product')
prod_info_total.to_csv('prod_info.csv')