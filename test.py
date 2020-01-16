'''
Need some help with these 2 issues. For the first, perhaps we can create a “helper”
function that creates a pandas dataframe - the steps to do this are on the readme in the repo.
However, having a convenience function .getDataframe would make this much simpler - similar to
how one can download a CSV from the UI.

For the second, not sure what the issue is - perhaps is trying to access the wrong host?

Also, one additional question - the current implementation uses the dataset name to get the data.
What would it take to be able to access the data via the dataset ID.
'''
from scicrunch import datasets
import pandas as pd

#API interface
interface = datasets.Interface(
        "i9vlVyw2XQPISHpaZ2VWGkwbGUTqme3r",
        "STREET-FAIR sfn2018 fake lab",
        community="odc-sci"
)

#pull data
data = interface.getData(dataset='fake data')
data = interface.getData(dataset_id='144')

#pull info from data
info = interface.getInfo('fake data')

#coerce matrix into pandas dataframe
df = pd.DataFrame(data)

#pull data directly into a pandas DataFrame
df = interface.getDataFrame(dataset='fake data')
df = interface.getDataFrame(dataset_id='144')

## PUSH DATA
df =pd.read_csv("BBB fake data.csv")
fields = df.columns

template_id = interface.createDatasetTemplate("BBB_fake_data")

#generates error
for field in fields:
    interface.createDatasetField(template_id, field, 1, 1)

interface.setAsSubjectField(template_id, "AnimalID")
interface.submitDatasetTemplate(template_id)
