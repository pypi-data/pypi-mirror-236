from .app_store_objects import *


from typing import Any
import json
from auto_everything.http_ import Yingshaoxo_Http_Server, Yingshaoxo_Http_Request


class Service_app_store:
    def add_app(self, headers: dict[str, str], item: Add_App_Request) -> Add_App_Response:
        default_response = Add_App_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def search_app(self, headers: dict[str, str], item: Search_App_Request) -> Search_App_Response:
        default_response = Search_App_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def get_app_detail(self, headers: dict[str, str], item: Get_App_Detail_Request) -> Get_App_Detail_Response:
        default_response = Get_App_Detail_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    def export_data(self, headers: dict[str, str], item: Export_Data_Request) -> Export_Data_Response:
        default_response = Export_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response


def run(service_instance: Service_app_store, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    def handle_get_url(sub_url: str, headers: dict[str, str]) -> str:
        return 'Hi there, this website is using yrpc (Yingshaoxo remote procedure control module).'

    def handle_post_url(sub_url: str, headers: dict[str, str], item: dict[str, Any]) -> dict | str:
        sub_url = sub_url.strip("/")
        sub_url = sub_url.replace("app_store", "", 1)
        sub_url = sub_url.strip("/")
        request_url = sub_url.split("/")[0].strip()

        if (request_url == ""):
            return f"Request url '{request_url}' is empty"
        elif (request_url == "add_app"):
            correct_item = Add_App_Request().from_dict(item)
            return json.dumps((service_instance.add_app(headers, correct_item)).to_dict())

        elif (request_url == "search_app"):
            correct_item = Search_App_Request().from_dict(item)
            return json.dumps((service_instance.search_app(headers, correct_item)).to_dict())

        elif (request_url == "get_app_detail"):
            correct_item = Get_App_Detail_Request().from_dict(item)
            return json.dumps((service_instance.get_app_detail(headers, correct_item)).to_dict())

        elif (request_url == "export_data"):
            correct_item = Export_Data_Request().from_dict(item)
            return json.dumps((service_instance.export_data(headers, correct_item)).to_dict())

        return f"No API url matchs '{request_url}'"

    def general_handler(request: Yingshaoxo_Http_Request) -> dict | str:
        response = f"No handler for {request.url}"
        if request.method == "GET":
            response = handle_get_url(request.url, request.headers)
        elif request.method == "POST":
            response = handle_post_url(request.url, request.headers, json.loads(request.payload))
        return response

    router = {
        r"(.*)": general_handler,
    }

    yingshaoxo_http_server = Yingshaoxo_Http_Server(router=router)
    yingshaoxo_http_server.start(host="0.0.0.0", port=int(port), html_folder_path=html_folder_path, serve_html_under_which_url=serve_html_under_which_url)


if __name__ == "__main__":
    service_instance = Service_app_store()
    run(service_instance, port="6060")