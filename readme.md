# MCP Analytics — Employee Data Analysis Using AI

## Overview

MCP Analytics is a Python-based project that uses the **Model Context Protocol (MCP)** to connect an AI assistant with employee data. It enables users to analyze employee information by asking questions in natural language through an MCP-compatible client such as GitHub Copilot in VS Code.

The project uses Pandas to process employee data and FastMCP to expose analytics functions as tools that an AI assistant can call.

## Features

- **Employee Summary:** Retrieve total employees, department count, average salary, and missing-value information.
- **Department Analytics:** Calculate employee counts, average salaries, and total salary expenditure by department.
- **Salary Statistics:** Calculate average, median, minimum, and maximum salaries.
- **Top-Paid Employees:** Retrieve the highest-paid employees.
- **Employee Search:** Search employees by first name, last name, email, or department.
- **Gender Distribution:** Analyze employee counts by gender.

## Technologies Used

- Python
- Model Context Protocol (MCP)
- FastMCP
- Pandas
- GitHub Copilot
- Visual Studio Code
- CSV for data storage

## Project Structure

```text
MCP_analytics/
├── .venv/
├── .vscode/
│   └── mcp.json
├── data/
│   └── employees_100.csv
├── server.py
└── README.md
```

## Dataset

The project uses `employees_100.csv`, containing 100 sample employee records.

The dataset includes these columns:

| Column | Description |
|---|---|
| `id` | Employee identifier |
| `first_name` | Employee first name |
| `last_name` | Employee last name |
| `email` | Employee email address |
| `gender` | Employee gender |
| `department` | Employee department |
| `salary` | Employee salary |

## Installation and Setup

### 1. Prerequisites

Install the following:

- Python 3.10 or later
- Visual Studio Code
- GitHub Copilot with access to Agent mode and MCP server support

### 2. Open the project

Open the project folder in VS Code:

```powershell
cd C:\MCP_analytics
```

### 3. Create and activate a virtual environment

If the `.venv` environment does not already exist:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

Use the MCP SDK v1 API required by the current `server.py` implementation:

```powershell
python -m pip install "mcp[cli]>=1.0.0,<2.0.0" pandas
```

### 5. Configure the MCP server

Create `.vscode/mcp.json` with the following configuration for Windows:

```json
{
  "servers": {
    "employee-analytics": {
      "type": "stdio",
      "command": "${workspaceFolder}/.venv/Scripts/python.exe",
      "args": [
        "${workspaceFolder}/server.py"
      ]
    }
  }
}
```

### 6. Start the MCP server

Open `.vscode/mcp.json` in VS Code and use the available **Start** action for the `employee-analytics` server.

The MCP client launches the server and communicates with it through standard input/output (stdio). Avoid manually running `python server.py` as a way to test client connectivity; the server expects protocol messages from an MCP client.

## How It Works

1. The user asks a question in GitHub Copilot Chat.
2. The AI assistant identifies an appropriate analytics tool.
3. The MCP client sends a tool request to the Python MCP server.
4. The server reads the CSV file using Pandas.
5. Python calculates the requested statistics and returns structured results.
6. The AI assistant presents the results in natural language.

## Example Questions

Try asking GitHub Copilot Chat in Agent mode:

- How many employees are in the dataset?
- Show the number of employees in each department.
- What is the average salary across all departments?
- Find the five highest-paid employees.
- Search for employees in the Engineering department.
- Compare gender distribution across departments.
- Which department has the highest average salary?

## Example Analytics

The dataset has 100 employee records across 8 departments.

Example summary metrics include:

- Total employees: 100
- Male employees: 50
- Female employees: 50
- Overall average salary: $77,720
- Minimum salary: $51,000
- Maximum salary: $108,000

These figures describe the sample dataset supplied for this project. Run the analytics tools against the current CSV to verify results.

## Troubleshooting

### FastMCP import error

If you see an error involving `mcp.server.fastmcp`, check the installed MCP SDK version:

```powershell
python -m pip show mcp
```

The current code uses the MCP SDK v1 API. Install a compatible version:

```powershell
python -m pip install "mcp[cli]>=1.0.0,<2.0.0"
```

### CSV file not found

Confirm that the dataset is located at:

```text
C:\MCP_analytics\data\employees_100.csv
```

### MCP server does not start in VS Code

- Confirm `.vscode/mcp.json` contains valid JSON.
- Confirm the Python executable path exists.
- Ensure the MCP server is started through the VS Code MCP controls.
- Check the MCP server output and logs for errors.

## Future Enhancements

- Interactive salary and department charts.
- SQL database integration.
- Automated data quality checks.
- Salary outlier detection.
- Additional datasets and analytics tools.
- Unit tests and automated validation.
- A web-based analytics dashboard.

## Security and Privacy

The supplied dataset uses example employee records. Do not expose real employee emails, salaries, or other personal information to unauthorized users. Apply appropriate access controls before connecting this project to real company data.

## License

This project is intended for learning, experimentation, and portfolio development. Add a formal license if you plan to distribute or publish the source code.

## Author

Developed as an AI-powered data analytics project using Python and the Model Context Protocol.
