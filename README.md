
**# Web Domain Scanner**

The **Web Domain Scanner** is a comprehensive tool designed to gather detailed information about a given web domain and identify potential security vulnerabilities. It features a user-friendly GUI built with Tkinter, allowing users to perform various scans, including port scanning, CMS detection, and vulnerability checks, all from one interface.

## Features

- **Domain Information Gathering**: Collects IP address, server details, CMS, and protocol information.
- **Sensitive Path Finder**: Identifies sensitive paths and files on the target domain.
- **Vulnerability Scans**:
  - Cross-Origin Resource Sharing (CORS) Misconfigurations
  - SQL Injection
  - Cross-Site Scripting (XSS)
  - Open Redirects
  - Local File Inclusions (LFI)
- **Port Scanning**: Identifies open ports and associated vulnerabilities.
- **JavaScript URL Extraction**: Gathers all JavaScript URLs from the target domain.
- **Public Archives URL Fetching**: Extracts URLs from public archives for further analysis.
- **Directory Brute-Forcing**: Attempts to brute-force directories to find hidden files or folders.
- **Results Logging**: All scan results are saved in a structured directory for easy review.

## Installation

### Prerequisites

- Python 3.8+
- Tkinter (comes pre-installed with Python on most platforms)
- Required Python libraries (install via `requirements.txt`)

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/potatoaimer44/webscanner.git

2. **Libraries**:
    Install required libraries
   
3. **Libraries**:
   ```bash
   python web_scanner.py



Here’s a sample README.md for your web domain scanner project:

markdown
Copy code
# Web Domain Scanner

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-UI-red)

## Overview

The **Web Domain Scanner** is a comprehensive tool designed to gather detailed information about a given web domain and identify potential security vulnerabilities. It features a user-friendly GUI built with Tkinter, allowing users to perform various scans, including port scanning, CMS detection, and vulnerability checks, all from one interface.

## Features

- **Domain Information Gathering**: Collects IP address, server details, CMS, and protocol information.
- **Sensitive Path Finder**: Identifies sensitive paths and files on the target domain.
- **Vulnerability Scans**:
  - Cross-Origin Resource Sharing (CORS) Misconfigurations
  - SQL Injection
  - Cross-Site Scripting (XSS)
  - Open Redirects
  - Local File Inclusions (LFI)
- **Port Scanning**: Identifies open ports and associated vulnerabilities.
- **JavaScript URL Extraction**: Gathers all JavaScript URLs from the target domain.
- **Public Archives URL Fetching**: Extracts URLs from public archives for further analysis.
- **Directory Brute-Forcing**: Attempts to brute-force directories to find hidden files or folders.
- **Results Logging**: All scan results are saved in a structured directory for easy review.

## Installation

### Prerequisites

- Python 3.8+
- Tkinter (comes pre-installed with Python on most platforms)
- Required Python libraries (install via `requirements.txt`)

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/web-domain-scanner.git
   cd web-domain-scanner
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Scanner:

bash
Copy code
python web_scanner.py
Usage
Launch the application:

Run the web_scanner.py file, and the Tkinter GUI will open.
Enter the domain:

Input the domain you wish to scan (e.g., example.com).
Start the scan:

Click the START SCAN button to begin scanning.
View logs and results:

Real-time logs will appear in the GUI, and detailed results will be saved in the /results folder.
Explore available modules:

Click SHOW AVAILABLE SCANNING MODULE to see the list of available scan options.

## File Structure

web-domain-scanner/
│
├── attacks/                 # Modules for specific attacks
│   ├── cors.py
│   ├── xss.py
│   ├── open_redirection.py
│   ├── security_header.py
│   ├── sql.py
│   └── dirbs.py
│
├── libraries/               # General scanning libraries
│   ├── tech.py
│   ├── waf.py
│   ├── sensitive.py
│   ├── info.py
│   ├── javascript.py
│   ├── redirect.py
│   ├── xss.py
│   ├── sqli.py
│   └── lfi.py
│
├── results/                 # Output folder for scan results
│
├── web_scanner.py           # Main application script
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
