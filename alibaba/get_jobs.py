# -*- coding: utf-8 -*- 
import json
import logging
import requests
import sys
reload(sys)  
sys.setdefaultencoding('utf8')  

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)
JSON_URL = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'

class JOBS(object):
    def __init__(self, json_obj):
        return_value = json_obj['returnValue']

        self.totalPage   = return_value['totalPage']
        self.pageSize    = return_value['pageSize']
        self.startPos    = return_value['startPos']
        self.endPos      = return_value['endPos']
        self.pageIndex   = return_value['pageIndex']
        self.totalRecord = return_value['totalRecord']
        self.datas       = return_value['datas']


# first: 
def get_json(pageIndex, pageSize, first=''):
    values = {'first': first, 'pageIndex': pageIndex, 'pageSize': pageSize}
    rsp = requests.post(JSON_URL, data = values)
    json_str = rsp.text
    json_obj = json.loads(json_str)
    return JOBS(json_obj)

def get_job_list(pageSize):
    jobs = get_json(1, pageSize)
    logger.info('totalRecord: %d| pageSize: %d| totalPage: %d', jobs.totalRecord, jobs.pageSize, jobs.totalPage)    
    jobs_list = []
    for i in range(jobs.totalPage):
        index = i + 1
        logger.info('current index:%d', index)
        jobs = get_json(index, pageSize)
        for data in jobs.datas:
            jobs_list.append(data)

    logger.info('process end')
    return jobs_list


if __name__ == '__main__':
    es_url = 'http://111.231.142.86:9200/jobnest/jobs/'
    header = {}
    header['Content-Type'] = 'application/json'
    pageSize = 50
    job_list = get_job_list(pageSize)
    f = open('job.txt', 'w')
    for job in job_list:
        line = json.dumps(job, ensure_ascii=False)
        line1 = json.dumps(job)
        f.write(line)
        f.write('\n')
        code = job['code']
        url = es_url + code
        print(url)
        res = requests.post(url, data = line1, headers = header)
        print(res.text)
    f.close()
