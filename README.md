# Web Automation Framework (Python · Selenium · Pytest-BDD)
A portfolio-style web automation framework demonstrating BDD patterns, Page Object Model architecture, and parallel cross-browser execution against a real public web application.

## Feature Under Test
This suite targets the **Wikipedia** search flow:
* Search for a term → results page loads and is navigable
* Validate search results page elements are displayed correctly
* Cross-browser coverage on Chrome and Firefox via Selenium Grid

## Highlights
* **Page Object Model (POM)** for clean, maintainable test architecture
* **Behaviour-Driven Development (BDD)** using readable, business-oriented Gherkin scenarios
* **Dockerized Selenium Grid** for consistent and reproducible cross-browser execution
* **Parallel execution** via pytest-xdist for faster suite runs
* **CI/CD integration** for automated test execution in pipelines
* **Allure reporting** for rich, visual test reports
* **Structured logging** for traceability and debugging
* **Failure-proofing techniques** to increase test stability and reduce flakiness

## Tech Stack
* Python 3.12
* Selenium 4
* pytest-BDD
* pytest-xdist
* Pipenv
* Docker + Selenium Grid (4.21.0)
* Allure
* webdriver-manager

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
allure generate --clean allure-results
```
Run test via xdist (recommended for first checkup*):
```bash
# 5. Run tests
pipenv run pytest tests/test_fw.py

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

# Optional: run in parallel with a fixed browser mix (recommended once Grid is up)
pipenv run pytest -n 3 --dist=load -k "web" --browsers firefox,chrome

# Optional: run in parallel using the default browser only
pipenv run pytest -n 3 --dist=load -k "web"

# Optional: generate Allure report
allure serve allure-results

# Optional: verify the Grid
http://localhost:4444/grid/console
```

## Project Structure
```text
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

If the `python` command doesn't work or doesn't print the expected version number,
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


### Running Selenium Grid with Docker

This project __does not__ include a Dockerfile or containerised test runner.
Instead, it depends on Selenium Grid containers you run locally.

Start the Selenium Grid using the official images (version 4.21.0)

__Windows/Linux__:
```bash
docker network create grid
docker run -d --net grid --name selenium-hub -p 4444:4444 selenium/hub:4.21.0
docker run -d --net grid --name chrome-node -e SE_EVENT_BUS_HOST=selenium-hub \ selenium/node-chrome:4.21.0
docker run -d --net grid --name firefox-node -e SE_EVENT_BUS_HOST=selenium-hub \ selenium/node-firefox:4.21.0
```

__macOS (Apple Silicon + Intel)__:
```bash
docker network create grid
docker run -d --net grid --platform linux/amd64 \ --name selenium-hub -p 4444:4444 selenium/hub:4.21.0
docker run -d --net grid --platform linux/amd64 \ --name chrome-node -e SE_EVENT_BUS_HOST=selenium-hub selenium/node-chrome:4.21.0
docker run -d --net grid --platform linux/amd64 \ --name firefox-node -e SE_EVENT_BUS_HOST=selenium-hub selenium/node-firefox:4.21.0
```

Once the containers are running, verify the Grid is ready: http://localhost:4444/grid/console
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
docker pull selenium/hub:4.21.0
```
Verify the image:
```bash
docker images
```
<hr>

### Pulling Selenium Browser Nodes
macOS (Apple Silicon + Intel)
```bash
docker pull --platform linux/amd64 selenium/node-chrome:4.21.0
docker pull --platform linux/amd64 selenium/node-firefox:4.21.0
```
Windows/Linux
```bash
docker pull selenium/node-chrome:4.21.0
docker pull selenium/node-firefox:4.21.0
```

By verifying the images again `docker images`, you should see:
```bash
IMAGE                                ID             DISK USAGE   CONTENT SIZE   EXTRA
selenium/hub:4.21.0                  f269ed6bcd3f        966MB          327MB
selenium/node-chrome:4.21.0          239eacca7175       3.02GB          931MB
selenium/node-firefox:4.21.0         549284752c8c       2.93GB          903MB
```
<hr>

### Running the Selenium Grid
Start Selenium Grid using Docker Compose:
```bash
docker-compose up -d
```
Scale browsers if necessary:
```bash
docker-compose up -d --scale chrome=2 --scale firefox=4
```
Notes:
* This project is validated with Selenium images `4.21.0` and `platform: linux/amd64` in `docker-compose.yml`.
* Avoid mixing tags (for example `latest` for nodes and pinned for hub) because it can cause node registration and session timeouts.
* On Apple Silicon, the `linux/amd64` images run under emulation. This is expected for the stable setup below.
<hr>

### Installing Python Packages
Install project dependencies with Pipenv manually, if `pipenv shell` did not activate the environment:
```bash
pipenv install selenium pytest pytest-xdist webdriver-manager pytest-bdd pyyaml allure-pytest
```
Verify the initial test:
```bash
pipenv run pytest tests/test_fw.py
```
<hr>

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


## Troubleshooting
A collection of common issues and quick fixes for running the web-automation project.

### Pipenv Issues
__Pipenv environment not activating__

__Symptom__: `pipenv run pytest` fails or packages aren't found.

__Fix__:
```bash
pipenv --rm
pipenv install
pipenv shell
```

__Conflicts with global Python installations__

__Symptom__: `python --version` prints a different version than expected.

__Fix__: Force Pipenv to use Python 3.12:
```bash
pipenv --python 3.12
```

__`.venv` folder not created inside the project__

__Symptom__: After running `pipenv install`, no `.venv` folder appears in the repository, even though the environment exists.

__Cause__: Pipenv stores virtual environments __outside the project__ by default.

__Fix__ (enable project-local venv):
```bash
export PIPENV_VENV_IN_PROJECT=1
pipenv --rm
pipenv install
```

This recreates the environment inside `./.venv/`.
<hr>

### Python Path Problems
__`ModuleNotFoundError` for project imports__

__Symptom__: Imports like from `pages.home_page import HomePage` fail when running tests.

__Fix__: Add the project root to PYTHONPATH:
```bash
export PYTHONPATH=.
```

macOS/Linux: add to `.zshrc` or `.bashrc`
Windows: add to _Environment Variables_ → _User Variables_ → _PYTHONPATH_
<hr>

### Pytest Problems
__Pytest can't discover tests__

__Fix__:
* Ensure test filenames follow: `test_*.py`
* Ensure the folder contains an `__init__.py` if needed
* Run with explicit path:
```bash
pipenv run pytest tests/
```

__Parallel tests fail (xdist)__ Usually caused by WebDriver sessions overwriting each other.

__Fix__:
* Use isolated sessions per worker
* Or disable parallel for debugging:
```bash
pipenv run pytest -n 1
```
<hr>

### Docker / Selenium Grid Issues
__Recommended, known-good Docker versions (stable baseline)__

If tests are flaky after changing Docker images or tags, return to the known-good versions:
* `selenium/hub:4.21.0`
* `selenium/node-chrome:4.21.0`
* `selenium/node-firefox:4.21.0`

In `docker-compose.yml`, keep `platform: linux/amd64` for all services.
Then restart the Grid:
```bash
docker-compose down
docker-compose up -d --scale chrome=2 --scale firefox=4
```

__Selenium Hub not reachable__

__Symptom__: `selenium.common.exceptions.WebDriverException: hub unreachable`

__Fix__:
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

__Symptom__: `/status` shows only one browser type or zero available slots, and tests fail with `SessionNotCreatedException` or timeouts.

__Cause__: Version mismatch between hub and nodes, or platform mismatch on Apple Silicon.

__Fix__:
* Use the same Selenium version for hub and all nodes (recommended: `4.21.0`).
* Ensure `platform: linux/amd64` is set on all services in `docker-compose.yml` (macOS Apple Silicon).
* Restart the Grid after changes:
```bash
docker-compose down
docker-compose up -d --scale chrome=2 --scale firefox=4
```

Optional: validate the Grid before running tests:
```bash
curl -s http://localhost:4444/status | python3 -m json.tool | grep -E '"browserName"|session'
```

__Browser crashes instantly__

Memory limit too low.

__Fix__ (Linux/macOS):
```bash
sudo sysctl -w kernel.shmmax=268435456
```
<hr>

### Allure Issues
__No results appear in the report__

__Symptom__: Allure opens a report with 0 tests.

__Fix__:
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
<hr>

### WebDriver Issues
__`GeckoDriver not found`__

Install with webdriver-manager (already in project):
```bash
pipenv install webdriver-manager
```

Use `GeckoDriverManager()` instead of local binary.

__Browser cannot start: "DevToolsActivePort file doesn't exist"__

This happens in Docker or CI environments.

__Fix__:
Add proper browser options (already included in most setups):
```bash
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
```
<hr>

### Permissions / OS Issues
__`zsh: permission denied` when running scripts__
```bash
chmod +x <script_name>
```

__Windows: tests hang or fail silently__

Run terminal as Administrator<br>
__OR__<br>
Disable long path restrictions.
