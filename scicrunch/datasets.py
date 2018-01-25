import requests, json, string, urllib2

class Interface:
    """
    Interface for connecting to scicrunch server
    Uses api key, lab name, community name

    import datasets.Interface
    interface = datasets.Interface('apikey', 'Lab01', 'Community')
    """
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
        url = url + self.host + '/api/1/'
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
            lab_id = req.json()['data']
            self.__lab_ids = {lab: lab_id}
            return lab_id
               
    # doesnt pass in Dataset object
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

    def getDataset(self, d_name, lab=None):
        """
        Arguments: name of a dataset and lab(optional)
        Returns a Dataset object

        dataset = interface.getDataset('Mouse_dataset')
        """
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
                    labid = __getLabID(self.lab)
        self.__lab_ids[lab] = labid
        url = self.url + 'datasets/id?labid=' + str(labid) + '&datasetname=' + d_name +'&key='+self.key
        print(url)
        try:
            req = requests.get(url,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            d_id = req.json()['data']
            info = self.__getInfo(d_id)
            name = info['name']
            template_id = info['template_id']
            long_name = info['long_name']
            publications = info['publications']
            description = info['description']
            del info['name']
            del info['long_name']   
            del info['publications']
            del info['description']
            del info['d_id']
            fields = info
            dataset = Dataset(d_id, name, long_name, publications, description, template_id, lab, labid, self, fields)
            return dataset

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
            json = req.json()['data']
            d = {}
            d['d_id'] = json['id']
            d['name'] = json['name']
            d['long_name'] = json['long_name']
            d['template_id'] = json['template']['id']
            d['description'] = json['description']
            d['publications'] = json['publications']
            for j in json['template']['fields']:
                d[j['name']] = j['termid']['label']
            return d
    def getInfo(self, dataset, lab=None):
        """
        Argument: dataset name
        Returns a dataset Object with all information

        interface.getInfo('Mouse_1')
        """
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
                    labid = __getLabID(self.lab)
        self.__lab_ids[lab] = labid
        d_id = self.__getDataset(labid, dataset)
        url = self.url + 'datasets/info?datasetid=' + str(d_id) + '&key=' +self.key
        print(url)
        try:
            req = requests.get(url,auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            json = req.json()['data']
            d = {}
            d['d_id'] = json['id']
            d['name'] = json['name']
            d['long_name'] = json['long_name']
            d['template_id'] = json['template']['id']
            d['description'] = json['description']
            d['publications'] = json['publications']
            for j in json['template']['fields']:
                d[j['name']] = j['termid']['label']
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
    
    def getdata(self, dataset, query=None, lab=None):
        """
        Arguments: dataset name, query(optional), lab name(optional)
        Returns list of data
        Query field: Returns only list of data from field indicated 

        data = interface.getdata('Mouse_Dataset', 'AnimalID')
        """
        data_id = self.__getDataset(self.__getLabID(self.lab), dataset)        
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
            if query:
                for r in data:
                    d_set.append(r[query])
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
        """
        Arguments: name of the template, fields requrired for entries
        Returns: new dataset template id

        interface.createDatasetTemplate('template', 'AnimalID')
        """
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
            return d1
  
    #required & queryable can be either '1' or '0'
    def createDatasetField(self, temp_id, name, ilxid, req, query):
        """
        Arguments: template id, name of field to add, ilxid of field to add, req and query are '1' or '0'
        req is whether or not the field is required; query is whether or not the field is queryable

        interface.createDatasetField('1234', 'Study', 'tmp_0138983', '0', '1')
        """
        url = self.url + 'datasets/fields/add'
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
        """
        Arguments: template id, dataset field name, annotation name
        To mark field as subject of template annotation name = 'subject'

        interface.markDatasetField('1234', 'AnimalID', 'subject')
        """
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
        return req.json()
    #/datasets/template/submit?template_id=
    def submitDatasetTemplate(self, temp_id):
        """
        Arguments: template id to submit

        interface.submitDatasetTemplate('1234')
        """
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
        print(req.json())
    #/api/1/datasets/add?name=$long_name=description=publications=metadata=template_id=                
    #return dataset object
    def addDataset(self, name, long_name, desc, pub, template_id):
        """
        Arguments: name, long name, description, publications, and id of template to be used
        Returns a Dataset object containing all information of new dataset

        interface.addDataset('Mouse_Data', 'Data for mice', 'Dataset about VGLUT/CRE expressing mice', 'PMID:12345', '1234' )
        """
        url = self.url + 'datasets/add'
        print(url)
        d ={'name':name,
            'long_name': long_name,
            'description': desc,
            'publications': pub,
            'template_id': template_id,
            'key': self.key}
        headers = {'Content-type': 'application/json'}
        try:
            req = requests.post(url, data=json.dumps(d), headers=headers, auth=(self.user,self.pwrd))
            print(req.status_code)
        except IOError, e:
            if hasattr(e, 'code'):
                print(e.code)
        else:
            #(self, d_id, lab, lab_id, interface, fields):
            
            info = self.__getInfo(dataset.d_id)
            template_id = info['template_id']
            d_id = info['d_id']
            del info['name']
            del info['template_id']
            del info['long_name']   
            del info['publications']
            del info['description']
            del info['d_id']
            fields = info
            dataset = Dataset(d_id, name, long_name, publications, description, template_id, self.lab, self.lab_ids[self.lab], self, fields)
            #add dataset_ID
            print(req.json())
            return dataset
    #/datasets/records/add?datasetid=fields=
    #input fields as dictionary {'field':'value', 'field2': 'value2'}
    def addDatasetRecord(self, d_id, fields):
        """
        Arguments: dataset id, fields of data to add to dataset

        
        interface.addDatasetRecord('12345','{'Gender': 'Female', 'ID': '3', 'Scientist': 'Joe'}' )
        """
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
        print(req.json())
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
        print(req.json())
    def submitDataset(self, dataset, status, lab=None):
        """
        Arguments: dataset name to submit, status of the submit
        Valid status inputs are pending, rejected, approved, approved-internal, not-submitted

        interface.submitDataset('Mouse_Dataset', 'approved')
        """
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
        print(req.json())

class Dataset:
    """
    Dataset class stores information about a specific dataset from scicrunch server
    Uses the dataset id, dataset name, long name, associated publications, description
    template id, lab name, lab d, interface associated with it, and data fields

    dataset = interface.addDataset('Mouse_Data', 'Data for mice', 'Dataset about VGLUT/CRE expressing mice', 'PMID:12345', '1234' )

    or

    dataset = interface.getDataset('Mouse_dataset')
    """

    def __init__(self, d_id, name, long_name, publications, description, template_id, lab, lab_id, interface, fields):
        self.d_id = d_id
        self.name = name
        self.long_name = long_name  
        self.publications = publications
        self.description = description
        self.template_id = template_id
        self.lab = lab
        self.lab_id = lab_id
        self.interface = interface
        self.fields = fields


    def get_fields(self):
        """
        Returns all field types associated with dataset

        dataset.get_fields()
        """
        return self.fields


    def addDatasetRecord(self, fields):
        """
        Adds a record to the dataset from given fields 

        dataset.addDatasetRecord({'Gender': 'Female', 'AnimalID':'4', 'Scientist':'Joe'})
        """
        return self.interface.addDatasetRecord(self.d_id, fields)['success']


    def submitDataset(self, status):
        """
        Submits a dataset to a lab 
        Valid Status input: pending, rejected, approved, approved-internal, not-submitted

        dataset.submitDataset('pending')
        """
        test =  self.interface.submitDataset(self.d_id, status)['success']
        if test:
            self.status = status
        return test
