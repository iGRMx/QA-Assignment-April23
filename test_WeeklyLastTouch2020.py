from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time

from selenium.webdriver.chrome.options import Options

import pytest


#--Chrome Browser
service_obj = Service("O:\QA\chromedriver_win32\chromedriver.exe")
driver = webdriver.Chrome(service=service_obj)
driver.implicitly_wait(5)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

#login
driver.get("https://app.roivenue.com/explore/process/")
driver.find_element(By.ID, "Username").send_keys("imuravyevmail@gmail.com")
driver.find_element(By.ID, "Password").send_keys("qD6MPfKtzwWbV8t")
driver.find_element(By.ID, "tracking-button-submit").click()
#wait = WebDriverWait(driver,18)
#wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "button[id='attributionButton'] span:nth-child(1)")))
time.sleep(18)
driver.maximize_window()


#currency switch -> CZK
driver.find_element(By.ID, "tracking-menu-group-settings").click()
driver.find_element(By.ID, "tracking-menu-item-personalSettings").click()
time.sleep(3)
driver.find_element(By.ID, "tracking-user-settings-currency-selector").click()
driver.find_element(By.XPATH, "(//span[@class='mat-option-text'])[39]").click()   #CZK option
driver.get("https://app.roivenue.com/explore/process/")
time.sleep(15)


#WeeklyLastTouch2020 test for CZK

#Model_LastTouch
driver.find_element(By.CSS_SELECTOR, "button[id='attributionButton'] span[class='mat-button-wrapper']").click() #open the menu
driver.find_element(By.XPATH, "(//span[@class='mat-radio-inner-circle'])[2]").click() #choose the option Last Touch, in brackets we can change our option 1,2,3,4
time.sleep(3)
#driver.find_element(By.XPATH, "(//div[@class='cdk-overlay-backdrop mat-overlay-transparent-backdrop cdk-overlay-backdrop-showing'])[1]").click() #remove the menu

#Granularity_Weekly
driver.find_element(By.CSS_SELECTOR, "roi-granularity-picker[class='ng-star-inserted'] span[class='mat-button-wrapper']").click() #open the menu
driver.find_element(By.XPATH, "//div[@class='cdk-overlay-container']//button[2]").click() #choose the option, in brackets we can change our option 1,2,3

#Period
driver.find_element(By.CSS_SELECTOR, "button[class='mat-focus-indicator mat-tooltip-trigger not-a-real-button mat-button mat-button-base'] span[class='mat-button-wrapper']").click()

#setting the start of the period
driver.find_element(By.ID, "tracking-date-range-picker-from-input").click()
driver.find_element(By.ID, "tracking-date-range-picker-from-input").clear()
driver.find_element(By.ID, "tracking-date-range-picker-from-input").send_keys("01/01/2020")

#setting the end of the period
driver.find_element(By.ID, "tracking-date-range-picker-to-input").click()
driver.find_element(By.ID, "tracking-date-range-picker-to-input").clear()
driver.find_element(By.ID, "tracking-date-range-picker-to-input").send_keys("31/12/2020")

#FinishPeriod
driver.find_element(By.ID, "tracking-date-range-picker-confirm-button").click()


#choosing Google Ads platform ONLY
driver.find_element(By.CSS_SELECTOR, "img[src='/assets/icons/hide_icon.svg']").click()
driver.find_element(By.XPATH, "(//mat-panel-title)[2]").click()
driver.find_element(By.CSS_SELECTOR, "input[placeholder='Find...']").send_keys("Google Ads")
driver.find_element(By.CSS_SELECTOR, ".mat-tooltip-trigger.name").click()
driver.find_element(By.XPATH, "//button[@class='mat-focus-indicator only-button mat-stroked-button mat-button-base']//span[@class='mat-button-wrapper']").click()


#extracting data from DB
#wait = WebDriverWait(driver,8)
#wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//tbody/tr[12]/td[3]")))
time.sleep(6)


#monthlyMarketingInvestment to self-check
months_CZK = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
for month in months_CZK:
    print(month.text)


#all months of MarketingInvestment
czk_sum = 0
for month in months_CZK:
    czk_text = month.text.split()[1]  #Extract CZK value from text
    czk_value = float(czk_text.replace(',', ''))  #Convert to float
    czk_sum += czk_value


print("Total CZK sum:", czk_sum)
czk_avg = czk_sum / len(months_CZK)
print("Total CZK avg:", czk_avg)


#monthlyMargin Return On Marketing Investment to self-check
MROMIs = driver.find_elements(By.XPATH, "//tbody/tr/td[3]")
num_MROMIs = []
for MROMI in MROMIs:
    print(MROMI.text)
    numeric_value = float(MROMI.text)
    num_MROMIs.append(numeric_value)


min_MROMIs = min(num_MROMIs)
max_MROMIs = max(num_MROMIs)


#all months of Margin Return On Marketing Investment
sum_MROMIs = 0
for MROMI in MROMIs:
    sum_MROMIs += float(MROMI.text)


avg_MROMIs = sum_MROMIs / len(MROMIs)

print("Avg MROMIs:", avg_MROMIs)
print("Min MROMIs:", min_MROMIs)
print("Max MROMIs:", max_MROMIs)


#UnderlineResults

#Sum
greatSumText = driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='sum'] td:nth-child(2)").text
greatSumValue = float(greatSumText.split()[1].replace(',', ''))
print("UnderlineSum CZK:", greatSumValue)

#Avg
greatAvgText = driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='avg'] td[class='summary-value']").text
greatAvgValue = float(greatAvgText.split()[1].replace(',', ''))
print("UnderlineAvg CZK:", greatAvgValue)

#Total of Margin Return On Marketing Investment
greatTotalMarginROI = float(driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='total'] td[class='summary-value']").text)
print("Underline Total of Margin Return On Marketing Investment:", greatTotalMarginROI)

#Min of Margin Return On Marketing Investment
greatMinMarginROI = float(driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='min'] td[class='summary-value']").text)
print("Underline Min of Margin Return On Marketing Investment:", greatMinMarginROI)

#Max of Margin Return On Marketing Investment
greatMaxMarginROI = float(driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='max'] td[class='summary-value']").text)
print("Underline Max of Margin Return On Marketing Investment:", greatMaxMarginROI)

#rounding
czk_sum = round(czk_sum, 2)
czk_avg = round(czk_avg, 2)
avg_MROMIs = round(avg_MROMIs, 2)
min_MROMIs = round(min_MROMIs, 2)
max_MROMIs = round(max_MROMIs, 2)


#Final Check for CZK
def test_equalityTableSumFinalSumMIczk():
    assert czk_sum == greatSumValue, "Equality of MITableSum and MIFinalSum failed in CZK"


def test_equalityTableAvgFinalAvgMIczk():
    assert czk_avg == greatAvgValue, "Equality of MITableAvg and MIFinalAvg failed in CZK"


def test_equalityTableAvgTotalMROMIczk():
    assert avg_MROMIs == greatTotalMarginROI, "Equality of TableAvgMROMIs and TotalMROMIs failed in CZK"


def test_equalityTableMinFinalMinMROMIczk():
    assert min_MROMIs == greatMinMarginROI, "Equality of TableMinMROMIs and FinalMinMROMIs failed in CZK"


def test_equalityTableMaxFinalMaxMROMIczk():
    assert max_MROMIs == greatMaxMarginROI, "Equality of TableMaxMROMIs and FinalMaxMROMIs failed in CZK"


#currency switch -> EUR
driver.find_element(By.ID, "tracking-menu-group-settings").click()
driver.find_element(By.ID, "tracking-menu-item-personalSettings").click()
time.sleep(3)
driver.find_element(By.ID, "tracking-user-settings-currency-selector").click()
driver.find_element(By.XPATH, "(//span[@class='mat-option-text'])[47]").click()   #EUR option
time.sleep(3)
driver.get("https://app.roivenue.com/explore/process/")


#WeeklyLastTouch test for EUR
wait = WebDriverWait(driver, 18)
wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "button[id='attributionButton'] span:nth-child(1)")))
time.sleep(16)


#Model_LastTouch
driver.find_element(By.CSS_SELECTOR, "button[id='attributionButton'] span[class='mat-button-wrapper']").click() #open the menu
driver.find_element(By.XPATH, "(//span[@class='mat-radio-inner-circle'])[2]").click() #choose the option Last Touch, in brackets we can change our option 1,2,3,4
time.sleep(3)
driver.find_element(By.XPATH, "(//div[@class='cdk-overlay-backdrop mat-overlay-transparent-backdrop cdk-overlay-backdrop-showing'])[1]").click() #remove the menu


#Granularity_Weekly
driver.find_element(By.CSS_SELECTOR, "roi-granularity-picker[class='ng-star-inserted'] span[class='mat-button-wrapper']").click() #open the menu
driver.find_element(By.XPATH, "//div[@class='cdk-overlay-container']//button[2]").click() #choose the option, in brackets we can change our option 1,2,3


#Period
driver.find_element(By.CSS_SELECTOR, "button[class='mat-focus-indicator mat-tooltip-trigger not-a-real-button mat-button mat-button-base'] span[class='mat-button-wrapper']").click()
#setting the start of the period
driver.find_element(By.ID, "tracking-date-range-picker-from-input").click()
driver.find_element(By.ID, "tracking-date-range-picker-from-input").clear()
driver.find_element(By.ID, "tracking-date-range-picker-from-input").send_keys("01/01/2020")

#setting the end of the period
driver.find_element(By.ID, "tracking-date-range-picker-to-input").click()
driver.find_element(By.ID, "tracking-date-range-picker-to-input").clear()
driver.find_element(By.ID, "tracking-date-range-picker-to-input").send_keys("31/12/2020")

#FinishPeriod
driver.find_element(By.ID, "tracking-date-range-picker-confirm-button").click()


#choosing Google Ads platform
driver.find_element(By.CSS_SELECTOR, "img[src='/assets/icons/hide_icon.svg']").click()
driver.find_element(By.XPATH, "(//mat-panel-title)[2]").click()
driver.find_element(By.CSS_SELECTOR, "input[placeholder='Find...']").send_keys("Google Ads")
driver.find_element(By.CSS_SELECTOR, ".mat-tooltip-trigger.name").click()
driver.find_element(By.XPATH, "//button[@class='mat-focus-indicator only-button mat-stroked-button mat-button-base']//span[@class='mat-button-wrapper']").click()


#extracting data from DB
#wait = WebDriverWait(driver, 8)
#wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//tbody/tr[12]/td[3]")))
time.sleep(6)


#monthlyMarketingInvestment to self-check
months_EUR = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
for monthEUR in months_EUR:
    print(monthEUR.text)


#all months of MarketingInvestment
eur_sum = 0
for monthEUR in months_EUR:
    eur_text = monthEUR.text.split()[1]  #Extract EUR value from text
    eur_value = float(eur_text.replace(',', ''))  #Convert to Float
    eur_sum += eur_value


print("Total EUR sum:", eur_sum)
eur_avg = eur_sum / len(months_EUR)
print("Total EUR avg:", eur_avg)


#monthlyMargin Return On Marketing Investment to self-check
eurMROMIs = driver.find_elements(By.XPATH, "//tbody/tr/td[3]")
num_eurMROMIs = []
for eurMROMI in eurMROMIs:
    print(eurMROMI.text)
    numeric_value_eur = float(eurMROMI.text)
    num_eurMROMIs.append(numeric_value_eur)


min_eurMROMIs = min(num_eurMROMIs)
max_eurMROMIs = max(num_eurMROMIs)


#all months of Margin Return On Marketing Investment
sum_eurMROMIs = 0
for eurMROMI in eurMROMIs:
    sum_eurMROMIs += float(eurMROMI.text)


avg_eurMROMIs = sum_eurMROMIs / len(eurMROMIs)

print("Avg EUR MROMIs:", avg_eurMROMIs)
print("Min EUR MROMIs:", min_eurMROMIs)
print("Max EUR MROMIs:", max_eurMROMIs)


#UnderlineResults

#Sum
greatSumTextEUR = driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='sum'] td:nth-child(2)").text
greatSumValueEUR = float(greatSumTextEUR.split()[1].replace(',', ''))
print("UnderlineSum EUR:", greatSumValueEUR)

#Avg
greatAvgTextEUR = driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='avg'] td[class='summary-value']").text
greatAvgValueEUR = float(greatAvgTextEUR.split()[1].replace(',', ''))
print("UnderlineAvg EUR:", greatAvgValueEUR)

#Total of Margin Return On Marketing Investment
greatTotalMarginROIeur = float(driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='total'] td[class='summary-value']").text)
print("Underline Total of Margin Return On Marketing Investment:", greatTotalMarginROIeur)

#Min of Margin Return On Marketing Investment
greatMinMarginROIeur = float(driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='min'] td[class='summary-value']").text)
print("Underline Min of Margin Return On Marketing Investment:", greatMinMarginROIeur)

#Max of Margin Return On Marketing Investment
greatMaxMarginROIeur = float(driver.find_element(By.CSS_SELECTOR, "tr[data-summary-type='max'] td[class='summary-value']").text)
print("Underline Max of Margin Return On Marketing Investment:", greatMaxMarginROIeur)

#rounding
eur_sum = round(eur_sum, 2)
eur_avg = round(eur_avg, 2)
avg_eurMROMIs = round(avg_eurMROMIs, 2)
min_eurMROMIs = round(min_eurMROMIs, 2)
max_eurMROMIs = round(max_eurMROMIs, 2)


#Final EUR Check
def test_equalityTableSumFinalSumMIeur():
    assert eur_sum == greatSumValueEUR, "Equality of MITableSum and MIFinalSum failed in EUR"


def test_equalityTableAvgFinalAvgMIeur():
    assert eur_avg == greatAvgValueEUR, "Equality of MITableAvg and MIFinalAvg failed in EUR"


def test_equalityTableAvgTotalMROMIeur():
    assert avg_eurMROMIs == greatTotalMarginROIeur, "Equality of TableAvgMROMIs and TotalMROMIs failed in EUR"


def test_equalityTableMinFinalMinMROMIeur():
    assert min_eurMROMIs == greatMinMarginROIeur, "Equality of TableMinMROMIs and FinalMinMROMIs failed in EUR"


def test_equalityTableMaxFinalMaxMROMIeur():
    assert max_eurMROMIs == greatMaxMarginROIeur, "Equality of TableMaxMROMIs and FinalMaxMROMIs failed in EUR"


time.sleep(3)


#currency switch -> CZK
driver.find_element(By.ID, "tracking-menu-group-settings").click()
driver.find_element(By.ID, "tracking-menu-item-personalSettings").click()
time.sleep(3)
driver.find_element(By.ID, "tracking-user-settings-currency-selector").click()
driver.find_element(By.XPATH, "(//span[@class='mat-option-text'])[39]").click()   #CZK option
time.sleep(3)
driver.get("https://app.roivenue.com/explore/process/")


driver.close()