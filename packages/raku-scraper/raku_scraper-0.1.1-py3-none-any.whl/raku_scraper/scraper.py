import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO)


class ScrapingTask:
    """A class for defining a scraping task including the URL and actions to be performed on the webpage."""
    
    def __init__(self, url, title="", description=""):
        """Initialize the scraping task with URL, title, and description."""
        self.task = {
            "url": url,
            "title": title,
            "description": description,
            "steps": []
        }

    def add_action(self, step_id, selector, action, description=""):
        """Add an action step to the scraping task."""
        if any(step for step in self.task['steps'] if step['id'] == step_id):
            logging.warning(f"Step ID '{step_id}' already exists. Consider using a unique ID for each step.")
            return

        step = {
            "id": step_id,
            "type": "action",
            "selector": selector,
            "action": action,
            "description": description
        }
        self.task['steps'].append(step)

    def add_selector(self, step_id, selector, attribute="text", description=""):
        """Add a selector step to scrape data from the webpage."""
        if any(step for step in self.task['steps'] if step['id'] == step_id):
            logging.warning(f"Step ID '{step_id}' already exists. Consider using a unique ID for each step.")
            return

        step = {
            "id": step_id,
            "type": "selector",
            "selector": selector,
            "attribute": attribute,
            "description": description
        }
        self.task['steps'].append(step)


class Scraper:
    """A class for executing the scraping task and collecting data from the webpage."""
    
    def __init__(self, task, driver_path='chromedriver', headless=True):
        """Initialize the scraper with a scraping task, path to the webdriver, and mode."""
        self.task = task
        self.driver_path = driver_path
        self.headless = headless
        self.driver = None

    def _init_driver(self):
        """Initialize the Selenium webdriver."""
        options = Options()
        options.headless = self.headless
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=options)
        self.driver.maximize_window()
        logging.info("WebDriver initialized")

    def _close_driver(self):
        """Close the Selenium webdriver."""
        if self.driver:
            self.driver.quit()
            logging.info("WebDriver closed")

    def _execute_action(self, step):
        """Execute an action step on the webpage."""
        time.sleep(1)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, step['selector']))
            )
            
            if step['action'] == 'click':
                ActionChains(self.driver).click(element).perform()
                logging.info(f"Clicked on element {step['selector']}")
                time.sleep(3)
        except Exception as e:
            logging.error(f"Failed to execute action on {step['selector']}: {e}")

    def _scrape_data(self, step):
        """Scrape data from the webpage according to the selector step."""
        time.sleep(1)
        elements = self.driver.find_elements(By.CSS_SELECTOR, step['selector'])
        logging.info(f"Found {len(elements)} elements with selector {step['selector']}")

        data = []
        for element in elements:
            content = element.text if step['attribute'].lower() == 'text' else element.get_attribute(step['attribute'])
            data.append(content)

        logging.info(f"Scraped data: {data}")
        return {step['id']: data}

    def scrape_and_perform_actions(self):
        """Execute the scraping task and collect data."""
        if not self.driver:
            self._init_driver()

        scraped_data = {}
        try:
            self.driver.get(self.task.task['url'])
            logging.info(f"Opened webpage {self.task.task['url']}")

            for step in self.task.task['steps']:
                if step['type'] == 'action':
                    self._execute_action(step)
                elif step['type'] == 'selector':
                    scraped_data.update(self._scrape_data(step))

        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            self._close_driver()

        return scraped_data