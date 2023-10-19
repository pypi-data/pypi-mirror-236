import json
from client import AskSageClient

client = AskSageClient('nicolas@after-mouse.com', '3912492342449027ad4d5d25b705420a8ddba9a5a6ce46452da143d31e0e3f94')
ret = client.query('/superadmin-get-dataset tom.brazil@icsinc.com')

message = ret['message']
if message[0] == '"':
    message = message[1:]
if message[-1] == '"':
    message = message[:-1]

assign_to = 'dany.strakos@icsinc.com'

array_datasets = json.loads(message)
for dataset in array_datasets:
    print('Assigning Dataset: ' + dataset)
    ret = client.query('/superadmin-assign-dataset ' + dataset + ' ' + assign_to)
    print(ret)