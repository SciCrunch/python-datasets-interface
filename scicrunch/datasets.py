import requests, json, string, urllib2


class Interface:
    #def __init__(self, key=None, host=scicrunch.org, lab, community, user=None, pwrd=None)
    #if lab id !200 raise exception
    def __init__(self, key, host = None, lab, community, user=None, pwrd=None):
        self.key = key
        self.host = scicrunch.org
        self.lab = lab
        self.community = community
        self.user = user
        self.pwrd = pwrd
        #self.key = cfg.interface['key']
        #self.host = cfg.interface['host']
        #self.lab = cfg.interface['lab']
        #self.community = cfg.interface['community']
        #self.user = cfg.interface['user']
        #self.pwrd = cfg.interface['pwrd']
        url = "https://"
        l = '/'
        url = url + self.host +'.org'+ '/api/1/'
        self.url = url

    #/api/1/lab/id?labname=${name}&portalname=${portalname}
    #get lab id to access lab
    def getLabID(self, lab, portal):
        url = self.url+ 'lab/id?labname=' + self.lab+'&portalname=' + self.community +'&key='+self.key
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
    def getDataset(self, labid, dataset):
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
    def getInfo(self, data_id):
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
    def getData(self, data_id, d_set):
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
            for a in data:
                d_set.add_data(a)
            return d_set
    
    #Create a data template
    # give a name for tem plate and labid to put template in and any required fields name
    #/api/1/datasets/template/add?name=labid=required_fields_name=
    def createDatasetTemplate(self, name, labid, req_f_name):
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
    def submitDataset(self, d_id, status):
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
