# SciCrunch python datasets interface
## Currently this library works with Python 3

[Example of how to create a dataset](https://github.com/SciCrunch/python-datasets-interface/tree/master/examples/create_dataset)

[Example of how to get data from an existing dataset](https://github.com/SciCrunch/python-datasets-interface/tree/master/examples/get_data)
## install
```
pip install git+git://github.com/SciCrunch/python-datasets-interface
```

## usage
```python
    from scicrunch import Interface
    interface = Interface(
        "my secret key",
        "lab name",
        community="community name"
    )

    dataset = interface.getDataset("dataset_name")

    dataset_fields = dataset.get_fields()
    record = {"field_name" : "value", "field_name2" : "value", "field_name3": "value"}
    # add dataset records and submit dataset using dataset object
    dataset.addDatasetRecord(record)
    dataset.submitDataset("status")

    data = interface.getData(dataset)

    # dataset template methods
    template_id = interface.createDatasetTemplate("template_name")
    interface.createDatasetField(template_id, "field_name", "if_required", "if_queryable")
    interface.setAsSubjectField(template_id, "field_name", "subject")
    interface.submitDatasetTemplate(template_id)

    dataset2 = interface.addDataset("dataset_name", "long_dataset_name", "description", "publications", template_id)

    # add dataset record and submit dataset using interface
    record = {"field_name" : "value", "field_name2" : "value", "field_name3": "value"}
    interface.addDatasetRecord(dataset.id, record=record)

    interface.submitDataset(dataset, "status change if you have permissions")


```
