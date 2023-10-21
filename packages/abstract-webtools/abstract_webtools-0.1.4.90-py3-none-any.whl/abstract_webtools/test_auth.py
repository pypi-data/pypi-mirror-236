from abstract_webtools import UrlManager,SafeRequest,SoupManager,LinkManager,VideoDownloader
from abstract_security.envy_it import get_env_value
from abstract_utilities.read_write_utils import read_from_file
url = "https://vk.com"
username = get_env_value(key='vk_login')
password= get_env_value(key='vk_pass')
url_manager = UrlManager(url=url)
request_manager = SafeRequest(url_manager=url_manager,
                              proxies={'8.219.195.47','8.219.197.111'},
                              password=password,
                              email=username)
input(request_manager.react_source_code)
