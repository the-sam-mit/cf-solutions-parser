import os
import sys
import requests
import re
from bs4 import BeautifulSoup
import shutil
import time

username = input('Enter username in CodeForces: ')

submission_list_url = 'https://codeforces.com/submissions/{}/'.format(username)
page = requests.get(submission_list_url, verify = True)

if (page.status_code != 200):
    print("Failed to retrieve the URL: {}".format(contest_url))
    exit(1)

soup = BeautifulSoup(page.text, 'html.parser')
contests = soup.find('div', attrs={"class":"datatable"})
c_table = contests.find('tbody')
lst = contests.findAll('tr')

flag=False

def getExtension(sub_lang):
    ext = ""
    if 'C++' in sub_lang:
        ext = ".cpp"
    elif "C#" in sub_lang:
        ext = ".cs"
    elif 'C' in sub_lang:
        ext = ".c"
    elif 'Py' in sub_lang:
        ext = ".py"
    elif "JavaScript" in sub_lang:
        ext = ".js"
    elif "Java" in sub_lang:
        ext = ".java"
    elif "Kotlin" in sub_lang:
        ext = ".kt"
    elif "PHP" in sub_lang:
        ext = ".php"
    elif "Rub" in sub_lang:
        ext = ".rb"

    
    return ext

def make_dir_os(sub_id, contest_id, sub_status,sub_name,sub_lang, get_soln,folder_name):
    ext = getExtension(sub_lang)

    sub_name = sub_name + ext
    file_name = os.path.join(folder_name,sub_name)
    
    if os.path.isfile(file_name):
    	flag = True
    	print("Already exists !!!")
    	return 

    file1 = open(file_name,'a')
    header = "\n" + contest_id + " " + sub_name + " " + sub_lang + " " + sub_status + "\n"
    file1.write(header + get_soln)
    file1.close()

def createFolder(folder_name):
    if os.path.exists(folder_name) == False:
        os.mkdir(folder_name)
        print("Folder named Submissions created for parsing.")
        return 1
    else:
        print("Folder Submissions already exists!")
        return 0

def get_soln_text(sub_id, contest_id, sub_status,sub_name,sub_lang ,folder_name):
    url_soln = get_soln_url.format(contest_id,sub_id)
    print(url_soln)

    cpp = requests.get(url_soln, verify = True)
    soup_cpp = BeautifulSoup(cpp.text,'html.parser')
    
    get_soln = soup_cpp.findAll('div',attrs={"class" : "roundbox"})[1].find('pre').text
    make_dir_os(sub_id, contest_id, sub_status,sub_name,sub_lang,get_soln,folder_name)


def extract_solution(row_data, c_id, folder_name):
    sub_cell = row_data[-3].find('span')
    sub_id = sub_cell['submissionid']
    sub_status = sub_cell.text
    sub_name = row_data[-5].find('a').text.strip()
    sub_lang =  row_data[-4].text.strip()
    
    #log
    print(sub_id)
    print(sub_status)
    print(sub_name)
    print(sub_lang)
    if sub_status == "Accepted": 
    	get_soln_text(sub_id,c_id,sub_status,sub_name,sub_lang,folder_name)

    print("\n")

t = int(input('Only accepted submissions of all the mentioned submissions will be parsed.\nHow many recent submissions do you want to parse ?\nEnter : ')) + 1
print("Go error-free !! :P\n")
get_soln_url = "http://codeforces.com/contest/{}/submission/{}"

# Main
createFolder("Submissions")

for i in range(t):
	if i==0: continue
	row = lst[i]
	row_data = row.findAll('td')
	link = row_data[3].find('a')['href']
	contest_id = re.findall('[0-9]+',link)[0]
	extract_solution(row_data, contest_id, "Submissions")
	if flag == True: break
# print("Total accepted problems : {} out of {} selected.".format(c, t-1))	

