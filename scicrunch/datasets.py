import requests, json, string, urllib2

"""
Condense methods
if look up lab id store in __lab_ids
before look up check if lab_id in dictionary 
if not specified use default(original) lab
push to git


"""


class Interface:
    #def __init__(self, key=None, host=scicrunch.org, lab, community, user=None, pwrd=None)
    #if lab id !200 raise exception
    def __init__(self, key, lab, community, host = None, user=None, pwrd=None):
        self.key = key
        if host is None:
            self.host = 'scicrunch.org'
        else:
            self.host = host
        self.lab = lab
        self.community = community
        self.user = user
        self.pwrd = pwrd
        url = "https://"
        l = '/'
        url = url + self.host +'.org'+ '/api/1/'
        self.url = url
        url = self.url+ 'lab/id?labname=' + self.lab+'&portalname=' + self.community +'&key='+ self.key
        lab_id = ''
        try:
            req = requests.get(url,auth=(user,pwrd))
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            lab_id = req.json()['data']
        self.__lab_ids = {lab: lab_id}

    #/api/1/lab/id?labname=${name}&portalname=${portalname}
    #get lab id to access lab
    def __getLabID(self, lab):
        url = self.url+ 'lab/id?labname=' + lab+'&portalname=' + self.community +'&key='+ self.key
        print(url)
        try:
            req = requests.get(url,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            return req.json()['data']

   
    def __getDataset(self, labid, dataset):
        url = self.url + 'datasets/id?labid=' + str(labid) + '&datasetname=' + dataset+'&key='+self.key
        print(url)
        try:
            req = requests.get(url,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            return req.json()['data']
    #/api/1/datasets/id?labid=${labid}&datasetname=${datasetname}
    # get dataset id to access data and information
    def getDataset(self, dataset, lab=None):
        if not lab:
            lab = self.lab
            labid = self.__lab_ids[lab]
            if labid == '':
                self.__lab_ids[lab] = self.__getLabID(lab)
        there = False
        for i in self.__lab_ids:
            if i == lab:
                labid = self.__lab_ids[lab]
                there = True
        if not there:
            labid = __getLabID(lab, self.community)
            self.__lab_id[lab] = labid
        url = self.url + 'datasets/id?labid=' + str(labid) + '&datasetname=' + dataset+'&key='+self.key
        print(url)
        try:
            req = requests.get(url,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            return req.json()['data']

    #/api/1/datasets/info?datasetid=${datasetid}
    #if lab id !200 raise exception
    # get metadata for the data set
    def __getInfo(self, data_id):
        url = self.url + 'datasets/info?datasetid=' + str(data_id) + '&key=' +self.key
        print(url)
        try:
            req = requests.get(url,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            d = Dataset()
            json = req.json()
            for j in json['data']['template']['fields']:
                u =d.new_field(j['name'],j['termid']['label'])
            return d

    def getInfo(self, dataset, lab=None):
        data_id = self.getDataset(dataset, lab)
        url = self.url + 'datasets/info?datasetid=' + str(data_id) + '&key=' +self.key
        print(url)
        try:
            req = requests.get(url,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            d = Dataset()
            json = req.json()
            for j in json['data']['template']['fields']:
                u =d.new_field(j['name'],j['termid']['label'])
            return d


    #/api/1/datasets/search?datasetid=${datasetid}
    # get actual data
    def __getdata(self, data_id):
        url = self.url + 'datasets/search?datasetid=' + str(data_id) + '&key=' + self.key
        print(url)
        try:
            req = requests.get(url,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            d = req.json()
            data = d['data']['records']
            d_set = []
            for a in data:
                d_set.append(a)
            return d_set
    
    def getdata(self, dataset, lab=None):
        data_id = self.getDataset(dataset, lab)
        url = self.url + 'datasets/search?datasetid=' + str(data_id) + '&key=' + self.key
        print(url)
        try:
            req = requests.get(url,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            d = req.json()
            data = d['data']['records']
            d_set = []
            for a in data:
                d_set.append(a)
            return d_set
    
    #Create a data template
    # give a name for tem plate and labid to put template in and any required fields name
    #/api/1/datasets/template/add?name=labid=required_fields_name=
    def __createDatasetTemplate(self, name, labid, req_f_name):
        url = self.url + 'datasets/template/add'
        print(url)
        headers = {'Content-type': 'application/json'}
        d = {'name': name, 
             'labid': labid,
             'required_fields_name': req_f_name,
             'key':self.key
             }
        try:
            req = requests.post(url,data = json.dumps(d),headers = headers,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            d1 = req.json()
            data = d1['data']['id']
            return data
    def createDatasetTemplate(self, name, req_f_name, lab=None):
        if not lab:
            lab = self.lab
            labid = self.__lab_ids[lab]
        there = False
        for i in self.__lab_ids:
            if i == lab:
                labid = self.__lab_ids[lab]
                there = True
        if not there:
            labid = __getLabID(lab, self.community)
            self.__lab_id[lab] = labid
        url = self.url + 'datasets/template/add'
        print(url)
        headers = {'Content-type': 'application/json'}
        d = {'name': name, 
             'labid': labid,
             'required_fields_name': req_f_name,
             'key':self.key
             }
        try:
            req = requests.post(url,data = json.dumps(d),headers = headers,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            d1 = req.json()
            data = d1['data']['id']
            return data
  
    #/datasets/field/add?template_id/name=ilxid=required=queryable=
    #required & queryable can be either '1' or '0'
    def createDatasetField(self, temp_id, name, ilxid, req, query):
        url = self.url + ' datasets/fields/add'
        print(url)
        d = {'template_id':temp_id,
            'name': name,
            'ilxid': ilxid,
            'required': req,
            'queryable': query,
            'key': self.key
            }
        headers = {'Content-type': 'application/json'}
        try:
            req = requests.post(url, data=json.dumps(d), headers=headers,auth=(self.user, self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
    #/datasets/field/annotation/add?tamplate_id=name=annotation_name=annotation_value=
    #annotation name = subject to mark field as subject
    def markDatasetField(self, temp_id, name, ann_name):
        url = self.url + 'datasets/field/annotation/add'
        print(url)
        d = {'template_id':temp_id,
            'name': name,
            'annotation_name': ann_name,
            'key': self.key
            }
        headers = {'Content-type': 'application/json'}
        try:
            req = requests.post(url, data=json.dumps(d), headers=headers,auth=(self.user, self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
    #/datasets/template/submit?template_id=
    def submitDatasetTemplate(self, temp_id):
        url = self.url +'datasets/template/submit'
        print(url)
        d = {'template_id':temp_id,
             'key': self.key}
        headers = {'Content-type': 'application/json'}
        try:
            req = requests.post(url, data=json.dumps(d), headers=headers,auth=(self.user, self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
    #/api/1/datasets/add?name=$long_name=description=publications=metadata=template_id=                
    def addDataset(self, name, long_name, desc, pub, temp_id):
        url = self.url + 'datasets/add'
        print(url)
        d ={'name':name,
            'long_name': long_name,
            'description': desc,
            'publications': pub,
            'template_id': temp_id,
            'key': self.key}
        headers = {'Content-type': 'application/json'}
        try:
            req = requests.post(url, data=json.dumps(d), headers=headers, auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
    #/datasets/records/add?datasetid=fields=
    #input fields as dictionary {'field':'value', 'field2': 'value2'}
    def addDatasetRecord(self, d_id, fields):
        url =self.url +'datasets/records/add' 
        print(url)
        headers = {'Content-type': 'application/json'}
        d = {'datasetid': d_id,
            'fields':fields,
            'key':self.key
            }
        try:
            req = requests.post(url, data=json.dumps(d), headers=headers, auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
    #valid status input: pending, rejected, approved, approved-internal, not-submitted
    def __submitDataset(self, d_id, status):
        url = self.url + 'datasets/change-lab-status'
        print(url)
        headers = {'Content-type': 'application/json'}
        d = {'datasetid': d_id,
            'status':status,
            'key':self.key
            }
        try:
            req = requests.post(url, data=json.dumps(d), headers=headers, auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
    def submitDataset(self, dataset, status, lab=None):
        d_id = getDataset(dataset, lab) 
        url = self.url + 'datasets/change-lab-status'
        print(url)
        headers = {'Content-type': 'application/json'}
        d = {'datasetid': d_id,
            'status':status,
            'key':self.key
            }
        try:
            req = requests.post(url, data=json.dumps(d), headers=headers, auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        

class Dataset:
    def __init__(self):
        self.fields = []
        self.data = []
    def new_field(self, m, n ):
        self.fields.append((m,n))
    def add_data(self, a):
        self.data.append(a)
    def get_fields(self):
        return self.fields
    def get_data(self):
        return self.data
