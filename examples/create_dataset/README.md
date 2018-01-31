If you have an API Key, Lab and community proceed to the next step.

API Key:
1. Login to Scicrunch or create an account
2. Go to My Account -> API Keys
3. Generate an API Key or get the one under Key

Community:
1. Go to My Account -> Communities
2. Join a community

Lab:
1. Go to My Account -> Labs and datasets
2. Either register a lab or use one of your labs

# Create Dataset
```python
    
    from scicrunch.datasets import *

    interface = datasets.Interface(
        "api_key",
        "lab_name",
        "community_name"
    )
    
    # If dataset template is not created 
    template_id = interface.createDatasetTemplate("Mouse_Example", "Animal_ID")

    fields = {}
    data = []
    with open("mose1.txt") as f:
        line_num = 0
        keys = []
        for line in f:
            if line_num == 0:
                field_info = line.strip.split("|")
                for f in field_info:
                    keys.append(f[0]
                    f = f.split(",")
                    key = f[0]
                    val = f[1]
                    fields[key] = val
            else:
                temp = line.split("|")
                temp_data = {}
                for t in range(len(temp)):
                    temp_data[keys[t]] = temp[t]
                data.append(temp_data)
            line_num += 1
                    

    for field in fields:
        interface.createDatasetField(template_id, field, fields[field], 1, 1)
    interface.markDatasetField(template_id, "field_name", "subject")
    interface.submitDatasetTemplate(template_id)


    # If dataset template is created
    dataset = interface.addDataset("Mouse_Data_Example", "Example of how to create a dataset", "Fake dataset made into a template", "PMID:0000", template_id)
    for d in data:
        interface.addDatasetRecord(dataset.d_id, d)
    interface.submitDataset(dataset, 'approved')  
    

```
