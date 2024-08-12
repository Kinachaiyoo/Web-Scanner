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
   git clone https://github.com/potatoaimer44/webscanner.git
   cd web-domain-scanner

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Run the Scanner**:
   ```bash
   python web_scanner.py

   
## Usage

1. **Launch the Application**:
   - Run the `web_scanner.py` script using Python, and the Tkinter GUI will open.

2. **Enter the Domain**:
   - Input the domain you wish to scan in the provided field (e.g., `example.com`).

3. **Start the Scan**:
   - Click the `START SCAN` button to initiate the scanning process. The scanner will begin gathering information about the domain and checking for vulnerabilities.

4. **Monitor Logs**:
   - Real-time logs will be displayed in the text area within the GUI, detailing the actions taken by the scanner and the results of each scan.

5. **View Results**:
   - After the scan is complete, the results will be saved in a folder named after the target domain. This folder will contain files with detailed information about detected vulnerabilities, open ports, sensitive paths, and more.

6. **Explore Available Modules**:
   - To view the different scanning modules available, click the `SHOW AVAILABLE SCANNING MODULE` button. This will display a list of all the features the scanner can perform.

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



