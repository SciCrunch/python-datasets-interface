from scicrunch import datasets

user ='scicrunch'
pwrd = 'perl22(query'
api = 'JpP40SrjfvpZ4JyigzoD6WCnNVHJcWXq'
comm = 'Tester2'
lab = 'tester02'
d_set = 'Test'

#mouse
d_set = 'Mouse 1'
d_set = 'Mouse 2'
d_set = 'Mouse 3'
d_set = 'Mouse 4'
d_set = 'Test'

"""
d = datasets.Interface(api,'test2.scicrunch',lab,comm,user, pwrd)
lab_id = d.getLabID(lab,'portal')
data_id = d.getDataset(lab_id, d_set)
print(data_id)
dset = d.getInfo(data_id)
d.getData(data_id, dset)
#post
#temp_id = d.createDatasetTemp('tester17', lab_id, 'Animal_ID') //works
temp_id = '195'
#d.createDatasetField(temp_id, 'Study', 'tmp_0138983','1','0') //works
#d.markDatasetField(temp_id,'Study', 'subject' )
#d.submitDatasetTemplate(temp_id)
#cant iterate over a nonsequence but metadata for datasetid=25 is []
d.addDataset('TestMice', 'Test for code', 'check if can add', 'PMID:0000','195')
d.addDatasetRecord('20',{'Gender': 'female','ID':'13','Scientist':'J'})
i = d.getDataset(lab_id, 'TestMice')
d.submitDataset(i, 'approved')
"""

#do not need to put the data being passed in into the url can also put the key in the data
#do not need to use annotation value/just set annotation name to subject

#new methods
# all new methods word 1/16

dataset = d_set
d = datasets.Interface(api,lab,comm,'test2.scicrunch',user, pwrd)
c = d.getDataset(dataset)#lab is optional
f = d.getInfo(dataset)#lab is optional
h = d.getdata(dataset)#lab is optional
labid = 9
name = 'try'
req_f_name  = 'Sex'
d.createDatasetTemplate(name, req_f_name)#lab is optional
