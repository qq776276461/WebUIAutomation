
import re
import requests
from webdriver_manager.utils import validate_response, File, download_file

from src.utils.Log import init_log

log = init_log()


def get_driver_path(self, driver):
    binary_path = self.driver_cache.find_driver(driver)
    if binary_path:
        return binary_path
    url = driver.get_url()
    log.info(f"未找到对应版本的webdriver, 即将下载: {url}")
    file = download_file(url, driver.ssl_verify)
    binary_path = self.driver_cache.save_file_to_cache(driver, file)
    return binary_path


def overwrite_download_file(url: str, ssl_verify=True) -> File:
    log.info(f"未找到对应版本的webdriver, 即将下载: {url}")
    response = requests.get(url, stream=True, verify=ssl_verify)
    validate_response(response)
    return File(response)


# hook webdriver_manager第三方库中的方法, 修改firefoxdriver下载地址
def get_url(self):
    resp = requests.get(
        url=self.tagged_release_url(self.get_version()),
        headers=self.auth_header,
        verify=self.ssl_verify,
    )
    validate_response(resp)
    assets = resp.json()["assets"]

    name = f"{self.get_name()}-{self.get_version()}-{self.get_os_type()}."
    output_dict = [
        asset for asset in assets if asset['name'].startswith(name)
    ]
    result_url = output_dict[0]['browser_download_url'].replace(
        "https://github.com/mozilla/geckodriver/releases/download",
        self._url)
    return result_url


# hook webdriver_manager第三方库中的方法, 修复获取filename的bug
@property
def file_name(self) -> str:
    try:
        filename = re.findall("filename=(.+);", self._File__stream.headers["content-disposition"])[0]
    except KeyError:
        filename = f"{self._File__temp_name}.zip"
    except IndexError:
        filename = f"{self._File__temp_name}.exe"

    if '"' in filename:
        filename = filename.replace('"', "")
    return filename
