# 🤖 BioImageIO ChatBot

## Your Personal Assistant in BioImage Analysis

Welcome to the BioImage.IO Chatbot user guide. This guide will help you get the most out of the chatbot, providing detailed information on how to interact with it and retrieve valuable insights related to bioimage analysis.

## Introduction

The BioImage.IO Chatbot is a versatile conversational agent designed to assist users in accessing information related to bioimage analysis. It leverages the power of Large Language Models (LLMs) and integrates user-specific data to provide contextually accurate and personalized responses. Whether you're a researcher, developer, or scientist, the chatbot is here to make your bioimage analysis journey smoother and more informative.

## Chatbot Features

The BioImage.IO Chatbot offers the following features:

* **Contextual Understanding**: The chatbot can understand the context of your questions, ensuring responses are relevant and informative.

* **Personalization**: By incorporating your background information, the chatbot tailors responses to meet your specific requirements.

* **Document Retrieval**: It can search through extensive documentation to provide detailed information on models, applications, datasets, and more. Up to this day, the ChatBot is able to retrieve information from the [bioimage.io](https://bioimage.io), [bio.tools](https://bio.tools), [deepImageJ](https://deepimagej.github.io) and [ImJoy](https://imjoy.io/#/).

* **Query Structured Database by Script Execution**: The chatbot can generate Python scripts for complex queries in structured databases (e.g. csv, json file, SQL databases etc.), helping you perform advanced tasks such as specific questions about the available models at [bioimage.io](https://bioimage.io).

## Using the Chatbot

You can visit the BioImage.IO Chatbot at [https://chat.bioimage.io](https://chat.bioimage.io). Please note that the chatbot is still in beta and is being actively developed. If you encounter any issues, please report them via [Github issues](https://github.com/bioimage-io/bioimageio-chatbot/issues).

## Setup the Chatbot locally

If you want to run the chatbot server locally, you need to have an OpenAI API key. You can get one by signing up at [OpenAI](https://beta.openai.com/). Once you have your API key, you can run the chatbot using the following command:

```bash
pip install bioimageio-chatbot
```

You will also need to set the following environment variables:
```bash
export OPENAI_API_KEY=sk-xxxxxxxx
export BIOIMAGEIO_KNOWLEDGE_BASE_PATH=/path/to/bioimageio-knowledge-base  # default to ./bioimageio-knowledge-base 
```

For more detailed usage, please follow the instructions for the **Command-line Interface**.

### Command-line Interface

BioImage.IO Chatbot comes with a command-line interface to facilitate server management, connection to external servers, and knowledge base creation.

You can access the command-line interface by running `python -m bioimageio_chatbot` or the `bioimageio-chatbot` command.

Below are the available commands and options:

#### Start Server

To start your own server entirely, use the `start-server` command:

```bash
bioimageio-chatbot start-server [--host HOST] [--port PORT]
```

**Options:**

- `--host`: The host address to run the server on (default: `0.0.0.0`)
- `--port`: The port number to run the server on (default: `9000`)

**Example:**

```bash
export OPENAI_API_KEY=sk-xxxxxxxx
export BIOIMAGEIO_KNOWLEDGE_BASE_PATH=./bioimageio-knowledge-base
bioimageio-chatbot start-server --host=0.0.0.0 --port=9000
```

#### Connect to Server

To connect to an external hypha server, use the `connect-server` command:

```bash
bioimageio-chatbot connect-server [--server-url SERVER_URL]
```

**Options:**

- `--server-url`: The URL of the external hypha server to connect to (default: `https://ai.imjoy.io`)

**Example:**

```bash
export OPENAI_API_KEY=sk-xxxxxxxx
export BIOIMAGEIO_KNOWLEDGE_BASE_PATH=./bioimageio-knowledge-base
bioimageio-chatbot connect-server --server-url=https://ai.imjoy.io
```

#### Create Knowledge Base

To create a new knowledge base, use the `create-knowledge-base` command:

```bash
bioimageio-chatbot create-knowledge-base [--output-dir OUTPUT_DIR]
```

**Options:**

- `--output-dir`: The directory where the knowledge base will be created (default: `./bioimageio-knowledge-base`)

**Example:**

```bash
export OPENAI_API_KEY=sk-xxxxxxxx
export BIOIMAGEIO_KNOWLEDGE_BASE_PATH=./bioimageio-knowledge-base
bioimageio-chatbot create-knowledge-base --output-dir=./bioimageio-knowledge-base
```


### Asking Questions

To ask the chatbot a question, simply type your query and send it. The chatbot will analyze your question and provide a relevant response. You can ask questions related to bioimage analysis, software tools, models, and more.

### Personalized Responses

The chatbot uses your user profile information, such as your name, occupation, and background, to personalize its responses. This ensures that the information you receive is tailored to your specific needs.

## Join Us as a Community Partner

The BioImage.IO Chatbot is a community-driven project. We welcome contributions from the community to help improve the chatbot's knowledge base and make it more informative and useful to the community.

For more information, please visit the [contribution guidelines](docs/CONTRIBUTING.md).

If you are a tool developer or maintaining a database related to bioimage analysis, you can join us as a community partner. Please contact us via [Github issues](https://github.com/bioimage-io/bioimageio-chatbot/issues).

## Contact Us

If you have any questions, need assistance, or want to contribute to the chatbot's knowledge base, please don't hesitate to contact us via [Github issues](https://github.com/bioimage-io/bioimageio-chatbot/issues) . Our team is here to help you get started and make valuable contributions.

Thank you for your support and for helping make the BioImage.IO Chatbot more informative and useful to the community.

## Acknowledgements

We thank [AI4Life consortium](https://ai4life.eurobioimaging.eu/) for its crucial support in the development of the BioImage.IO Chatbot.

![AI4Life](https://ai4life.eurobioimaging.eu/wp-content/uploads/2022/09/AI4Life-logo_giraffe-nodes-2048x946.png)

AI4Life has received funding from the European Union’s Horizon Europe research and innovation programme under grant agreement number 101057970. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council Executive Agency. Neither the European Union nor the granting authority can be held responsible for them.
