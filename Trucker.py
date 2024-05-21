from bs4 import BeautifulSoup
import requests
import datetime
import re

def dateLogic(date, dot):
    currentYear = datetime.datetime.now().year
    currentMonth = datetime.datetime.now().month
    monthEXP = dot % 10
    if monthEXP == 0:
        monthEXP = 10
    dot = dot // 10 
    if dot % 2 == 0:
        even = True
    else:
        even = False

    if even: 
        if currentYear % 2 == 0:
            yearEXP = currentYear - 2
        else:
            yearEXP = currentYear - 1
    else:
        if currentYear % 2 == 0:
            yearEXP = currentYear - 1
        else:
            yearEXP = currentYear - 2
    formYear = date[6:]
    if int(formYear) < yearEXP:
       return "EXPIRED"
    elif int(formYear) == yearEXP:
        formMonth = date[:2]
        if int(formMonth) < currentMonth:
            return "EXPIRED"
        else:
            return "UP TO DATE"
    else:
        return "UP TO DATE"
    
def InterstateLogic(dot, name, current):
    # url = "https://www.ucr.gov/registration-history/" + str(dot)
    # headers = {
    #    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"
    # }
    # response = requests.get(url, headers=headers)
    # if response.status_code == 200:
    #     soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    #     print (soup)
    # else: 
    #     print (f"Failed to retrieve the webpage for DOT " + str(dot) + ". Status code: {response.status_code}")

    print(str(dot) + " - " + name + " - " + current + " - " + "INTERSTATE" )

def getDotNums():
    dot_nums = []
    with open("Numbers.txt", "r") as file:
        for line in file:
            match = re.match(r'^\d+', line)
            if match:
                dot_nums.append(int(match.group()))
    
    return dot_nums


def main():
    #dot_nums = [1423178, 3434322, 1235567, 3176322, 1009025, 2442555, 6930632]
    dot_nums = getDotNums()
    for dot in dot_nums:
        print()
        url = "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=" + str(dot)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            td_tags = soup.find_all("td", class_="queryfield", valign="top")
            if len(td_tags) <=0: # if not fields are found, company is likelly inactive
                print(str(dot) + " - LIKELY INACTIVE")
                continue
            if  td_tags[6]: # number 6 should hold the name of the company
                name = td_tags[6].get_text(strip=True)
                if  td_tags[4]: # number 4 should hold the date the company was last updated
                    date = td_tags[4].get_text(strip=True)
                    current = dateLogic(date, dot)
                else:
                    print(str(dot) + " - NO DATE FOUND")
                    continue
            else:
                print(str(dot) + " - NO NAME FOUND") 
                continue
        
            td_xTags = soup.find_all("td", width="5%", class_="queryfield")
            interstate = td_xTags[3].get_text(strip=True)  # location of the interstate x field
            if interstate == 'X':
                InterstateLogic(dot, name, current)
            else:
                print(str(dot) + " - " + name + " - " + current + " - " + "NOT INTERSTATE")



        else:
            print(f"Failed to retrieve the webpage for DOT " + str(dot) + ". Status code: {response.status_code}")

        

if __name__ == "__main__":
    main()