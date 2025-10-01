#$meta 9/30/2024 AzureAI Connect
#using DefaultAzureCredential
#sample for ex2 AgenticAI

import logging
from azure.identity import DefaultAzureCredential

#check if Azure SDK is working
print("Azure SDK is working!")

# logging.basicConfig(level=logging.DEBUG)
cred = DefaultAzureCredential(logging_enable=False)
print(cred.__str__()) #same as cred.__repr__()
print(cred.__dict__.keys())
print(cred.__dict__['credentials'].__class__, len(cred.__dict__['credentials']))
print(cred.__dict__['credentials'][:2]) #list of 2 credentials

#Default scope
print(cred.get_token("https://management.azure.com/.default").__class__)