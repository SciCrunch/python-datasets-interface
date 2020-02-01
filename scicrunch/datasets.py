import json
import numpy as np
import os
import pandas as pd
import re
import requests
from typing import Union, Dict, List
from urllib.parse import urljoin


def user_info(key, **kwargs):
    session = ScicrunchSession(key, **kwargs)
    return session.get('user/info')


class Tools:
    """ Easy Tools """

    def is_int(self, val):
        """ Check if value is a possible integer. """
        try:
            int(val)
            return True
        except:
            return False

    def clean(self, val):
        """ Generic string cleaning. """
        return str(val).strip().lower()

    def are_equal(self, val1, val2):
        """ Check if values are equal. """
        return self.clean(val1) == self.clean(val2)


class ScicrunchSession:
    """ Boiler plate for SciCrunch server responses. """

    def __init__(self,
                 key: str,
                 host: str = 'scicrunch.org',
                 auth: tuple = (None, None)) -> None:
        """ Initialize Session with SciCrunch Server.

        :param str key: API key for SciCrunch [should work for test hosts].
        :param str host: Base url for hosting server [can take localhost:8080].
        :param str user: username for test server.
        :param str password: password for test server.
        """
        self.key = key
        self.host = host

        # https is only for security level environments
        if self.host.startswith('localhost'):
            self.api = "http://" + self.host + '/api/1/'
        else:
            self.api = "https://" + self.host + '/api/1/'

        self.session = requests.Session()
        self.session.auth = auth
        self.session.headers.update({'Content-type': 'application/json'})

    def __session_shortcut(self, endpoint: str, data: dict, session_type: str = 'GET') -> dict:
        """ Short for both GET and POST.

        Will only crash if success is False or if there a 400+ error.
        """
        def _prepare_data(data: dict) -> dict:
            """ Check if request data inputed has key and proper format. """
            if data is None:
                data = {'key': self.key}
            elif isinstance(data, dict):
                data.update({'key': self.key})
            else:
                raise ValueError('request session data must be of type dictionary')
            return json.dumps(data)

        url = urljoin(self.api, endpoint)
        data = _prepare_data(data)
        try:
            # TODO: Could use a Request here to shorten code.
            if session_type == 'GET':
                response = self.session.get(url, data=data)
            else:
                response = self.session.post(url, data=data)
            # crashes if success on the server side is False
            if not response.json()['success']:
                raise ValueError(response.text + f' -> STATUS CODE: {response.status_code}')
            response.raise_for_status()
        # crashes if the server couldn't use it or it never made it.
        except requests.exceptions.HTTPError as error:
            raise error

        # {'data':{}, 'success':bool}
        return response.json()['data']

    def get(self, endpoint: str, data: dict = None) -> dict:
        """ Quick GET for SciCrunch. """
        return self.__session_shortcut(endpoint, data, 'GET')

    def post(self, endpoint: str , data: dict = None) -> dict:
        """ Quick POST for SciCrunch. """
        return self.__session_shortcut(endpoint, data, 'POST')


class Interface(ScicrunchSession, Tools):
    """
    Interface for connecting to scicrunch server
    Uses api key, lab name, community name

    >>> from scicrunch.datasets import Interface
    >>> interface = scicrunch.datasets.Interface('apikey', 'Lab01', 'Community')
    """
    def __init__(self,
                 key: str,
                 lab: Union[str, int] = None,
                 community: Union[str, int] = None,
                 host: str = 'scicrunch.org',
                 auth: tuple = (None, None)):
        """ Interface for one lab at a time.
        :param str key: API key for SciCrunch [should work for test hosts].
        :param Union[str, int] lab: Lab ID or name.
        :param Union[str, int] community: Community ID or name.
        :param str host: Base url for hosting server [can take localhost:8080].
        :param str user: username for test server.
        :param str password: password for test server.
        """
        # api_key for scicrunch (should be same for test environments)
        self.key = key

        ScicrunchSession.__init__(
            self,
            key=self.key,
            host=host,
            auth=auth,
        )

        self.user_info = self.get('user/info')

        self.accessible_communities = self.user_info['communities']
        self.accessible_labs = self.user_info['labs']
        self.accessible_datasets = self.user_info['datasets']

        self.lab_name, self.labid = self.process_lab(lab)
        self.community_name, self.cid = self.process_community(community)

    def process_lab(self, lab):
        field = 'labid' if self.is_int(lab) else 'name'
        for lab_record in self.user_info['labs']:
            if self.are_equal(lab, lab_record[field]):
                return lab_record['name'], lab_record['id']
        raise ValueError(
            f'You do not have access to lab [{lab}], ' +
            f'but you do have access to the following labs:\n' +
            f'{self.user_info["labs"]}'
        )

    def process_community(self, community):
        field = 'cid' if self.is_int(community) else 'portalName'
        for community_record in self.user_info['communities']:
            if self.are_equal(community, community_record[field]):
                return community_record['portalName'], community_record['cid']
        raise ValueError(
            f'You do not have access to community [{community}], ' +
            f'but you do have access to the following communities:\n' +
            f'{self.user_info["communities"]}'
        )

    def get_accessible_datasets(self) -> List[dict]:
        ''' Complete metadata for current lab datasets '''
        potential_datasets = {}
        for lab in self.accessible_labs:
            try:
                datasets = self.get(f'lab/datasets?labid={lab["id"]}')
                potential_datasets[lab['id']] = datasets
            except:
                pass
        return potential_datasets

    # get lab id to access lab
    # basic method to get lab id used only by other methods
    # def __getLabID(self, lab):
    #     url = self.url+ 'lab/id?labname=' + lab + '&portalname=' + self.community + '&key=' + self.key
    #     lab_id = self.get(url).json()['data']
    #     self.__lab_ids = {lab: lab_id}
    #     return lab_id

    # doesnt pass in Dataset object
    # requires lab id unlike public method
    def getRawDataset(self, dataset_name: str) -> dict:
        # TODO:
        # labs must be in it's ID
        # labid = process_lab(labid)
        # datasets need to be in string names
        # datasetname = process_datasetname(datasetname)
        return self.get(
            f'datasets/id?labid={self.labid}&datasetname={dataset_name}')

    # TODO: returns Dataset type instead of object
    def getDataset(self, dataset_name: str) -> object:
        """ Get Dataset meta from Name alone.

        :param str dataset_name: Name of dataset within established lab.
        :returns: Dataset object

        >>> dataset = interface.getDataset('Mouse_dataset')
        """
        try:
            dataset_id = self.get(f'datasets/id?labid={self.labid}&datasetname={dataset_name}')
        except:
            raise ValueError(
                f"You don't have access to \"{dataset_name}\", " +
                f"but have have access to these datasets " +
                f"{[s['name'] for sl in self.get_accessible_datasets().values() for s in sl]}"
            )
        info = self.getInfo(dataset_id)
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
        dataset = Dataset(
            dataset_id,
            name,
            long_name,
            publications,
            description,
            template_id,
            self.lab_name,
            self.labid,
            self,
            fields)
        return dataset

    def getDataFrame(self, dataset=None, dataset_id=None, query=None):
        """
        Arguments: dataset name, query(optional), lab name(optional)
        Returns Pandas DataFrame
        Query field: Returns DataFrame from field indicated

        >>> data = interface.getDataFrame('Mouse_Dataset', 'AnimalID')
        """
        data = self.getData(dataset=dataset, dataset_id=dataset_id, query=query)
        df = pd.DataFrame(data)
        # converts np.Nan types to None
        # saves headache since np.Nan aren't considered null
        df = df.where(pd.notnull(df), None)
        # adds respected header for the column
        if query:
            df.columns = [query]
        return df

    # getDatset will give same information
    def getInfo(self, dataset_id):
        """
        Argument: dataset name
        Returns a dataset Object with all information

        >>> interface.getInfo('Mouse_1')
        """
        json = self.get(f'datasets/info?datasetid={dataset_id})')
        data = {
            'd_id': json['id'],
            'name': json['name'],
            'long_name': json['long_name'],
            'template_id': json['template']['id'],
            'description': json['description'],
            'publications': json['publications'],
            'fields': {},
        }
        for j in json['template']['fields']:
            data['fields'][j['name']] = j['termid']['label']
        return data

    # TODO: endpoint doesn't seem to exist anymore. double check in api-controller.
    # def getData(self, dataset: Union[int,str], field_name: str = None) -> list:
    #     """ Returns only list of data from query field indicated or full list by default.
    #
    #     :param int dataset_id: Dataset ID.
    #     :param str field_name: Field that you want only.
    #
    #     >>> data = interface.getData('Mouse_Dataset', 'AnimalID')
    #     """
    #     if not self.is_int(dataset):
    #         dataset_id = self.getDataset(dataset_name=dataset)
    #     print(dataset_id)
    #     records = self.get(f'datasets/search?datasetid={dataset_id}')['records']
    #     if field_name:
    #         return [r[field_name] for r in records]
    #     return records

    def createDatasetTemplate(self, name):
        """
        Arguments: name of the template
        Returns: new dataset template id

        Only makes a template with a name and id, must still add desired feilds

        >>> interface.createDatasetTemplate('template')
        """
        data = {
            'name': name,
            'labid': self.labid,
            # 'required_fields_name': req_f_name, # what is this for?
        }
        response = self.post('datasets/template/add', data=data)
        return response['id']

    def defaultILX(self):
        """
        Gives default ilxid for fields for current server
        Default ILX is "Unmapped Data Element"
        """
        default_id = '0115028' # "Unmapped Data Element"
        # TODO: elastic for testing no longer has the default unmapped data
        # if re.search('test[0-9].scicrunch.org', self.host):
        #     return 'tmp_' + default_id
        # elif self.host == 'scicrunch.org':
        #     return 'ilx_' + default_id
        # else:
        #     raise ValueError(f'Unsupported host {self.host}')
        return 'ilx_' + default_id

    def createDatasetField(self,
                           template_id: int,
                           field_name: str,
                           required: bool = False,
                           queryable: bool = True,
                           ilxid: int = None) -> dict:
        """ Adds a data field to previously created template

        :param int template_id: Lab's template id for dataset.
        :param str field_name: Dataset field name.
        :param bool required: If field is required in dataset.
        :param bool queryable: If field can be queried.
        :param int ilxid: InterLex ID [default: "Unmapped Data Element"].

        >>> interface.createDatasetField(1234, 'Study', required=False, queryable=True)
        """
        data = {
            'template_id': template_id,
            'name': field_name,
            'ilxid': ilxid if ilxid else self.defaultILX(),
            'required': 1 if required else 0,
            'queryable': 1 if queryable else 0,
        }
        return self.post('datasets/fields/add', data=data)

    #/datasets/field/annotation/add?tamplate_id=name=annotation_name=annotation_value=
    #annotation name = subject to mark field as subject
    def setAsSubjectField(self, template_id: int, field_name: str) -> dict:
        """ Template must have a data field marked subject in order for it to be submitted.

        :param int template_id: Lab's template id for dataset.
        :param str field_name: Dataset field name.

        >>> interface.setAsSubjectField('1234', 'AnimalID')
        """
        data = {
            'template_id': template_id,
            'name': field_name,
            'annotation_name': 'subject',
        }
        return self.post('datasets/field/annotation/add', data=data)

    def submitDatasetTemplate(self, template_id: int) -> dict:
        """ Template must contain a data field marked as subject before being submitted.

        :param int template_id: template id to submit.

        >>> interface.submitDatasetTemplate('1234')
        """
        return self.post('datasets/template/submit', data={'template_id':template_id})

    def addDataset( self,
                    name: str,
                    long_name: str,
                    description: str,
                    publications: str,
                    template_id: int
                  ) -> dict:
        # TODO: Should publications just be publication?
        """
        Arguments: name, long name, description, publications, and id of template to be used
        Returns a Dataset object containing all information of new dataset

        Data must still be added to the dataset after creation

        >>> interface.addDataset('Mouse_Data', 'Data for mice', 'Dataset about VGLUT/CRE expressing mice', 'PMID:12345', '1234' )
        """
        data = {
            'name':name,
            'long_name': long_name,
            'description': description,
            'publications': publications,
            'template_id': template_id,
        }
        info = self.post('datasets/add', data=data)
        template_id = info['template_id']
        d_id = info['id']
        fields = info['template']['fields']
        dataset = Dataset(d_id, name, long_name, publications, description, template_id, self.lab_name, self.labid, self, fields)
        return dataset

    #/datasets/records/add?datasetid=fields=
    #input fields as dictionary {'field':'value', 'field2': 'value2'}
    def addDatasetRecord(self, d_id: int, fields: dict) -> dict:
        """
        Arguments: dataset id, fields of data to add to dataset

        Add data to the previously created dataset
        Can get dataset id from dataset object that was made when addDataset was called

        >>> interface.addDatasetRecord('12345','{'Gender': 'Female', 'ID': '3', 'Scientist': 'Joe'}' )
        """
        data = {
            'datasetid': d_id,
            'fields': fields,
        }
        return self.post('datasets/records/add', data=data)

    def submitDataset(self, dataset, status):
        """
        Arguments: dataset name to submit, status of the submit
        Valid status inputs are pending, rejected, approved, approved-internal, not-submitted

        >>> interface.submitDataset('Mouse_Dataset', 'approved')
        """
        dd = self.getDataset(dataset)
        datasetid = dd.d_id
        data = {
            'datasetid': datasetid,
            'status':status,
        }
        return self.post('datasets/change-lab-status', data=data)

class Dataset:
    """
    Dataset class stores information about a specific dataset from scicrunch server
    Uses the dataset id, dataset name, long name, associated publications, description
    template id, lab name, lab d, interface associated with it, and data fields

    Creates a dataset on the scicrunch server and returns the information

    >>> from scicrunch.datasets import Dataset

    >>> dataset = interface.addDataset('Mouse_Data', 'Data for mice', 'Dataset about VGLUT/CRE expressing mice', 'PMID:12345', '1234' )

    or

    Returns dataset object for a previously created dataset on the scicrunch server

    >>> dataset = interface.getDataset('Mouse_dataset')
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

        >>> dataset.get_fields()
        """
        return self.fields


    def addDatasetRecord(self, fields):
        """
        Adds a record to the dataset from given fields

        >>> dataset.addDatasetRecord({'Gender': 'Female', 'AnimalID':'4', 'Scientist':'Joe'})
        """
        return self.interface.addDatasetRecord(self.d_id, fields)['success']


    def submitDataset(self, status):
        """
        Submits a dataset to a lab
        Valid Status input: pending, rejected, approved, approved-internal, not-submitted

        >>> dataset.submitDataset('pending')
        """
        test =  self.interface.submitDataset(self.name, status)['success']
        if test:
            self.status = status
        return test
