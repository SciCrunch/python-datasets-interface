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

    def __init__(self,
                 id: int,
                 name: str,
                 long_name: str,
                 publications: str,
                 description: str,
                 template_id: int,
                 lab: str,
                 lab_id: int,
                 interface: object,
                 fields: dict):
        self.id = id
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
        return self.interface.addDatasetRecord(self.id, fields)['success']


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
