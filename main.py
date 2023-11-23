import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd


def element_and_sibling(formatting):
    return """//td[@class='name' and contains(text(),"{0}")]|//td[@class='name' and contains(text(),"{0}")]/following-sibling::*""".format(
        (formatting))


def company_name():
    return "//div[@class='top-info p-0']//h1"


def get_img_src(browser, reg_code):
    #imgElement = (WebDriverWait(browser, 10).
    #              until(EC.presence_of_element_located((By.XPATH, "//img[@class='marginTop3']"))))
    try:
        imgElement = browser.execute_script("""return document.querySelector("img.marginTop3").attributes""")
        source = imgElement[0]["baseURI"] + "" + imgElement[0]["value"]
    except:
        source = "https://?"
        return "no-exist"


    img_data = requests.get(source).content
    with open('numbers/' + reg_code + ".gif", "wb") as f:
        f.write(img_data)


    return "Will be replaced"


def get_element_and_next_sibling_dom(list_key, browser_object):
    temp_data_set = {};
    # sirket adini ayri cekiyorum

    for temp in list_key:
        if temp == "Company name":
            company_name_object = browser_object.find_element(By.XPATH, "//div[@class='top-info p-0']//h1")
            temp_data_set["Company name"] = company_name_object.text
            continue
        element_n_sibling = element_and_sibling(temp)
        dom = browser_object.find_elements(By.XPATH, element_n_sibling)
        if len(dom) == 0 and temp == "Mobile phone":
            dom = browser_object.find_elements(By.XPATH, element_and_sibling("Phone"))
            temp_data_set["Mobile phone"] = get_img_src(browser, temp_data_set["Registration code"])
            continue
        if len(dom) == 0:
            temp_data_set[temp] = "Not exists"
            continue
        if temp == "Mobile phone":
            temp_data_set[temp] = get_img_src(browser, temp_data_set["Registration code"])
            continue
        temp_data_set[dom[0].text] = dom[1].text
    return temp_data_set


browser = webdriver.Chrome()
yeter = 0
count = 2
main_link = "https://rekvizitai.vz.lt/en/companies/odonthology_services/"
data_set = {}
key_list = ["Company name", "Registration code", "Manager", "Address", "Mobile phone", "Website"];
for count in range(93, 116):
    print("Üzerinde çalışılan sayfa=" + str(count))
    print("Kalan sayfa sayısı=" + str(115 - count))
    if count == 2:
        browser.get(main_link)
    else:
        browser.get(main_link + str(count))

    captcha_needed = browser.find_elements(By.XPATH,
                                           "//input[@id='security_code']")

    if (len(captcha_needed) == 1):
        approve_captcha = input("Captchayı girince entera basın.")
        print("İşleme devam ediliyor.")
    company_list = browser.find_elements(By.XPATH, "//a[contains(@class,'company-title')]");

    company_dic = {}
    for temp in company_list:
        company_dic[temp.text] = temp.get_attribute('href')
    for company in company_dic:
        company_name = company
        company_url = company_dic[company]
        browser.get(company_url)
        result = get_element_and_next_sibling_dom(key_list, browser)
        data_set[company_name] = result

df = pd.DataFrame(data_set)

df = (df.T)


df.to_excel('dict1.xlsx')
print("İşlem tamamlandı")
