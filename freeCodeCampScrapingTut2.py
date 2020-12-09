from bs4 import BeautifulSoup
import requests
import time

def list_diff(list1, list2):
    return (list(list(set(list1)-set(list2)) + list(set(list2)-set(list1))))

print("Type some skills that you do not want a job in or leave blank: \n")
undesired_skills = []
while True:
    und_skill = input('>')
    if und_skill == "":
        break
    undesired_skills.append(und_skill)

# for skills in undesired_skills:
#     print(skills)
# print(undesired_skills[-1])

print(f"Filtering out {undesired_skills}\n")

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')

    jobs= soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_ = 'sim-posted').span.text
        if 'few' in published_date:
            company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ', '')
            skills = job.find('span', class_ = 'srp-skills').text.replace(" ", "" )
            more_info = job.header.h2.a['href']
            flag = any(item in undesired_skills for item in skills)
            if flag is False:
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"Company Name: {company_name} \nRequired Skills: {skills}\n")
                    f.write(f'More Info: {more_info}\n')
                    f.write("*************************")
                print(f'File {index} created ....')

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f"Waiting for {time_wait} minutes ...")
        time.sleep(time_wait * 60)