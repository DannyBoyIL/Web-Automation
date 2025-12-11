# Web Automation Framework (Python · Selenium · Pytest-BDD)
This automation project for web application repository contains example code for the
*Behavior-Driven Python with pytest-bdd &amp; Selenium*.


## Quick Start
For users who want to run the project quickly:
```bash
# 1. Clone repo
git clone <repo-url>
cd web-automation

# 2. Install dependencies
pipenv install

# 3. Activate environment
pipenv shell

# 4. Generate and open an Allure session
allure generate --clean allure-results && allure open
```
Run test via xdist (recommended for first checkup*):
```bash
# 5. Run tests
pipenv run pytest --ignore=tests/step_defs

# Optional: run in parallel
pipenv run pytest -n 4 --ignore=tests/step_defs

# Optional: generate Allure report
allure serve allure-results
```
Run test via BDD (Gherkin):
```bash
# 5. Start Selenium Grid
docker-compose up -d --scale chrome=2 --scale firefox=4

# 6. Run tests 
pipenv run python -m pytest -k "web"

# Optional: generate Allure report
allure serve allure-results
```


## Repository Purpose
This project serves as a comprehensive example of a modern web automation framework built around simple Wikipedia search‑result page capabilities. It demonstrates a full end-to-end implementation of best practices used in professional QA automation, including:

* __Page Object Model (POM)__ for clean, maintainable test architecture.
* __Behaviour-Driven Development (BDD)__ using readable, business-oriented scenarios.
* __CI/CD integration__ for automated test execution in pipelines.
* __Dockerized test environments__ for consistent and reproducible runs.
* __Allure Reporting__ for rich, visual test reports.
* __Extensive logging__ to support debugging and traceability.
* __Failure-proofing techniques__ to increase test stability and reduce flakiness.

The repository provides reference implementations for all these components. Use this project as guidance when building or improving your own automation framework. Instead of copying code directly, explore the structure, patterns, and design decisions to understand how each part contributes to a scalable and robust automation setup.

### Project Structure
```graghql
web-automation/
│
├── features/               # BDD .feature files
├── pages/                  # Page Object Model implementation
├── tests/                  # Test step definitions & glue code
├── utils/                  # Helpers (logging, configs, waiters, etc.)
│
├── docker-compose.yml
├── Dockerfile              * Here will go the Dockerfile for more complex systems
├── Pipfile / Pipfile.lock
├── README.md
└── pytest.ini
```


## Python Setup
Python setup can be complicated.
This section documents how to set up your machine for Python test automation development.
<details> <summary><strong>Read more..</strong></summary>

### Python Installation and Tools

This application requires Python 3.12.
You can download the latest Python version from [Python.org](https://www.python.org/downloads/).
Follow the appropriate installation instructions for your operating system.

You should also have a good Python editor/IDE.
Good choices include [PyCharm](https://www.jetbrains.com/pycharm/)
and [Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

You will also need [Git](https://git-scm.com/) if you want to clone this repository locally.
If you are new to Git, [try learning the basics](https://try.github.io/).

For Web UI tests, install the appropriate browser and WebDriver executable.
These tests use Firefox and [geckodriver](https://github.com/mozilla/geckodriver/releases).

### Python Installation Troubleshooting

Unfortunately, installing Python properly can be complicated,
especially if Python was previously installed on your machine.
To verify your Python installation, enter `python --version` at the command line.
You should see the proper version printed.

If the `python` command doesn't work or doesn’t print the expected version number,
then try using the `python3` command instead.
If that still doesn't work,
then the correct Python installation might not be included in your system path.
Find the directory into which Python was installed,
manually add it to the system path,
relaunch the command line,
and try running Python again.

* [System Path Instructions for Windows](https://geek-university.com/python/add-python-to-the-windows-path/)
* [System Path Instructions for macOS](https://www.educative.io/edpresso/how-to-add-python-to-the-path-variable-in-mac)
* [System Path Instructions for Linux](https://www.computerhope.com/issues/ch001647.htm)

### Python Packages

This application uses third-party packages that are *not* part of the Python Standard Library.
They must be installed separately using `pip`, the standard Python package installer.
You can install them all before you create your test project.

To install each package, enter `pip3 install <package-name>` at the command line.
For example: `pip3 install pytest`.
If you already have a package installed but need to upgrade its version,
run `pip3 install --upgrade <package-name>`.

### Virtual Environments

Running `pipenv install` will install the pytest package locally inside the project ecosystem, while running `pip3 install` will install the pytest package globally for the whole system.
Installing Python packages globally is okay, but it typically isn't a best practice.
Instead, each project should manage its own dependencies locally using a virtual environment.
Virtual environments let projects avoid unnecessary dependencies and version mismatches.
</details>


## Docker Setup
This project uses Docker to ensure consistent and reproducible test environments.
<details> <summary><strong>Read more..</strong></summary>

### Install Docker

Download and install Docker Desktop for your operating system. After installation, verify it works by running:
```bash
docker --version
```
You should see the installed Docker version printed.

### Running Tests in Docker

The repository includes Docker configurations that allow you to run the entire test suite inside a containerised environment. Once Docker is installed, you can build and run the test image:
```bash
docker build -t automation-tests .
docker run automation-tests
```
These commands ensure your tests run in a clean, isolated environment every time.
</details>


## Allure Setup
Allure Reporting provides rich, visual test reports generated from your framework.
<details> <summary><strong>Read more..</strong></summary>

### Install Allure

You must install Allure locally to view reports.

macOS (Homebrew):
```bash
brew install allure
```

Windows: Download the Allure ZIP from the official distribution page, extract it, and add the bin folder to your system path.

Linux:
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

Verify installation:
```bash
allure --version
```

### Viewing Test Reports

After running your tests, an Allure results folder will be created. To generate and view the report:
```bash
allure serve allure-results
```
This command builds the report and opens it in your browser.
</details>


## Running Tests
This project uses Dockerized Selenium Grid and Pipenv-based Python tooling to run the full automation suite.

### Pulling Selenium Hub to Docker Desktop
After Docker Desktop is installed, pull the Selenium Hub image:
```bash
docker pull selenium/hub:latest
```
Verify the image:
```bash
docker images
```

### Pulling Selenium Browser Nodes
macOS (Apple Silicon + Intel)
```bash
docker pull --platform linux/amd64 selenium/node-chrome
docker pull --platform linux/amd64 selenium/node-firefox
docker pull --platform linux/amd64 selenium/node-chrome-debug
docker pull --platform linux/amd64 selenium/node-firefox-debug
```
Windows/Linux
```bash
docker pull selenium/node-chrome
docker pull selenium/node-firefox
docker pull selenium/node-chrome-debug
docker pull selenium/node-firefox-debug
```

By verifying the images again `docker images`, you should see:
```bash
IMAGE                                ID             DISK USAGE   CONTENT SIZE   EXTRA
selenium/hub:latest                  f269ed6bcd3f        966MB          327MB        
selenium/node-chrome-debug:latest    4205fd019f4c       1.63GB          436MB        
selenium/node-chrome:latest          239eacca7175       3.02GB          931MB        
selenium/node-firefox-debug:latest   15f9830958b3       1.46GB          384MB        
selenium/node-firefox:latest         549284752c8c       2.93GB          903MB        
```

### Running the Selenium Grid
Start Selenium Grid using Docker Compose:
```bash
docker-compose up -d
```
Scale browsers if necessary:
```bash
docker-compose up -d --scale chrome=2 --scale firefox=4
```

### Installing Python Packages
Install project dependencies with Pipenv manually, if `pipenv shell` did not activate the environment:
```bash
pipenv install selenium pytest pytest-xdist webdriver-manager pytest-bdd pyyaml allure-pytest
```
Verify the initial test:
```bash
pipenv run pytest
```

### Running the Full Test Suite
After verifying that `test_fw.py` passes:
1. Generate and open an Allure session:
```bash
allure generate --clean allure-results && allure open
```
2. Run Python tests targeting the @web tag:
```bash
pipenv run python -m pytest -k "web"
```
3. View the Allure report:
```bash
allure serve allure-results
```


## 🛠️ Troubleshooting
A collection of common issues and quick fixes for running the web-automation project.

### Pipenv Issues
__Pipenv environment not activating__
Symptom:
`pipenv run pytest` fails or packages aren’t found.

Fix:
```bash
pipenv --rm
pipenv install
pipenv shell
```

__Conflicts with global Python installations__
Symptom:
`python --version` prints a different version than expected.

Fix:
Force Pipenv to use Python 3.12:
```bash
pipenv --python 3.12
```

### Python Path Problems
__`ModuleNotFoundError` for project imports__

Symptom:
Imports like from `pages.home_page import HomePage` fail when running tests.

Fix:
Add the project root to PYTHONPATH:
```bash
export PYTHONPATH=.
```

macOS/Linux: add to `.zshrc` or `.bashrc`
Windows: add to _Environment Variables_ → _User Variables_ → _PYTHONPATH_

### Pytest Problems
__Pytest can't discover tests__
Fix:
* Ensure test filenames follow: `test_*.py`
* Ensure the folder contains an `__init__.py` if needed
* Run with explicit path:
```bash
pipenv run pytest tests/
```

__Parallel tests fail (xdist)__
Usually caused by WebDriver sessions overwriting each other.

Fix:
* Use isolated sessions per worker
* Or disable parallel for debugging:
```bash
pipenv run pytest -n 1
```

### Docker / Selenium Grid Issues
__Selenium Hub not reachable__
Symptom:
`selenium.common.exceptions.WebDriverException: hub unreachable`

Fix:
```bash
docker-compose down
docker-compose up -d
```

Check containers:
```bash
docker ps
```

Hub must be running at:
```bash
http://localhost:4444
```

__Nodes not registering to Hub__
Fix:
Nodes must match Hub’s platform.

Apple Silicon (M1/M2/M3) requires:
```bash
docker pull --platform linux/amd64 selenium/node-chrome
```

Then restart Grid:
```bash
docker-compose down
docker-compose up -d
```

__Browser crashes instantly__
Memory limit too low.

Fix (Linux/macOS):
```bash
sudo sysctl -w kernel.shmmax=268435456
```

### Allure Issues
__No results appear in the report__
Symptom:
Allure opens a report with 0 tests.

Fix:
* Ensure pytest Allure plugin is installed:
```bash
pipenv install allure-pytest
```
* Ensure tests were run before generating:
```bash
pipenv run pytest
```

__`allure: command not found`__

Install Allure:
* macOS:
```bash
brew install allure
```
* Windows: Add `allure\bin` to PATH
* Linux:
```bash
sudo apt-get install allure
```

### WebDriver Issues
__`GeckoDriver not found`__

Install with webdriver-manager (already in project):
```bash
pipenv install webdriver-manager
```

Use `GeckoDriverManager()` instead of local binary.

__Browser cannot start: “DevToolsActivePort file doesn’t exist”__
This happens in Docker or CI environments.

Fix:
Add proper browser options (already included in most setups):
```bash
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
```

### Permissions / OS Issues
__`zsh: permission denied` when running scripts__
```bash
chmod +x <script_name>
```

__Windows: tests hang or fail silently__

Run terminal as Administrator 
OR 
Disable long path restrictions.
