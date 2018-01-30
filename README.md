# SciCrunch python datasets interface

## install
```
pip install git+git://github.com/SciCrunch/python-datasets-interface
```

## usage
```python
    import scicrunch
    interface = scicrunch.datasets.Interface(
        "my secret key",
        "lab name",
        "community name", 
        "scicrunch.org",
        "http_user_name",
        "http_password"
    )

    dataset = interface.getDataset("dataset_name")

    dataset_fields = dataset.get_fields()
    fields = {"field_name" : "value", "field_name2" : "value", "field_name3": "value"}
    # add dataset records and submit dataset using dataset object
    dataset.addDatasetRecord(fields)
    dataset.submitDataset("status")

    data = interface.getdata(dataset)

    # dataset template methods
    template_id = interface.createDatasetTemplate("template_name", "field_name")
    interface.createDatasetField(template_id, "field_name", "ilxid", "if_required", "if_queryable")
    interface.markDatasetField(template_id, "field_name", "subject")
    interface.submitDatasetTemplate(template_id)
    
    dataset2 = interface.addDataset("dataset_name", "long_dataset_name", "description", "publications", template_id)
    
    # add dataset record and submit dataset using interface
    fields = {"field_name" : "value", "field_name2" : "value", "field_name3": "value"}
    interface.addDatasetRecord(dataset.d_id, fields)

    interface.submitDataset(dataset, "status")


```
