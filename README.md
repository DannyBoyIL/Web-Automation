# Web-Automation
This automation project for web application repository contains example code for the
*Behavior-Driven Python with pytest-bdd &amp; Selenium*.
The stack includes the implementation of the following: POM | BDD | CI/CD | Docker | Allure Reporting | Logging | Failue Proofing


## Repository Purpose
This project serves as a comprehensive example of a modern web automation framework built around simple Wikipedia search‑result page capabilities. It demonstrates a full end-to-end implementation of best practices used in professional QA automation, including:

* Page Object Model (POM) for clean, maintainable test architecture.
* Behaviour-Driven Development (BDD) using readable, business-oriented scenarios.
* CI/CD integration for automated test execution in pipelines.
* Dockerized test environments for consistent and reproducible runs.
* Allure Reporting for rich, visual test reports.
* Extensive logging to support debugging and traceability.
* Failure-proofing techniques to increase test stability and reduce flakiness.

The repository provides reference implementations for all these components. Use this project as guidance when building or improving your own automation framework. Instead of copying code directly, explore the structure, patterns, and design decisions to understand how each part contributes to a scalable and robust automation setup.

## Python Setup

Python setup can be complicated.
This section documents how to set up your machine for Python test automation development.

### Python Installation and Tools

You can complete this course using any OS: Windows, macOS, Linux, etc.

This course requires Python 3.
You can download the latest Python version from [Python.org](https://www.python.org/downloads/).
Follow the appropriate installation instructions for your operating system.

You should have basic Python programming skills before attempting this course.
Learning the language is always a prerequisite for learning automation.
If you need help learning Python, check out this article:
[How Do I Start Learning Python?](https://automationpanda.com/2020/02/18/how-do-i-start-learning-python/)

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

This course will use a handful of third-party packages that are *not* part of the Python Standard Library.
They must be installed separately using `pip`, the standard Python package installer.
You can install them all before you create your test project,
or you can install them as you complete each chapter in the course.

To install each package, enter `pip install <package-name>` at the command line.
For example: `pip install pytest`.
If you already have a package installed but need to upgrade its version,
run `pip install --upgrade <package-name>`.

Please note that if you need to use the `python3` command to run Python,
then you might also need to use the `pip3` command in lieu of `pip`.

### Virtual Environments

Running `pip install` will install the pytest package globally for the whole system.
Installing Python packages globally is okay for this course,
but it typically isn't a best practice in the "read world."
Instead, each project should manage its own dependencies locally using a virtual environment.
Virtual environments let projects avoid unnecessary dependencies and version mismatches.

For simplicity, this course will not use or teach virtual environments.
If you would like to learn virtual environments on your own, then RealPython's article
[Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)
is an excellent place to start.


## Running Tests

To run the example tests from the command line, run `python -m pytest` from the project root directory.
This command will discover and run all tests in the project.

You can also run tests using the shorter `pytest` command.
However, I recommend always using the lengthier `python -m pytest` command.
The lengthier command automatically adds the current directory to `sys.path`
so that all modules in the project can be discovered.

The pytest command has several command line options.
Course material will cover many of them.
Check out the [Usage and Invocations](https://docs.pytest.org/en/stable/usage.html) page
for complete documentation.

*Warning:*
If you attempt to run tests from this example project,
make sure to checkout the correct branch first!
