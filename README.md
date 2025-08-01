# Email Agent

An intelligent email classification and summarization agent built with LangGraph and LangChain that integrates with Gmail.

## Features

- **Email Classification**: Automatically categorizes emails into categories like PERSONAL, WORK, SCHOOL, PROMOTIONAL, etc.
- **Gmail Integration**: Direct integration with Gmail API for reading and labeling emails
- **LangGraph Workflow**: Uses LangGraph for orchestrated email processing

## Project Structure

```
email-agent/
├── nodes/                 # LangGraph nodes
│   ├── classifier.py      # Email classification agent
│   └── summarizer.py      # Email summarization agent
├── tools/                 # LangChain tools
│   ├── get_emails.py      # Tool to retrieve emails from Gmail
│   ├── add_to_label.py    # Tool to add emails to Gmail labels
│   └── gmail_authenticate.py # Gmail authentication tool
├── prompts/               # Prompt templates
│   ├── classifier_prompt.py
│   └── summarizer_prompt.py
├── graph.py               # Main LangGraph workflow
├── state.py               # State definition for the graph
├── requirements.txt       # Python dependencies
└── test_setup.py         # Setup verification script
```

## Setup

### 1. Install Dependencies

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project root with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Gmail Authentication

To use Gmail features, you need to set up authentication:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials file and save it as `credentials.json` in the project root

### 4. Test Setup

Run the test script to verify everything is working:

## Usage

### Basic Usage

```python
from graph import graph
from state import State

# Initialize the graph
app = graph.compile()

# Run the email processing workflow
result = app.invoke({"messages": [{"role": "user", "content": "Process my emails"}]})
```

### Email Categories

The classifier categorizes emails into the following categories:

- **PERSONAL**: Personal emails from friends and family
- **WORK**: Work-related emails
- **SCHOOL**: Educational emails
- **PROMOTIONAL**: Marketing and promotional emails
- **SOCIAL**: Social media notifications
- **JOB_STATUS**: Job application updates
- **OTHER**: Miscellaneous emails
