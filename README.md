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
        "https://scicrunch.org",
        "http_user_name",
        "http_password"
    )

    dataset = interface.getDataset("dataset_name")
```
