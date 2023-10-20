#!/usr/bin/env python
# coding: utf-8



URL = 'http://manage.jaen.kr'


import requests
import json
import datetime
import os
import pandas as pd
from requests.auth import HTTPBasicAuth
from IPython.display import display

class Dataset:
  
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        # data 폴더 생성
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        try:
            res = requests.get(URL+'/api/project/list_data')
            
        except requests.exceptions.Timeout as errd:
            print("Timeout Error : ", errd)
            
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting : ", errc)
            
        except requests.exceptions.HTTPError as errb:
            print("Http Error : ", errb)

        # Any Error except upper exception
        except requests.exceptions.RequestException as erra:
            print("AnyException : ", erra)

        
        project_data = json.loads(res.text)

        ids = []
        titles = []
        filenames = list(project_data['data_file'].values())
        infos = list(project_data['data_info'].values())
        datas = []
        for e in range(len(list(project_data['data_info'].keys()))):
            id_val = list(project_data['data_info'].keys())[e].split('_')[0]
            ids.append(id_val)
            titles.append((list(project_data['data_info'].keys())[e].split('_')[1]))
            if len(filenames[e])==1:
                datas.append(URL + f'/api/project/dataSingleDownload?pro_id={id_val}&fileName={str(filenames[e])[2:-2]}')
            else:
                temp = []
                for i in range(len(filenames[e])):
                    temp.append(URL + f'/api/project/dataSingleDownload?pro_id={id_val}&fileName={str(filenames[e][i])}')
                datas.append(temp)

        self.dataset = pd.DataFrame({
            'pro_id': ids,
            'name': titles,
            'info': infos,
            'data': datas,
            'filename': filenames,
        })


    def info(self):
        display(self.dataset[['pro_id', 'name', 'info', 'filename']])


    def load(self, dataset_names):
        global datasets
        username = 'mysuni'
        password = 'mysuni1!'

        if type(dataset_names) == str:
            df = self.dataset.loc[self.dataset['name'] == dataset_names]
            if df.shape[0] > 0:
                fileurl = df['data']
                filename = df['filename']
                if type(fileurl.iloc[0]) == str:
                    fileurl.iloc[0] = pd.Series(fileurl.iloc[0])
                for f_name, f_url in zip(filename.iloc[0], fileurl.iloc[0]):
                    r = requests.get(f_url, auth=HTTPBasicAuth(username, password))
                    filepath = os.path.join(self.data_dir, f_name)
                    open(filepath, 'wb').write(r.content)
                    print(f'파일 다운로드 완료\n====================\n\n데이터셋: {dataset_names}\n파일경로: {filepath}\n\n====================')
                return
            else:
                raise Exception('데이터셋 정보가 없습니다.')

        elif type(dataset_names) == list or type(dataset_names) == tuple:
            for dataset_name in dataset_names:
                df = self.dataset.loc[self.dataset['name'] == dataset_name]
                if df.shape[0] > 0:
                    fileurls = df['data'].iloc[0]
                    filenames = df['filename'].iloc[0]
                    if type(fileurls) == str:
                        fileurls = pd.Series(fileurls)
                    for fileurl, filename in zip(fileurls, filenames):
                        r = requests.get(fileurl, auth=HTTPBasicAuth(username, password))
                        filepath = os.path.join(self.data_dir, filename)
                        open(filepath, 'wb').write(r.content)
                        print(f'파일 다운로드 완료\n====================\n\n데이터셋: {dataset_name}\n파일경로: {filepath}\n\n====================')
                else:
                    raise Exception('데이터셋 정보가 없습니다.')
            return
        else:
            raise Exception('잘못된 정보입니다.')
            

dataset = Dataset()


def list_data():
    global dataset
    dataset.info()


def download_data(dataset_name):
    global dataset
    return dataset.load(dataset_name)





class Project:
    def __init__(self, project_name, class_info, email, server='manage'):
        self.project_name = project_name
        self.edu_name = class_info['edu_name']
        self.edu_rnd = class_info['edu_rnd']
        self.edu_class = class_info['edu_class']
        self.email = email
        self.server = server

    def __make_submission(self, submission):
        timestring = datetime.datetime.now().strftime('%H-%M-%S')
        filename = 'submission-{}.csv'.format(timestring)
        submission.to_csv(filename, index=False)
        print('파일을 저장하였습니다. 파일명: {}'.format(filename))
        return filename

    def __project_submission(self, file_name):
        file_path = './'
        url = URL + f'/api/studentProject/apiScoring?edu_name={self.edu_name}&edu_rnd={self.edu_rnd}&edu_class={self.edu_class}&mail={self.email}&project_name={self.project_name}&file_name={file_name}'
        files = {'file': (file_name, open(file_path + file_name, 'rb'), 'text/csv')}
        r = requests.post(url, files=files)
        r.encoding = 'utf-8'
        message = ''
        try:
            data = json.loads(r.text) # json 변환 실패시 원본 메세지 사용
            if 'trial' in data.keys():
                message = '제출 여부 :{}\n오늘 제출 횟수 : {}\n제출 결과:{}'.format(data['msg'], data['trial'], data['score'])
            else:
                message = '제출 실패 : {}'.format(data['msg'])
        except:
            message = '변환 에러 발생 : {}'.format(r.text)
        return message

    def submit_ipynb(self, ipynb_file_path=None):
        if ipynb_file_path is None:
            raise Exception('노트북(ipynb) 파일의 경로를 입력해 주세요.') 
        url = URL + '/api/studentProject/ipynbUploadFromMod'
        upload = {'upload_file': open(ipynb_file_path, 'rb')}
        upload['filename'] = upload['upload_file'].name[2:]
        res = requests.post(url, data = upload, params = self.info(), verify = False)
        print(res.text)

    def submit(self, submission):
        filename = self.__make_submission(submission)
        print(self.__project_submission(filename))
    
    def info(self):
        return {'edu_name': self.edu_name, 
                'edu_rnd': self.edu_rnd,
                'edu_class': self.edu_class, 
                'email': self.email, 
                'project_name': self.project_name}

def submit(submission_file):
    global project
    project.submit(submission_file)

def submit_ipynb(ipynb_file_path):
    global project
    project.submit_ipynb(ipynb_file_path)


def update_project(project_name=None, class_info=None, email=None):
    global project
    if project_name:
        project.project_name = project_name
    if project.class_info:
        project.class_info = class_info
    if project.email:
        project.email = email
    print('정보 업데이트 완료')

