"""
This module contains shared fixtures.
"""

import pytest
import json
import yaml
import allure
import os
import tempfile
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException
from utils.logger import log
import time
import json as jsonlib
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for tests: chrome | firefox | headless"
    )

    parser.addoption(
        "--browsers",
        action="store",
        default="",
        help="Comma-separated browsers to run in parallel (e.g. chrome,firefox). Overrides --browser."
    )
    parser.addoption(
        "--grid-wait-timeout",
        action="store",
        default=60,
        type=int,
        help="Seconds to wait for Selenium Grid to be ready with required slots."
    )
    parser.addoption(
        "--implicit-wait",
        action="store",
        default=10,
        type=int,
        help="Implicit wait time in seconds"
    )


def _get_worker_id(pytestconfig):
    worker = getattr(pytestconfig, "workerinput", None)
    if worker and "workerid" in worker:
        return worker["workerid"]
    return os.environ.get("PYTEST_XDIST_WORKER", "master")

def _parse_browsers(pytestconfig):
    raw = (pytestconfig.getoption("--browsers") or "").strip()
    if raw:
        browsers = [b.strip() for b in raw.split(",") if b.strip()]
        return browsers
    return [pytestconfig.getoption("--browser")]


def _attach_debug_artifacts(driver, test_name):
    if not driver:
        return

    try:
        allure.attach(driver.current_url, "Current URL", allure.attachment_type.TEXT)
    except Exception as e:
        log.warning(f"Failed to attach current URL: {e}")

    try:
        allure.attach(driver.page_source, "Page Source", allure.attachment_type.HTML)
    except Exception as e:
        log.warning(f"Failed to attach page source: {e}")

    try:
        caps = getattr(driver, "capabilities", None)
        if caps:
            allure.attach(json.dumps(caps, indent=2), "Capabilities", allure.attachment_type.JSON)
    except Exception as e:
        log.warning(f"Failed to attach capabilities: {e}")

    try:
        browser_logs = driver.get_log("browser")
        if browser_logs:
            allure.attach(
                "\n".join([str(entry) for entry in browser_logs]),
                "Browser Console Logs",
                allure.attachment_type.TEXT,
            )
    except Exception as e:
        # Not all drivers support log collection
        log.debug(f"Browser logs unavailable: {e}")

    try:
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{test_name}_FAILURE.png")
        driver.save_screenshot(screenshot_path)
        allure.attach.file(
            screenshot_path,
            name=f"Failure Screenshot - {test_name}",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as e:
        log.warning(f"Failed to capture screenshot: {e}")


def load_grid_url_from_docker_compose():

    with open("docker-compose.yml", "r") as f:
        compose = yaml.safe_load(f)

    hub = compose["services"]["selenium-hub"]

    # Extract port mapping (e.g., "4444:4444")
    port_mapping = hub["ports"][0]
    host_port = port_mapping.split(":")[0]

    return f"http://localhost:{host_port}/wd/hub"


def _expected_slots_by_browser(pytestconfig, browsers):
    num = pytestconfig.getoption("numprocesses") or 0
    if not num or num < 1:
        # No xdist: require one slot for the first browser
        return {browsers[0]: 1}

    counts = {b: 0 for b in browsers}
    for i in range(num):
        counts[browsers[i % len(browsers)]] += 1
    return counts


def _count_available_slots(payload):
    counts = {}
    nodes = payload.get("value", {}).get("nodes", [])
    for node in nodes:
        for slot in node.get("slots", []):
            if slot.get("session") is not None:
                continue
            browser = slot.get("stereotype", {}).get("browserName")
            if browser:
                counts[browser] = counts.get(browser, 0) + 1
    return counts


def _wait_for_grid_ready(grid_url, pytestconfig, timeout_seconds=60):
    status_url = grid_url.replace("/wd/hub", "/status")
    deadline = time.time() + timeout_seconds
    last_error = None
    browsers = _parse_browsers(pytestconfig)
    expected = _expected_slots_by_browser(pytestconfig, browsers)

    while time.time() < deadline:
        try:
            req = Request(status_url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=5) as resp:
                data = resp.read().decode("utf-8")
            payload = jsonlib.loads(data)
            ready = payload.get("value", {}).get("ready", False)
            if ready:
                available = _count_available_slots(payload)
                if all(available.get(b, 0) >= expected[b] for b in expected):
                    return True
                last_error = f"Grid ready but slots unavailable. Expected: {expected}, Available: {available}"
            else:
                last_error = f"Grid not ready yet: {payload.get('value')}"
        except (URLError, HTTPError, ValueError) as e:
            last_error = str(e)

        time.sleep(2)

    raise RuntimeError(f"Selenium Grid not ready within {timeout_seconds}s. Last error: {last_error}")


@pytest.fixture(scope="session")
def config(pytestconfig):

    grid_url = load_grid_url_from_docker_compose()
    # Only the master process should gate on Grid readiness; workers may race.
    if os.environ.get("PYTEST_XDIST_WORKER") is None:
        _wait_for_grid_ready(
            grid_url,
            pytestconfig,
            timeout_seconds=pytestconfig.getoption("--grid-wait-timeout"),
        )

    # Read CLI args
    browser = pytestconfig.getoption("--browser")
    implicit_wait = pytestconfig.getoption("--implicit-wait")

    # Validate
    if browser not in ["chrome", "firefox", "headless"]:
        pytest.fail(f"Invalid --browser value: '{browser}'. Must be chrome, firefox, or headless.")
    if implicit_wait <= 0:
        pytest.fail("--implicit-wait must be greater than 0.")

    return {
        "grid_url": grid_url,
        "browser": browser,
        "implicit_wait": implicit_wait
    }


@pytest.fixture(scope="session")
def json_config():

    # Read the file
    with open("config.json") as f:
        config = json.load(f)

    # Validate values
    valid_browsers = ['chrome', 'firefox', 'safari', 'opera', 'edge', 'Headless Chrome']
    if config['browser'] not in valid_browsers:
        pytest.fail(f"Invalid browser in config.json: '{config['browser']}'. Must be one of: {valid_browsers}")
    if not isinstance(config['implicit_wait'], int) or config['implicit_wait'] <= 0:
        pytest.fail("implicit_wait in config.json must be a positive integer.")

    # Return config for use
    return config


@pytest.fixture
def browser(config, pytestconfig, request):

    grid_url = config["grid_url"]
    browsers = _parse_browsers(pytestconfig)
    worker_id = _get_worker_id(pytestconfig)

    # Prefer explicit parametrization if provided; otherwise map workers to browsers.
    if getattr(request, "param", None):
        browser_name = request.param
    elif len(browsers) > 1:
        # Distribute browsers across xdist workers (gw0, gw1, ...)
        idx = 0
        if worker_id.startswith("gw"):
            try:
                idx = int(worker_id[2:])
            except ValueError:
                idx = 0
        browser_name = browsers[idx % len(browsers)]
    else:
        browser_name = browsers[0]

    # Initialize the WebDriver instance

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        # Remote Grid runs inside Docker; use a container-local writable dir.
        options.add_argument(f"--user-data-dir=/tmp/chrome-profile-{worker_id}")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()

    elif browser_name == "safari":
        options = webdriver.SafariOptions()

    elif browser_name == "headless":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--user-data-dir=/tmp/chrome-profile-{worker_id}")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
    else:
        raise Exception(f"Unsupported browser: {browser_name}")

    browser = None
    last_error = None
    for attempt in range(2):
        try:
            browser = webdriver.Remote(
                command_executor=grid_url,
                options=options
            )
            break
        except WebDriverException as e:
            last_error = e
            log.warning(f"Grid session attempt {attempt + 1} failed: {e}")
            time.sleep(3)

    if not browser:
        raise last_error

    # Add browser label to Allure for quick filtering
    try:
        allure.dynamic.label("browser", browser_name)
    except Exception:
        pass

    # Make its calls wait up to 10 seconds for elements to appear
    browser.implicitly_wait(config['implicit_wait'])

    # Return the WebDriver instance for the setup
    log.info("Setting up and initializing WebDriver browser for the test...")
    yield browser

    # Quit the WebDriver instance for the cleanup
    log.info("Tearing down WebDriver browser.")
    browser.quit()


@pytest.fixture
def json_browser(json_config, pytestconfig):
    worker_id = _get_worker_id(pytestconfig)

    # Initialize the WebDriver instance
    if json_config['browser'] == 'chrome':
        options = webdriver.ChromeOptions()
        profile_dir = tempfile.mkdtemp(prefix=f"chrome-profile-{worker_id}-")
        options.add_argument(f"--user-data-dir={profile_dir}")
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif json_config['browser'] == 'firefox':
        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif json_config['browser'] == 'safari':
        opts = webdriver.SafariOptions()
        opts.set_capability("safari:useNonPersistentSession", True)
        browser = webdriver.Safari(options=opts)
    elif json_config['browser'] == 'Headless Chrome':
        opts = webdriver.ChromeOptions()
        opts.add_argument('--headless=new')
        opts.add_argument('--disable-gpu')
        profile_dir = tempfile.mkdtemp(prefix=f"chrome-profile-{worker_id}-")
        opts.add_argument(f"--user-data-dir={profile_dir}")
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)
    else:
        raise Exception(f"Unsupported browser: {json_config['browser']}")

    # Make its calls wait up to 10 seconds for elements to appear
    browser.implicitly_wait(json_config['implicit_wait'])

    # Return the WebDriver instance for the setup
    log.info("Setting up and initializing WebDriver browser for the test...")
    yield browser

    # Quit the WebDriver instance for the cleanup
    log.info("Tearing down WebDriver browser.")
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    capture = False
    if report.when in {"call", "setup"}:
        if report.failed:
            capture = True
        # Capture artifacts for expected failures (xfail) as well.
        if getattr(report, "wasxfail", False):
            capture = True

    if capture:

        driver = None
        for name in ("browser", "json_browser"):
            try:
                driver = item.funcargs.get(name)
            except Exception:
                driver = None
            if driver:
                break
            # Fall back to requesting the fixture directly (BDD steps may not expose it in funcargs).
            if hasattr(item, "_request"):
                try:
                    driver = item._request.getfixturevalue(name)
                except Exception:
                    driver = None
                if driver:
                    break

        test_name = report.nodeid.replace("::", "_").replace("/", "_").replace(".py", "")
        _attach_debug_artifacts(driver, test_name)

        if not driver:
            log.warning("WebDriver unavailable; debug artifacts not captured.")

        try:
            # Short failure summary for quicker Allure scan
            summary = (report.longreprtext or "").splitlines()
            if summary:
                allure.attach(summary[0], "Failure Summary", allure.attachment_type.TEXT)
        except Exception:
            pass


def pytest_bdd_before_scenario(request, feature, scenario):
    allure.dynamic.feature(feature.name)
    allure.dynamic.story(scenario.name)
    try:
        allure.dynamic.title(request.node.name)
    except Exception:
        allure.dynamic.title(scenario.name)


def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        browsers = _parse_browsers(metafunc.config)
        # Only parametrize if more than one browser is requested
        if len(browsers) > 1:
            metafunc.parametrize("browser", browsers, indirect=True)


def pytest_collection_modifyitems(config, items):
    for item in items:
        if "negative" in item.keywords:
            item.add_marker(pytest.mark.xfail(reason="Intentional negative test for Allure demo", strict=False))
