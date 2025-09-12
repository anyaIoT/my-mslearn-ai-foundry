#===================================================================================================
#meta 9/11/2025 MSLEARN.  SAMPLE CHATBOT FROM AI FOUNDRY PLAYGROUND
# MSLEARN "Plan and prepare to develop AI solutions on Azure"
# Exercise.  https://ai.azure.com/
# refer to ex0_DevelopGenAI_solutions_in_Azure.pdf
# SAMPLE CODE Variaion 2b) Key authentication with OpenAI SDK (not Azure OpenAI SDK)
# src https://anya-azure-openai.openai.azure.com/openai/deployments/anya-gpt-4o-2/chat sample code


#infra: WLaptop + VSCode
#      env: myGithubExpd\mslearn-ai-foundry .venv
#      confirmed Python 3.10.4
#      $ pip install openai, python-dotenv
#      pip 25.2, openai 1.107.1, python-dotenv 1.1.1
#      maybe? $ pip install azure-identity (installed but not used here)
#      azure-core 1.35.0, azure-identity 1.24.0


# $ pip install openai, python-dotenv

#history
#9/11/2025 - SAMPLE CHATBOT 2b
#      OpenAI SDK, Key authentication
#      Got it working with $myfix0below

#$error, $myfix
#===================================================================================================
import os
from openai import OpenAI
import dotenv

#$error0:  raise OpenAIError(
#openai.OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable
#$myfix0
dotenv.load_dotenv()

endpoint = "https://anya-azure-openai.openai.azure.com/openai/v1/"
#endpoint = "https://anya-azure-openai.openai.azure.com/openai/v1/chat/completions" $note: both endpoints work
deployment_name = os.environ.get("AZURE_OAI_DEPLOYMENT", "anya-gpt-4o-2")
api_key =  os.environ.get("OPENAI_API_KEY")

#initialize
client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

#chat prompt
completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "What is the capital of Ukraine?",
        }
    ],
)

print(completion.choices[0].message)

#===================================================================================================
#output:
# ChatCompletionMessage(content='The capital of Ukraine is **Kyiv** (also spelled as Kiev). It is the largest city in Ukraine and serves as the political, cultural, and economic center of the country.', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None, annotations=[])
#===================================================================================================