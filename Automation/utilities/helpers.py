import random
import string
from datetime import datetime, timedelta


# ── Random Data Generators ────────────────────────────────────────────────────

def random_email():
    """Generate a unique email for each test run."""
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"test_{suffix}@playwright.com"

def random_name():
    """Generate a random first name."""
    names = ["Alice", "Bob", "Carol", "David", "Eva", "Frank", "Grace", "Henry"]
    return random.choice(names)

def future_date(days=30):
    """Return a date N days from today in YYYY-MM-DD format."""
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

def past_date(days=30):
    """Return a date N days ago in YYYY-MM-DD format."""
    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

def today():
    return datetime.now().strftime("%Y-%m-%d")


# ── Screenshot Helper ─────────────────────────────────────────────────────────

def take_screenshot(page, name):
    """Take a screenshot and save to screenshots folder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"screenshots/{name}_{timestamp}.png"
    page.screenshot(path=path)
    print(f"📸 Screenshot saved: {path}")
    return path


# ── Wait Helpers ──────────────────────────────────────────────────────────────

def wait_for_alert(page, alert_type="success", timeout=5000):
    """Wait for a Bootstrap alert to appear."""
    selector = f".alert-{alert_type}"
    page.wait_for_selector(selector, timeout=timeout)
    return page.text_content(selector)

def wait_for_url_contains(page, path, timeout=5000):
    """Wait until URL contains given path."""
    page.wait_for_function(
        f"window.location.href.includes('{path}')",
        timeout=timeout
    )
