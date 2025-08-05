# Email Agent

An intelligent email classification and summarization agent built with LangGraph and LangChain that integrates with Gmail.

## Features

- **Email Classification**: Automatically categorizes emails into categories like PERSONAL, WORK, SCHOOL, PROMOTIONAL, etc.
- **Gmail Integration**: Direct integration with Gmail API for reading and labeling emails
- **Job Application Tracking**: Detects new job application emails and logs them to a Google Sheet
- **LangGraph Workflow**: Uses LangGraph for orchestrated email processing

## Project Structure

```
email-agent/
├── agent/
│   ├── nodes/                 # LangGraph nodes
│   │   ├── classifier.py      # Email classification agent
│   │   ├── summarizer.py      # Email summarization agent
│   │   └── authenticator.py   # Node for loading credentials
│   ├── tools/                 # LangChain tools
│   │   ├── get_emails.py      # Tool to retrieve emails from Gmail
│   │   ├── add_to_label.py    # Tool to add emails to Gmail labels
│   │   ├── add_to_spreadsheet.py # Tool to record job applications in Google Sheets
│   │   └── gmail_authenticate.py # Gmail authentication tool
│   ├── prompts/               # Prompt templates
│   │   ├── classifier_prompt.py
│   │   └── summarizer_prompt.py
│   ├── utils/
│   │   ├── auth.py
│   │   ├── logging.py
│   │   └── print.py
│   ├── graph.py               # Main LangGraph workflow
│   ├── run_graph.py           # CLI entry point
│   └── state.py               # State definition for the graph
├── .github/
│   └── workflows/
│       └── email-agent.yml    # CI/CD workflow
├── requirements.txt       # Python dependencies
└── README.md
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
JOB_SHEET_ID=your_google_sheet_id
JOB_SHEET_NAME=Sheet1  # optional, defaults to Sheet1
```

### 3. Gmail Authentication

To use Gmail features, you need to set up authentication:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials file and save it as `credentials.json` in the project root
6. Generate a token for each Gmail account by running the `quickstart.py` script and save it as `token_<email>.json`

## Usage

Set the `USER_EMAILS` environment variable with a comma‑separated list of email addresses and run the graph:

```bash
export USER_EMAILS="user1@example.com,user2@example.com"
python -m agent.run_graph
```

If `USER_EMAILS` is not set, the default list inside `run_graph.py` is used. The `State` object requires a `user_email` value, and credentials for each user are loaded from `token_<email>.json`.
