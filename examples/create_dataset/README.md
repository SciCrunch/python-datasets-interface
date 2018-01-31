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

# Import module and get data from example dataset 'mouse1.txt'
```python
    
    from scicrunch.datasets import *

    # For reading in the example dataset file 'mouse1.txt'
    fields = []
    data = []
    with open("mouse1.txt") as f:
        line_num = 0
        keys = []
        for line in f:
            if line_num == 0:
                field_info = line.strip.split(",")
                for f in field_info:
                    keys.append(f)
            else:
                temp = line.split(",")
                temp_data = {}
                for t in range(len(temp)):
                    temp_data[keys[t]] = temp[t]
                data.append(temp_data)
            line_num += 1
```                    
# Make an Interface object to connect with the scicrunch server
Include your api key, the lab name and the community name
```
    interface = datasets.Interface(
        "api_key",
        "lab_name",
        "community_name"
    )
```  
# Create a dataset template and get its ID 
The only argument is the name of the dataset template.
Then add the dataset fields to the template. Specify the template ID gotten when the template was created, and the fields specified in the mouse1.txt file.
Set a field as the subject
After a field has been set as a subject the template can be submitted
```
    template_id = interface.createDatasetTemplate("Mouse_Example")
    
    for field in fields:
        interface.createDatasetField(template_id, field, 1, 1)
    interface.setAsSubjectField(template_id, "field_name", "subject")
    interface.submitDatasetTemplate(template_id)
```
# Create a dataset
Make the dataset with its name, long name, a description, publications and the ID of the template you would like to use
Then add data to the dataset using the example data from the file 'mouse1.txt'.
After the data has been added submit the dataset
```
    dataset = interface.addDataset("Mouse_Data_Example", "Example of how to create a dataset", "Fake dataset made into a template", "PMID:0000", template_id)
    for d in data:
        interface.addDatasetRecord(dataset.d_id, d)
    interface.submitDataset(dataset, 'approved')  
    

```
