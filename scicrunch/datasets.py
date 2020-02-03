import json
import numpy as np
import os
import pandas as pd
import re
from typing import Union, Dict, List
from .dataset import Dataset
from .scicrunch_session import ScicrunchSession
from .tools import Tools


def user_info(key, **kwargs):
    """ For debugging purposes to see what permissions you have with the API key. """
    session = ScicrunchSession(key, **kwargs)
    return session.get('user/info')


# TODO: modify user/info output to no return the fields of datasets... Too much unless asked for by user.
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

    def refresh_user_info(self):
        """ Need to have a global cached permissions & needs to be updated with each addition. """
        self.user_info = self.get('user/info')
        self.accessible_datasets = self.user_info['datasets']

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

    def process_dataset(self, dataset):
        if isinstance(dataset, Dataset):
            return dataset.name, dataset.id
        field = 'id' if self.is_int(dataset) else 'name'
        for dataset_record in self.user_info['datasets']:
            if self.are_equal(dataset, dataset_record[field]):
                return dataset_record['name'], dataset_record['id']
        # For readability
        accessible_datasets = [
            { 'name': d['name'], 'id': d['id'] }
            for d in dl
            for dl in self.get_accessible_datasets().values()
        ]
        raise ValueError(
            f'You do not have access to dataset [{dataset}], ' +
            f'but you do have access to the following datasets:\n' +
            f'{accessible_datasets}'
        )

    # Does this give more information than user_info? I really hope so.
    def get_accessible_datasets(self) -> List[dict]:
        ''' Complete metadata for current lab datasets. '''
        potential_datasets = {}
        for lab in self.accessible_labs:
            try:
                datasets = self.get(f'lab/datasets?labid={lab["id"]}')
                potential_datasets[lab['id']] = datasets
            except:
                pass
        return potential_datasets

    def getRawDataset(self, dataset: Union[str, int]) -> dict:
        """ Returns complete server response of the dataset. """
        dataset_name, dataset_id = self.process_dataset(dataset)
        return self.get(f'datasets/id?labid={self.labid}&datasetname={dataset_name}')

    def getDataset(self, dataset: Union[str, int]) -> object:
        """ Get Dataset meta from Name alone.

        :param str dataset_name: Name of dataset within established lab.
        :returns: Dataset object

        >>> dataset = interface.getDataset('Mouse_dataset')
        """
        # will break & return usable datasets if you don't have permission for the one selected.
        dataset_name, dataset_id = self.process_dataset(dataset)
        info = self.get(f'datasets/id?labid={self.labid}&datasetname={dataset_name}')
        dataset = Dataset(
            info['id'],
            info['name'],
            info['long_name'],
            info['publications'],
            info['description'],
            info['template_id'],
            self.lab_name,
            self.labid,
            self,
            info['template']['fields'])
        return dataset

    def getDataset(self, dataset: Union[str, int]) -> object:
        """ Get Dataset meta from ID alone.

        :param str dataset_name: Name of dataset within established lab.
        :returns: Dataset object

        >>> dataset = interface.getDataset('300')
        """
        # will break & return usable datasets if you don't have permission for the one selected.
        dataset_name, dataset_id = self.process_dataset(dataset)
        info = self.get(f'datasets/info?datasetid={dataset_id})')
        dataset = Dataset(
            info['id'],
            info['name'],
            info['long_name'],
            info['publications'],
            info['description'],
            info['template_id'],
            self.lab_name,
            self.labid,
            self,
            info['template']['fields'])
        return dataset

    def getDataFrame(self, dataset: Union[str, int]) -> pd.DataFrame:
        """
        :param Union[str, int] dataset: Dataset you wish to get the metadata for.

        >>> df = interface.getDataFrame('Mouse_Dataset')
        """
        data = self.getData(dataset=dataset)
        df = pd.DataFrame(data)
        # converts np.Nan types to None
        # saves headache since np.Nan aren't considered null
        df = df.where(pd.notnull(df), None)
        return df

    def getData(self, dataset: Union[int,str], field_name: str = None) -> list:
        """ Returns only list of data from query field indicated or full list by default.

        :param Union[str, int] dataset: Dataset you wish to get the metadata for.
        :param str field_name: Field that you want only.

        >>> data = interface.getData('Mouse_Dataset', 'AnimalID')
        """
        dataset_name, dataset_id = self.process_dataset(dataset)
        records = self.get(f'datasets/search?datasetid={dataset_id}')['records']
        if field_name:
            return [r[field_name] for r in records]
        return records

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
                           ilx_id: int = None) -> dict:
        """ Adds a data field to previously created template

        Should not use ilx_id parameter unless you made a custom entity for your dataset.

        :param int template_id: Lab's template id for dataset.
        :param str field_name: Dataset field name.
        :param bool required: If field is required in dataset.
        :param bool queryable: If field can be queried.
        :param int ilx_id: InterLex ID [default: "Unmapped Data Element"].

        >>> interface.createDatasetField(
                template_id = 1234,
                field_name = 'Study',
                required = False,
                queryable = True
            )
        """
        data = {
            'template_id': template_id,
            'name': field_name,
            'ilxid': ilx_id if ilx_id else self.defaultILX(),
            'required': 1 if required else 0,
            'queryable': 1 if queryable else 0,
        }
        return self.post('datasets/fields/add', data=data)

    def setAsSubjectField(self, template_id: int, field_name: str) -> dict:
        """ Template must have a data field marked subject in order for it to be submitted.

        :param int template_id: Lab's template id for dataset.
        :param str field_name: Dataset field name.

        >>> interface.setAsSubjectField(
                template_id = '1234',
                field_name  = 'AnimalID',
            )
        """
        data = {
            'template_id': template_id,
            'name': field_name,
            'annotation_name': 'subject', # subject to mark field as subject
        }
        return self.post('datasets/field/annotation/add', data=data)

    def submitDatasetTemplate(self, template_id: int) -> dict:
        """ Template must contain a data field marked as subject before being submitted.

        :param int template_id: template id to submit.

        >>> interface.submitDatasetTemplate('1234')
        """
        return self.post('datasets/template/submit', data={'template_id':template_id})

    def addDataset(self,
                   name: str,
                   long_name: str,
                   description: str,
                   publications: Union[list, str],
                   template_id: Union[str, int]) -> dict:
        # TODO: Check how publications are store in DB.
        """ Creates a new dataset within the Lab and the Community associated with it.

        Data must still be added to the dataset after creation.

        :param str name: New shortened dataset name.
        :param str long_name: Complete New dataset name.
        :param str description: Description of dataset intended contents.
        :param str publications: Publications associated with dataset. Comma seperated in DB.
        :param str template_id:
        :returns: a Dataset object containing all information of new dataset

        >>> interface.addDataset(
                name         = 'Mouse_Data',
                long_name    = 'Data for mice',
                description  = 'Dataset about VGLUT/CRE expressing mice',
                publications = 'PMID:12345', 'PMID:56789',
                template_id  = '206',
            )
        """
        # Publications are stored as a single single with delimiter comma.
        publications = ', '.join(publications) if isinstance(publications, list) else publications
        data = {
            'name':name,
            'long_name': long_name,
            'description': description,
            'publications': publications,
            'template_id': template_id,
        }
        info = self.post('datasets/add', data=data)
        self.refresh_user_info()
        dataset = Dataset(
            info['id'],
            info['name'],
            info['long_name'],
            info['publications'],
            info['description'],
            info['template_id'],
            self.lab_name,
            self.labid,
            self,
            info['template']['fields'])
        return dataset

    # TODO: figure out what this post actually returns.
    def addDatasetRecord(self, dataset: int, record: dict) -> dict:
        """ Add row of data to dataset.

        Add data to the previously created dataset.

        :param int dataset: ID of dataset to add row to.
        :param dict fields: Key is the column and the Value is the data added to the column.
        :returns: Dataset dict with meta from row added.

        >>> interface.addDatasetRecord(
                dataset = '12345',
                fields  = {'Gender': 'Female', 'ID': '3', 'Scientist': 'Joe'},
            )
        """
        if not isinstance(record, dict):
            raise ValueError(f'Record should be of type dict, not {type(record)}.')
        dataset_name, dataset_id = self.process_dataset(dataset)
        data = {
            'datasetid': dataset_id,
            'fields': record,
        }
        return self.post('datasets/records/add', data=data)

    def updateDatasetStatus(self, dataset: Union[str, int], status: str = 'pending') -> dict:
        """ Update status of Dataset being worked on.

        :param Union[str, int] dataset: Name or ID of dataset within established lab.
        :param str status: Status of dataset.
            Valid status inputs are pending, rejected, approved-internal, not-submitted

        >>> interface.submitDataset(
                dataset = 'Mouse_Dataset',
                status  = 'approved',
            )
        """
        dd = self.getDataset(dataset)
        data = {
            'datasetid': dd.id,
            'status':status,
        }
        return self.post('datasets/change-lab-status', data=data)
