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
s = requests.Session()
headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.com'  # This is another valid field
}

for start in range(0,100,10):
    print(f"starting {start}")
    url = f'{job_website}{start}'
    r = s.get(url, headers=headers)
    for job in parse_jobs(r.text):
        jobs.append(job)

tmp = jobs
jobs = []
for job in tmp:
    if job not in jobs:
        jobs.append(job)

for job in jobs:
    info_string = f'''
{job['title']}
    Employer: {job['cmp']}
    Location: {job['city']}, {job['loc']}

    '''
    print(info_string)
print(len(jobs))
