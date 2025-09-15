#===================================================================================================
#meta 9/11/2025 MSLEARN.  SAMPLE CHATBOT FROM AI FOUNDRY PLAYGROUND
# MSLEARN "Plan and prepare to develop AI solutions on Azure"
# Exercise.  https://ai.azure.com/
# refer to ex0_DevelopGenAI_solutions_in_Azure.pdf
# SAMPLE CODE Variaion 2a) Key authentication with Azure OpenAI SDK (not Azure OpenAI SDK)
# src https://anya-azure-openai.openai.azure.com/openai/deployments/anya-gpt-4o-2/chat sample code


#infra: WLaptop + VSCode
#      env: myGithubExpd\mslearn-ai-foundry .venv
#      confirmed Python 3.10.4
#      $ pip install openai, python-dotenv
#      pip 25.2, openai 1.107.1, python-dotenv 1.1.1
#      maybe? $ pip install azure-identity (installed but not used here)
#      azure-core 1.35.0, azure-identity 1.24.0


#history
#9/11/2025 - SAMPLE CHATBOT 2a
#      Azure OpenAI SDK, Key authentication
#      Same $myfix as sample_auth_OpenAI.py

#$myfix
#===================================================================================================
import os
import base64
from openai import AzureOpenAI
import dotenv

#$myfix0
dotenv.load_dotenv()

endpoint = os.environ.get("AZURE_OAI_ENDPOINT") #or https://anya-azure-openai.openai.azure.com/openai/deployments/anya-gpt-4o-2/chat/completions?api-version=2025-01-01-preview
deployment = os.environ.get("AZURE_OAI_DEPLOYMENT")
subscription_key = os.environ.get("OPENAI_API_KEY") #"REPLACE_WITH_YOUR_KEY_VALUE_HERE" => my key value)

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

# Prepare the chat prompt
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "why honey is sweet?"
            }
        ]
    }
]

# Include speech result if speech is enabled
messages = chat_prompt

# Generate the completion
completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    max_tokens=6553,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

print(completion.to_json())

#===================================================================================================
#output:
# {
#   "id": "chatcmpl-CF4UVtWHlIgrJA58XGt3xMsjdPJlA",
#   "choices": [
#     {
#       "finish_reason": "stop",
#       "index": 0,
#       "logprobs": null,
#       "message": {
#         "content": "Honey is sweet because it contains natural sugars, primarily **fructose** and **glucose**, which are both simple sugars that taste sweet to the human palate. These sugars are easily digestible and provide a quick source of energy.\n\nHere's a breakdown of why honey is sweet:\n\n1. **High sugar content**: Honey is made up of about 80% sugar and 17-18% water...",
#         "refusal": null,
#         "role": "assistant",
#         "annotations": []
#       },
#       "content_filter_results": {
#         "hate": {
#           "filtered": false,
#           "severity": "safe"
#         },
#         "protected_material_code": {
#           "filtered": false,
#           "detected": false
#         },
#         "protected_material_text": {
#           "filtered": false,
#           "detected": false
#         },
#         "self_harm": {
#           "filtered": false,
#           "severity": "safe"
#         },
#         "sexual": {
#           "filtered": false,
#           "severity": "safe"
#         },
#         "violence": {
#           "filtered": false,
#           "severity": "safe"
#         }
#       }
#     }
#   ],
#   "created": 1757708219,
#   "model": "gpt-4o-2024-11-20",
#   "object": "chat.completion",
#   "system_fingerprint": "fp_ee1d74bde0",
#   "usage": {
#     "completion_tokens": 312,
#     "prompt_tokens": 27,
#     "total_tokens": 339,
#     "completion_tokens_details": {
#       "accepted_prediction_tokens": 0,
#       "audio_tokens": 0,
#       "reasoning_tokens": 0,
#       "rejected_prediction_tokens": 0
#     },
#     "prompt_tokens_details": {
#       "audio_tokens": 0,
#       "cached_tokens": 0
#     }
#   },
#   "prompt_filter_results": [
#     {
#       "prompt_index": 0,
#       "content_filter_results": {
#         "hate": {
#           "filtered": false,
#           "severity": "safe"
#         },
#         "jailbreak": {
#           "filtered": false,
#           "detected": false
#         },
#         "self_harm": {
#           "filtered": false,
#           "severity": "safe"
#         },
#         "sexual": {
#           "filtered": false,
#           "severity": "safe"
#         },
#         "violence": {
#           "filtered": false,
#           "severity": "safe"
#         }
#       }
#     }
#   ]
# }
#===================================================================================================    