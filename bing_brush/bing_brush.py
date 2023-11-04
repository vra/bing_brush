from http.cookies import SimpleCookie
import os
import random

# import re
import time

# from functools import partial

import requests
from requests.utils import cookiejar_from_dict

import regex


class BingBrush:
    def __init__(
        self,
        cookie,
        verbose=False,
        max_wait_time=600,
    ):
        self.max_wait_time = max_wait_time
        self.verbose = verbose

        self.session = self.construct_requests_session(cookie)

        self.prepare_error_messages()

    def parse_cookie(self, cookie_string):
        cookie = SimpleCookie()
        if os.path.exists(cookie_string):
            with open(cookie_string) as f:
                cookie_string = f.read()

        cookie.load(cookie_string)
        cookies_dict = {}
        cookiejar = None
        for key, morsel in cookie.items():
            cookies_dict[key] = morsel.value
            cookiejar = cookiejar_from_dict(
                cookies_dict, cookiejar=None, overwrite=True
            )
        return cookiejar

    def prepare_error_messages(self):
        self.error_message_dict = {
            "error_blocked_prompt": "Your prompt has been blocked by Bing. Try to change any bad words and try again.",
            "error_being_reviewed_prompt": "Your prompt is being reviewed by Bing. Try to change any sensitive words and try again.",
            "error_noresults": "Could not get results.",
            "error_unsupported_lang": "this language is currently not supported by bing.",
            "error_timeout": "Your request has timed out.",
            "error_redirect": "Redirect failed",
            "error_bad_images": "Bad images",
            "error_no_images": "No images",
        }

    def construct_requests_session(self, cookie):
        # Generate random IP between range 13.104.0.0/14
        FORWARDED_IP = f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        HEADERS = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "referrer": "https://www.bing.com/images/create/",
            "origin": "https://www.bing.com",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
            "x-forwarded-for": FORWARDED_IP,
        }

        session = requests.Session()
        session.headers = HEADERS
        session.cookies = self.parse_cookie(cookie)
        return session

    def process_error(self, response):
        for error_type, error_msg in self.error_message_dict.items():
            if error_msg in response.text.lower():
                return Exception(error_type)

    def request_result_urls(self, response, url_encoded_prompt):
        redirect_url = response.headers["Location"].replace("&nfy=1", "")
        request_id = redirect_url.split("id=")[-1]
        self.session.get(f"https://www.bing.com{redirect_url}")
        polling_url = f"https://www.bing.com/images/create/async/results/{request_id}?q={url_encoded_prompt}"
        # Poll for results
        start_wait = time.time()
        while True:
            if int(time.time() - start_wait) > self.max_wait_time:
                raise Exception(self.error_message_dict["error_timeout"])
            response = self.session.get(polling_url)
            if response.status_code != 200:
                raise Exception(self.error_message_dict["error_noresults"])
            if not response.text or response.text.find("errorMessage") != -1:
                time.sleep(1)
                continue
            else:
                break

        image_links = regex.findall(r'src="([^"]+)"', response.text)
        normal_image_links = [link.split("?w=")[0] for link in image_links]
        normal_image_links = list(set(normal_image_links))

        return normal_image_links

    def send_request(self, prompt):
        url_encoded_prompt = requests.utils.quote(prompt)
        payload = f"q={url_encoded_prompt}&qs=ds"
        url = f"https://www.bing.com/images/create?q={url_encoded_prompt}&rt=4&FORM=GENCRE"
        response = self.session.post(
            url,
            allow_redirects=False,
            data=payload,
            timeout=self.max_wait_time,
        )
        return response, url_encoded_prompt

    def process(self, prompt, out_folder):
        response, url_encoded_prompt = self.send_request(prompt)

        if response.status_code != 302:
            self.process_error(response)

        img_urls = self.request_result_urls(response, url_encoded_prompt)

        os.makedirs(out_folder, exist_ok=True)
        for url in img_urls:
            self.write_image(url, out_folder)

    def write_image(self, url, out_folder):
        response = requests.get(url)
        if response.status_code == 200:
            file_name = url.split("/")[-1]
            save_path = os.path.join(out_folder, file_name) + ".jpg"

            with open(save_path, "wb") as file:
                file.write(response.content)
            if self.verbose:
                print(f"图像已成功下载并保存为：{save_path}")
        else:
            print("下载失败！")


## Error messages
## Action messages
# sending_message = "Sending request..."
# wait_message = "Waiting for results..."
# download_message = "\nDownloading images..."
#
#
# class ImageGen:
#    """
#    Image generation by Microsoft Bing
#    Parameters:
#        auth_cookie: str
#    Optional Parameters:
#        debug_file: str
#        quiet: bool
#        all_cookies: List[Dict]
#    """
#
#    def __init__(
#        self,
#        auth_cookie: str,
#        debug_file: Union[str, None] = None,
#        quiet: bool = False,
#        all_cookies: List[Dict] = None,
#    ) -> None:
#        self.session: requests.Session = requests.Session()
#        self.session.headers = HEADERS
#        self.session.cookies = self.parse_cookie_string(auth_cookie)
#        self.quiet = quiet
#        self.debug_file = debug_file
#
#    @staticmethod
#    def parse_cookie_string(cookie_string):
#        cookie = SimpleCookie()
#        cookie.load(cookie_string)
#        cookies_dict = {}
#        cookiejar = None
#        for key, morsel in cookie.items():
#            cookies_dict[key] = morsel.value
#            cookiejar = cookiejar_from_dict(
#                cookies_dict, cookiejar=None, overwrite=True
#            )
#        return cookiejar
#
#    def get_limit_left(self) -> int:
#        r = self.session.get("https://www.bing.com/create")
#        if not r.ok:
#            raise Exception("Can not get limit left from this `cookie` please check")
#        value = re.search(
#            r'<div id="token_bal" aria-label="[0-9]+.*">([0-9]+)</div>', r.text
#        )
#        if not value:
#            return 0
#        if value.group(1).isnumeric():
#            return int(value.group(1))
#        else:
#            print(f"error value: {value.group(1)} just return 0")
#            return 0
#
#    def get_images(self, prompt: str) -> list:
#        """
#        Fetches image links from Bing
#        Parameters:
#            prompt: str
#        """