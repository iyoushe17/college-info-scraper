from bs4 import BeautifulSoup
import requests
import csv

codes = [
 '163',
 '172',
 '180',
 '164',
 '173',
 '181',
 '165',
 '174',
 '182',
 '166',
 '175',
 '183',
 '167',
 '176',
 '184',
 '168',
 '177',
 '185',
 '169',
 '178',
 '186',
 '170',
 '179',
 '879',
 '187',
 '171']

for district in codes:
    code = district
    url = 'http://www.studyguideindia.com/College-search.asp?college_type=2&State=GJ&Jobfield_id=&District=' + code

    source = requests.get(url).text

    soup = BeautifulSoup(source, 'lxml')

    # finding the link of each college given in the table
    table = soup.find('section', class_="PB15").find('div', class_ = "inner_content").find('table', class_="clg-listing")
    #print(table.prettify()) #table.html

    #store the links in a list
    collegeLinks = []
    for clglink in table.find_all('a'):
        collegeLinks.append(clglink['href'])

    #after storing, we go over each link
    collegeInfoList = []
    wanted = ['College Name', 'Phone', 'E-Mail', 'Website']
    for link in collegeLinks:
        collegeInfo =[]
        collegePage = requests.get(link).text
        soupAgain = BeautifulSoup(collegePage, 'lxml')
        #requests the entire page
        first_college_info = soupAgain.find('div', class_ = "mid_sec-new").find('div', id = "college_details-new")  #clgName.html
        first_college_deets = first_college_info.find('table')
        flag = 0
        key = ''
        df = {}
        for td in first_college_deets.find_all('td'):
            info = td.text.strip()
            if flag:
                df [key] = info
                flag = 0
            else:
                key = info
                flag = 1

        df_wanted = {key: df [key] for key in df.keys() & wanted}
        collegeInfoList.append(df_wanted)

    csv_columns = wanted
    csv_file = "College.csv"
    with open(csv_file, 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
        for data in collegeInfoList:
            writer.writerow(data)