import requests
import re

# Populate below list with URLs to be scraped
masterlist = ["https://clutch.co/agencies/new-york","https://clutch.co/uk/agencies/creative"]

headers = {'User-Agent': 'Mozilla\/5.0 \(Macintosh; Intel Mac OS X 10.14; rv:64.0\) Gecko\/20100101 Firefox\/64.0'}

def solver(lst,string):
    strng = ""
    for i in range(len(lst)):
        strng += string.split('#')[lst[i]]
    return strng

for ml in range(len(masterlist)):
    initresponse = requests.get(masterlist[ml],headers=headers)
    maxpages = re.findall(r"<li class=\"pager-current\">1 of (.*)</li>",initresponse.text)
    print(maxpages[0])
    for p in range(0,int(maxpages[0])+1):
        response = requests.get(masterlist[ml]+'?page='+str(p),headers=headers)
        toHit = re.findall(r"<a href=\"(https://clutch.co/profile/[\w\d-]*)\" target=\"_blank\">",response.text)
        for brandUrl in toHit:
            response1 = requests.get(brandUrl,headers=headers)
            mails = re.findall(r"= '(.*[@]{1}.*)';",response1.text)
            names = re.findall(r"(.*) </h1>",response1.text)
            codes = re.findall(r"document.getElementById\(.*'\).innerHTML = (.*)",response1.text)

            if len(mails) != 0:
                for i in range(len(codes)):
                    codes[i] = re.sub("[^0-9]", "", codes[i])
                    codes[i] = [int(i) for i in str(codes[i])]

                for j in range(len(mails)):
                    mails[j] = solver(codes[j],mails[j])

                with open('lst.csv', 'a') as nm:
                    for k in range(len(names)):
                        nm.write(names[k]+","+mails[k])
                        nm.write("\n")

                with open('progress.txt', 'a') as prog:
                    for mal in mails:
                        prog.write(brandUrl+" "+masterlist[ml]+'?page='+str(p))
                        prog.write("\n")

                print(brandUrl+" "+masterlist[ml]+'?page='+str(p))

            else:
                print("No Email Found")