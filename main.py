from selenium import webdriver
from selenium.webdriver.common.by import By
from airium import Airium


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def element_and_sibling(formatting):
    return """//td[@class='name' and contains(text(),"{0}")]|//td[@class='name' and contains(text(),"{0}")]/following-sibling::*""".format((formatting))
def company_name():
    return "//div[@class='top-info p-0']//h1"
def get_img_src(browser):
    try:

        imgElement = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "//img[@class='marginTop3']")))
        source = imgElement.get_attribute('src')

    except:
        source = "not exists"

    return source
def get_element_and_next_sibling_dom(list_key,browser_object):
    temp_data_set = {};
    #sirket adini ayri cekiyorum



    for temp in list_key:
        if temp == "Company name":
            company_name_object = browser_object.find_element(By.XPATH,"//div[@class='top-info p-0']//h1")
            temp_data_set["Company name"] = company_name_object.text
            continue
        element_n_sibling = element_and_sibling(temp)
        dom = browser_object.find_elements(By.XPATH,element_n_sibling)
        if len(dom) == 0 and temp =="Mobile phone":
            print(temp+"=Bu değişik mobile phone yok")
            dom = browser_object.find_elements(By.XPATH, element_and_sibling("Phone"))
            temp_data_set["Mobile phone"] = get_img_src(browser)
            continue
        if len(dom) == 0:
            print(temp+"=Bunda tek data dönüyo")
            temp_data_set[temp] = "Not exists"
            continue
        if temp =="Mobile phone":

            temp_data_set[temp] = get_img_src(browser)
            continue
        temp_data_set[dom[0].text] = dom[1].text
    return temp_data_set

browser = webdriver.Chrome()
yeter = 0
count = 2
main_link = "https://rekvizitai.vz.lt/en/companies/odonthology_services/"
data_set = {}
key_list = ["Company name","Registration code", "Manager", "Address", "Mobile phone", "Website"];
for count in range(2, 116):
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
        result = get_element_and_next_sibling_dom(key_list,browser)
        data_set[company_name] = result

a = Airium()
with a.table(style='border: 1px solid black; border-collapse:collapse;'):
    with a.thead():
        for key in key_list:
            a.th(style="", _t=key)
    for company in data_set:
        with a.tr():
            for details in data_set[company]:
                if details == "Mobile phone":
                    with a.td(style='border:1px solid black;', ):
                        a.img(src=data_set[company][details], alt="phone-number")
                        continue
                if details == "Website":
                    with a.td(style='border:1px solid black;', ):
                        a.a(href=data_set[company][details], _t="Siteye Git", target="_blank")
                a.td(style='border:1px solid black;', _t=data_set[company][details])

    write_it = str(a);

    with open(r'result.html', 'w', encoding='utf8') as f:
        f.write(write_it)

print("İşlem tamamlandı")
