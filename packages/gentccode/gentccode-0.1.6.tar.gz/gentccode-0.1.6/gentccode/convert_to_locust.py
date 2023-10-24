import re
import time
from urllib.parse import urlparse
from http_content_parser.req_data import ReqData
from http_content_parser.generate_api_file import GenerateApiFile

CHAR_SPACE_8 = "        "
CHAR_SPACE_4 = "    "


def get_import_str():
    import_str = (
        "from locust import HttpUser, TaskSet, task, events, between\n"
        + "from gevent.lock import Semaphore\n\n"
        + "all_users_spawned = Semaphore()\n"
        + "all_users_spawned.acquire()\n\n"
    )
    return import_str


def get_listener_str():
    listener_str = (
        f"@events.init.add_listener\n"
        + f"def _(environment, **kw):\n"
        + f"{CHAR_SPACE_4}@environment.events.spawning_complete.add_listener\n"
        + f"{CHAR_SPACE_4}def on_spawning_complete(**kw):\n"
        + f"{CHAR_SPACE_8}all_users_spawned.release()\n\n"
    )
    return listener_str


def get_user_class(host: str):
    http_user_class_str = (
        "class MyUser(HttpUser):\n"
        + f"{CHAR_SPACE_4}host = '{host}'\n"
        + f"{CHAR_SPACE_4}wait_time = between(1, 3)  # 定义用户间隔时间，单位秒\n"
        + f"{CHAR_SPACE_4}tasks = [UserTasks]\n\n"
    )
    return http_user_class_str


def get_user_task_class_str():
    task_set_str = (
        f"class UserTasks(TaskSet):\n"
        + f"{CHAR_SPACE_4}def on_start(self):\n"
        + f"{CHAR_SPACE_8}all_users_spawned.wait()\n"
        + f"{CHAR_SPACE_8}self.wait()\n\n"
    )
    return task_set_str


def get_task_str_of_method(payload: ReqData):
    method = payload.method
    host = payload.host
    path = payload.path
    query_param = payload.query_param
    if query_param and query_param != "{}":
        s = f'"{host}{path}{query_param}"'
    else:
        s = f'"{host}{path}"'
    if method != "get":
        var_str = f"{CHAR_SPACE_8}body_json={payload.body}\n"
        s += f", json=body_json"
    else:
        var_str = ""

    method_name = replace_api_label_chars(path)
    task_str = (
        f"{CHAR_SPACE_4}@task\n"
        + f"{CHAR_SPACE_4}def {method_name}(self):\n"
        + var_str
        + f"{CHAR_SPACE_8}with self.client.{method}({ s }) as response:\n"
        + f"{CHAR_SPACE_8}{CHAR_SPACE_4}assert response.status_code == 200, 'http response code is not 200'\n\n"
    )
    return task_str


def replace_api_label_chars(string):
    pattern = r"[-+@?={}/.]"  # 定义要匹配的特殊字符模式
    replacement = "_"  # 替换为的字符串

    new_string = re.sub(pattern, replacement, string)
    return new_string


def product_locust_code(curl_file_path):
    now_date = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    gaf = GenerateApiFile()
    http_payloads = gaf.convert_curl_data_to_model(curl_file_path)
    py_name = f"locust-{now_date}.py"
    with open(py_name, "at") as f:
        f.write(get_import_str() + get_listener_str() + get_user_task_class_str())
        host = ""
        for http_payload in http_payloads:
            task_body = get_task_str_of_method(http_payload)
            f.write(task_body)
            temp_url = http_payload.original_url
            host = _split_url(temp_url)
        f.write(get_user_class(host))


def _split_url(url):
    if url:
        parsed = urlparse(url)
        l = parsed.scheme + "://" + parsed.netloc + "/"
        return l
    else:
        return ""


if __name__ == "__main__":
    product_locust_code("")
