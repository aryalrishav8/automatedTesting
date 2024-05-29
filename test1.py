import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


from time import sleep

# Set options for not prompting DevTools information
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

print("testing started")
driver = webdriver.Chrome(options=options)

driver.get("https://arms-qa.deerwalk.edu.np")

def login():
    dropdown=driver.find_element(By.ID, "role")
    select=Select(dropdown)
    select.select_by_visible_text("Admin")

    email=driver.find_element(By.NAME,"email")
    email.send_keys("admin@sifal.deerwalk.edu.np")

    password=driver.find_element(By.NAME,"password")
    password.send_keys("password")

    driver.find_element(By.XPATH,"/html/body/main/div/div[2]/form/div/div[5]/button").click()
    sleep(5)


    role=driver.find_element(By.XPATH,'//*[@id="navbar"]/button/div[1]/p[2]')
    role_text=role.text

    assert role_text== "Admin", f"Not logged in"

    print("Login completed successfully")


def create_user():
    hamburg=driver.find_element(By.XPATH,'/html/body/div/div/nav/button/img')
    hamburg.click()
    user_icon=driver.find_element(By.XPATH,'/html/body/div/div/nav/div/a[2]')
    user_icon.click()
    add_user=driver.find_element(By.XPATH,'/html/body/div/main/div/div[1]/div/a')
    add_user.click()
    driver.find_element(By.NAME,'name').send_keys('Python Test')
    driver.find_element(By.NAME,'email').send_keys('python@gmail.com')
    checkbox=driver.find_element(By.XPATH,'/html/body/div/main/div/div[2]/div/div/form/div/div[3]/div/label[1]/input').click()
    upload=driver.find_element(By.ID,'signature')
    file_path=os.path.abspath(r"C:\users\dell\Downloads\canva.png")
    upload.send_keys(file_path)
    driver.find_element(By.XPATH,'/html/body/div/main/div/div[2]/div/div/form/div/div[5]/button').click()

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="myTable_wrapper"]/div[2]')))    
    element_text = element.text
    assert "Python Test" in element_text, f"Expected 'Python Test' to be in the element text, but got '{element_text}'"
    print("Text assertion passed. 'Python Test' is present in the element.")
    sleep(5)
    driver.quit()

def delete_user():
    hamburg=driver.find_element(By.XPATH,'/html/body/div/div/nav/button/img')
    hamburg.click()
    user_icon=driver.find_element(By.XPATH,'/html/body/div/div/nav/div/a[2]')
    user_icon.click()
    search=driver.find_element(By.XPATH,'//*[@id="dt-search-0"]')
    search.send_keys('Python')
    delete=driver.find_element(By.XPATH,'//*[@id="delete-9"]/button')
    delete.click()
    confirm=driver.find_element(By.XPATH,'/html/body/div[2]/div/div[6]/button[1]')
    confirm.click()
    sleep(4)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="myTable_wrapper"]/div[2]')))    
    element_text = element.text    
    if "Python Test" not in element_text:
        print("Success in deleting user")
    else:
        print("User not deleted")    
    driver.quit()


# def delete_student():
#     hamburg=driver.find_element(By.XPATH,'/html/body/div/div/nav/button/img')
#     hamburg.click()
#     student=driver.find_element(By.XPATH,'/html/body/div/div/nav/div/a[11]')
#     student.click()
#     active_rows=[]
    
#     body=driver.find_element(By.XPATH,'/html/body/div/main/div')
#     table=driver.find_element(By.XPATH,'//*[@id="myTable"]/tbody')
#     rows=table.find_elements(By.XPATH,'.//tr')
#     for row in rows:
#         status_cell=row.find_element(By.XPATH,'.//td[5]')
#         status=status_cell.text.strip()
#         if status=='Active':
#             active_rows.append(row)

#         for row in active_rows:
#             delete=driver.find_element(By.XPATH,'.//button[contains(text(),"Delete")]')
#             delete.click()
#             confirm=driver.find_element(By.XPATH,'//button[contains(text(),"Yes, delete it")]')
#             confirm.click()
#             sleep(5)
#             print("Student Deleted")
#             search=driver.find_element(By.XPATH,'//*[@id="dt-search-0"]')
#             search.send_keys('Tushar')

        
   
def delete_active_students():
    global active_rows  # Allow modification of the global variable
    
    hamburg = driver.find_element(By.XPATH, '/html/body/div/div/nav/button/img')
    hamburg.click()
    student = driver.find_element(By.XPATH, '/html/body/div/div/nav/div/a[11]')
    student.click()
    search = driver.find_element(By.XPATH, '//*[@id="dt-search-0"]')
    search.send_keys('Tushar')
    table = driver.find_element(By.XPATH, '//*[@id="myTable_wrapper"]/div[2]/div')
    rows = table.find_elements(By.XPATH, './/tr')
    
    for row in rows:       
        status_cell = row.find_element(By.XPATH, './/td[5]//span')
        status = status_cell.text.strip()
        if status == "Active" and row not in active_rows:
            active_rows[row] = "active"  # Store active rows in the dictionary
    
    for row, status in active_rows.items():
        if status != "deleted":
            delete_button = row.find_element(By.XPATH, './/button[contains(text(), "Delete")]')
            delete_button.click()
            confirm = driver.find_element(By.XPATH, '//button[contains(text(),"Yes, delete it")]')
            confirm.click()
            sleep(5)
            print("Student Deleted")
            search = driver.find_element(By.XPATH, '//*[@id="dt-search-0"]')
            search.clear()
            search.send_keys('Tushar')
            active_rows[row] = "deleted"  # Update status in the dictionary
            
            





active_rows = {}
login()
while True:
    delete_active_students()
    if all(status == "deleted" for status in active_rows.values()):
        break




