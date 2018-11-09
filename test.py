# -*- coding: utf-8 -*-
import requests
import re
import json

job_website = "https://www.indeed.com/jobs?l=Prescott,+AZ&start="

r = requests.get(job_website, params=None)
text = r.text
#drop html into a file for viewing
with open('jobs.html', mode='wb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as f:
    f.write(r.text.encode('utf-8'))

def parse_jobs(html):
    job_reg = r'jobmap\[\d\]= (.*)'
    jobs_parsed = re.findall(job_reg, text, flags=0)
    jobs = []
    for job in jobs_parsed:
        job = job.replace("'",'"').replace(';', '').replace('{','{"').replace(':','":')
        tmp = ''
        for i in range(len(job)):
            tmp += job[i]
            if job[i] == ',' and ':' in job[i:i+10]:
                tmp += '"'
        job = tmp
        job = f'{job}'
        job_dict = json.loads(job)
        jobs.append(job_dict)
    return jobs

jobs = []
#create a session and choose a user agent to emulate an actual browser
s = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}

for start in range(0,100,10):
    print(f"starting {start}")
    url = f'{job_website}{start}'
    r = s.get(url, headers=headers)
    for job in parse_jobs(r.text):
        jobs.append(job)

#remove duplicates
tmp = jobs
jobs = []
for job in tmp:
    if job not in jobs:
        jobs.append(job)

#spit out job info
for job in jobs:
    info_string = f'''
{job['title']}
    Employer: {job['cmp']}
    Location: {job['city']}, {job['loc']}

    '''
    print(info_string)
print(len(jobs))
