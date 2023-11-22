from selenium import webdriver
from selenium.webdriver.common.by import By
from airium import Airium

browser = webdriver.Chrome()
yeter=0
count = 2
main_link = "https://rekvizitai.vz.lt/en/companies/odonthology_services/"
data_set = {}
for count in range(2,10):
    print("Üzerinde çalışılan sayfa="+str(count))
    print("Kalan sayfa sayısı="+str(115-count))
    if count == 2:
        browser.get(main_link)
    else:
        browser.get(main_link+str(count))

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
        yeter += 1

        company_name = company
        company_url = company_dic[company]
        browser.get(company_url)

        dom = browser.find_elements(By.XPATH,"""//div[@class='details-block__1']//td[@class='name' and contains(text(),"Registration code")] | //div[@class='details-block__1']//td[@class='name' and contains(text(),"Registration code")]/following-sibling::* |
//div[@class='details-block__2']//td[@class='name' and contains(text(),"Manager")] |
//div[@class='details-block__2']//td[@class='name' and contains(text(),"Address")] |
//div[@class='details-block__2']//td[@class='name' and contains(text(),"Mobile phone")] |
//div[@class='details-block__2']//td[@class='name' and contains(text(),"Website")] |
//div[@class='details-block__2']//td[@class='name' and contains(text(),"Website")]/following-sibling::* |
//div[@class='details-block__2']//td[@class='name' and contains(text(),"Manager")]/following-sibling::* |
//div[@class='details-block__2']//td[@class='name' and contains(text(),"Address")]/following-sibling::* |
//div[@class='details-block__2']//td[@class='name' and contains(text(),"Mobile phone")]/following-sibling::*""")

        temp_data_set = {}
        print(len(dom))
        for i in range(1, len(dom), 2):
            if dom[i - 1].text == "Mobile phone":
                imgElement = dom[i - 1].find_element(By.XPATH, "//img[@class='marginTop3']")
                mobile_link = imgElement.get_attribute('src')
                temp_data_set[dom[i - 1].text] = mobile_link
                continue
            if dom[i-1].text == "Email address":
                continue
            temp_data_set[dom[i - 1].text] = dom[i].text;
        data_set[company_name] = temp_data_set
key_list = data_set[list(data_set.keys())[0]].keys();

a = Airium()
with a.table(style='border: 1px solid black; border-collapse:collapse;'):
    with a.thead():
        for key in key_list:
            a.th(style="", _t=key)
    for company in data_set:
        with a.tr():
            for details in data_set[company]:
                print(details+"=details")
                if details=="Mobile phone":
                    with a.td(style='border:1px solid black;',):
                        a.img(src=data_set[company][details],alt="phone-number")
                        continue
                if details=="Website":
                    with a.td(style='border:1px solid black;',):
                        a.a(href=data_set[company][details], _t="Siteye Git",target="_blank")
                a.td(style='border:1px solid black;', _t=data_set[company][details])

                print(details + ":" + data_set[company][details])
    write_it = str(a);

    with open(r'result.html', 'w', encoding='utf8') as f:
        f.write(write_it)

print("İşlem tamamlandı")
