import time
import csv
import queue
from concurrent import futures
from fake_useragent import FakeUserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

INPUT_DATA_FILE = "data_combined.csv"


class Translator:
    SERVER = "100.64.0.1:4444"
    SELENIUM_SERVER = f"http:///{SERVER}/wd/hub"

    def __init__(self, num_start=0, num_end=25, thread_count=5):
        self.num_start = num_start
        self.num_end = num_end
        self.thread_count = thread_count
        self.queue = queue.Queue()

    def get_driver(self):
        fua = FakeUserAgent(os=["windows"])

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument(f"--user-agent={fua.random}")

        return webdriver.Remote(command_executor=self.SERVER, options=options)

    def translate(self, driver, input_str: str) -> str:
        type_box = driver.find_element(By.CSS_SELECTOR, "d-textarea.min-h-0 > div:nth-child(1)")
        type_box.send_keys(input_str)

        output_box_css = "section.flex > div:nth-child(2)"

        output_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, output_box_css)))

        time.sleep(1.25)
        driver.implicitly_wait(10)

        texts = output_box.find_elements(By.TAG_NAME, "p")

        return " ".join(map(lambda x: x.text, texts))

    def worker(self):
        while not self.queue.empty():
            req = self.queue.get()
            if req is None:
                break

            text, aspect, label = req
            driver = self.get_driver()

            try:
                driver.get("https://www.deepl.com")
                time.sleep(1)
                translated_text = self.translate(driver, text)
                translated_aspect = self.translate(driver, aspect)
                print(translated_text, translated_aspect)
                result = (translated_text, translated_aspect, label)
                return result
            except Exception as e:
                print(e)
            finally:
                driver.quit()

            self.queue.task_done()

    def run(self):
        requests = self.prepare_requests()

        for req in requests:
            self.queue.put(req)

        with futures.ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            results = list(executor.map(lambda _: self.worker(), range(self.thread_count)))

        self.save_results([result for result in results if result is not None])

    def prepare_requests(self):
        label_map = {"positive": "pozitif", "negative": "negatif", "neutral": "nötr"}

        with open(INPUT_DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            requests = [(_t, _a, label_map.get(_l, "nötr")) for _t, _l, _a in zip(*reader)][
                self.num_start : self.num_end
            ]

        return requests

    def save_results(self, translated_texts):
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(map(str, translated_texts)))


if __name__ == "__main__":
    translator = Translator(num_start=0, num_end=25, thread_count=5)
    translator.run()
