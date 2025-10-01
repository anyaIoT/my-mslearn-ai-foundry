#===================================================================================================
#meta 9/30/2025 MSLEARN.  Ex2. Develop an AI agent
'''In this exercise, you’ll use Azure AI Agent Service to create a simple agent that analyzes data and creates charts.
The agent can use the built-in Code Interpreter tool to dynamically generate any code required to analyze data.  
Tip. The code used in this exercise is based on the for Azure AI Foundry SDK for Python.

Used the Azure AI Agent Service SDK to create a client application that uses an AI agent. 
Theagent can use the built-in Code Interpreter tool to run dynamic Python code to perform statistical analyses.

Review the code, using the comments to understand how it:
Connects to the AI Foundry project.
Uploads the data file and creates a code interpreter tool that can access it.
Creates a new agent that uses the code interpreter tool and has explicit instructions to use Python asnecessary for statistical analysis.
Runs a thread with a prompt message from the user along with the data to be analyzed.
Checks the status of the run in case there’s a failure
Retrieves the messages from the completed thread and displays the last one sent by the agent.
Displays the conversation history
Deletes the agent and thread when they’re no longer required.
'''
# MSLEARN "Develop an AI agent with Azure AI Foundry Agent Service"
# https://learn.microsoft.com/en-us/training/modules/develop-ai-agent-azure/
# Gitrepo: https://github.com/MicrosoftLearning/mslearn-ai-agents
# Exercise: https://github.com/MicrosoftLearning/mslearn-ai-agents/blob/main/Labfiles/02-build-ai-agent/Python/agent.py 
#           aka https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/02-build-ai-agent.html
# Steps in https://ai.azure.com/ and then agent.py code
# refer to ex2_DevelopAIAgentsInAzure.pdf


#infra: WLaptop + VSCode
#      created .venv: myGithubExpd\mslearn-ai-foundry .venv
#      reqs in file ex2_requirements.txt (python-dotenv 1.1.1, azure-identity 1.25.0, azure-ai-agents 1.1.0)
#      according to ex.pdf, .venv needed: pip install -r ex2_requirements.txt azure-ai-projects
#      confirmed Python 3.10.4
#      refer below for details $ pip list | grep azure


#history
#9/30/2025 - SAMPLE AI AGENT
#      Connect w/ DefaultAzureCredential
#      To figure it out, installed Azure SDK for python (not sure if needed this much Azure stuff))
#      according to ex.pdf, .venv needed: pip install -r ex2_requirements.txt azure-ai-projects


#===================================================================================================

import os
from dotenv import load_dotenv
from typing import Any
from pathlib import Path


# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FilePurpose, CodeInterpreterTool, ListSortOrder, MessageRole

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint= os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # Display the data to be analyzed
    script_dir = Path(__file__).parent  # Get the directory of the script
    file_path = script_dir / 'data.txt'

    with file_path.open('r') as file:
        data = file.read() + "\n"
        print(data)

    # Connect to the Agent client
    agent_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential
            (exclude_environment_credential=True,
            exclude_managed_identity_credential=True)
    )
    with agent_client:


        # Upload the data file and create a CodeInterpreterTool
        file = agent_client.files.upload_and_poll(
            file_path=file_path, purpose=FilePurpose.AGENTS
        )
        print(f"Uploaded {file.filename}")

        code_interpreter = CodeInterpreterTool(file_ids=[file.id])


        # Define an agent that uses the CodeInterpreterTool
        agent = agent_client.create_agent(
            model=model_deployment,
            name="data-agent",
            instructions="You are an AI agent that analyzes the data in the file that has been uploaded. Use Python to calculate statistical metrics as necessary.",
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        print(f"Using agent: {agent.name}")


        # Create a thread for the conversation
        thread = agent_client.threads.create()

    
        # Loop until the user types 'quit'
        while True:
            # Get input text
            user_prompt = input("Enter a prompt (or type 'quit' to exit): ")
            if user_prompt.lower() == "quit":
                break
            if len(user_prompt) == 0:
                print("Please enter a prompt.")
                continue

            # Send a prompt to the agent
            message = agent_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_prompt,
            )

            run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)


            # Check the run status for failures
            if run.status == "failed":
                print(f"Run failed: {run.last_error}")

    
            # Show the latest response from the agent
            last_msg = agent_client.messages.get_last_message_text_by_role(
                thread_id=thread.id,
                role=MessageRole.AGENT,
            )
            if last_msg:
                print(f"Last Message: {last_msg.text.value}")


        # Get the conversation history
        print("\nConversation Log:\n")
        messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        for message in messages:
            if message.text_messages:
                last_msg = message.text_messages[-1]
                print(f"{message.role}: {last_msg.text.value}\n")
    

        # Clean up
        agent_client.delete_agent(agent.id)

    


if __name__ == '__main__': 
    main()


# #Xtra
# #      refer below to $ pip list | grep azure
# azure-ai-agents                        1.1.0
# azure-ai-ml                            1.29.0
# azure-common                           1.1.28
# azure-core                             1.35.1
# azure-core-tracing-opentelemetry       1.0.0b12
# azure-identity                         1.25.0
# azure-mgmt-compute                     37.0.0
# azure-mgmt-core                        1.6.0
# azure-monitor-opentelemetry            1.8.1
# azure-monitor-opentelemetry-exporter   1.0.0b42
# azure-storage-blob                     12.26.0
# azure-storage-file-datalake            12.21.0
# azure-storage-file-share               12.22.0
# opentelemetry-resource-detector-azure  0.1.5
# (.venv) 