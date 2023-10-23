from typing import Any
import sys
import multiprocessing
from time import sleep
from datetime import datetime
import multiprocessing
import os
import re
import json

from auto_everything.terminal import Terminal, Terminal_User_Interface
from auto_everything.python import Python
from auto_everything.disk import Disk, Store
from auto_everything.io import IO
from auto_everything.time import Time
terminal = Terminal()
terminal_user_interface = Terminal_User_Interface()
disk = Disk()
python = Python()
io_ = IO()
time_ = Time()

import generated_yrpc.app_store_objects as app_store_objects
import generated_yrpc.app_store_pure_python_rpc as app_store_pure_python_rpc
from generated_yrpc.app_store_yingshaoxo_database_rpc import Yingshaoxo_Database_Excutor_app_store

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    #print('running in a PyInstaller bundle')
    def resource_path(relative_path: str) -> str:
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path) #type: ignore
        return os.path.join(os.path.abspath("."), relative_path)
    resource_basic_folder_path = resource_path(".")
    the_database_path = disk.join_paths(disk.get_parent_directory_path(disk.get_parent_directory_path(resource_basic_folder_path)), './database_data')
else:
    #print('running in a normal Python process')
    resource_basic_folder_path = disk.get_directory_path(__file__)
    the_database_path = disk.join_paths(resource_basic_folder_path, './database_data')

print(f"resource_basic_folder_path: {resource_basic_folder_path}")
print(f"database_path: {the_database_path}")
print()
disk.create_a_folder(the_database_path)
multiprocess_manager_socket_service = multiprocessing.Manager()
global_shared_dict = multiprocess_manager_socket_service.dict()
database_excutor_for_remote_service = Yingshaoxo_Database_Excutor_app_store(database_base_folder=the_database_path, use_sqlite=False, global_multiprocessing_shared_dict=global_shared_dict)


class App_Store_Service(app_store_pure_python_rpc.Service_app_store):
    def add_app(self, headers: dict[str, str], item: app_store_objects.Add_App_Request) -> app_store_objects.Add_App_Response:
        default_response = app_store_objects.Add_App_Response()

        try:
            search_list = database_excutor_for_remote_service.An_App.search(item_filter=app_store_objects.An_App(name=item.an_app.name))
            if len(search_list) == 0:
                item.an_app.create_time_in_10_numbers_timestamp_format = time_.get_current_timestamp_in_10_digits_format()
                database_excutor_for_remote_service.An_App.add(item=item.an_app)
                default_response.app_name = item.an_app.name
            else:
                default_response.error = f"The '{item.an_app.name}' is already in our website.\n\nTry to use a different name."
        except Exception as e:
            print(f"Error: {e}")
            default_response.error = str(e)
            #default_response.success = False

        return default_response

    def search_app(self, headers: dict[str, str], item: app_store_objects.Search_App_Request) -> app_store_objects.Search_App_Response:
        default_response = app_store_objects.Search_App_Response()

        try:
            if item.search_input.strip() == "":
                search_list = database_excutor_for_remote_service.An_App.search(item_filter=app_store_objects.An_App(), page_number=item.page_number, page_size=item.page_size)
                default_response.app_list = search_list
            else:
                def a_handler(raw_json_text: str) -> dict[str, Any] | None:
                    search_text = item.search_input
                    json_object = json.loads(raw_json_text)
                    if search_text.lower() in str(json_object).lower():
                        return json_object
                    return None
                search_list = database_excutor_for_remote_service.An_App.raw_search(one_row_json_string_handler=a_handler, page_number=item.page_number, page_size=item.page_size)
                default_response.app_list = search_list
        except Exception as e:
            print(f"Error: {e}")
            default_response.error = str(e)
            #default_response.success = False

        return default_response

    def get_app_detail(self, headers: dict[str, str], item: app_store_objects.Get_App_Detail_Request) -> app_store_objects.Get_App_Detail_Response:
        default_response = app_store_objects.Get_App_Detail_Response()

        try:
            search_list = database_excutor_for_remote_service.An_App.search(item_filter=app_store_objects.An_App(name=item.name))
            if len(search_list) != 0:
                default_response.an_app = search_list[0]
        except Exception as e:
            print(f"Error: {e}")
            default_response.error = str(e)
            #default_response.success = False

        return default_response

    def export_data(self, headers: dict[str, str], item: app_store_objects.Export_Data_Request) -> app_store_objects.Export_Data_Response:
        default_response = app_store_objects.Export_Data_Response()

        try:
            temp_zip_file = disk.get_a_temp_file_path("backup.zip")
            disk.compress(input_folder_path=the_database_path, output_zip_path=temp_zip_file)
            bytes_io_data = disk.get_bytesio_from_a_file(temp_zip_file)
            default_response.file_bytes_in_base64_format = disk.bytesio_to_base64(bytes_io_data)
            default_response.file_name = "app_store_backup.zip"
        except Exception as e:
            print(f"Error: {e}")
            default_response.error = str(e)
            #default_response.success = False

        return default_response


def generate_robots_txt_and_sitemap_xml(domain: str, output_folder: str):
    if not disk.exists(output_folder):
        print(f"Can't generate robots.txt and sitemap.xml to {output_folder}")
        return

    import urllib.parse
    robots = f"""
User-agent: *
Sitemap: {domain}/sitemaps.xml
""".strip()

    sitemap_part = """
"""
    sitemap_part_list = []
    search_list = database_excutor_for_remote_service.An_App.search(item_filter=app_store_objects.An_App())
    for one in search_list:
        last_modify_time = time_.get_datetime_object_from_timestamp(one.create_time_in_10_numbers_timestamp_format).strftime("%y-%m-%d")
        safe_name = urllib.parse.quote_plus(one.name)
        sitemap_part_list.append(f"""
   <url>
      <loc>{domain}/app_page?name={safe_name}</loc>
      <lastmod>{last_modify_time}</lastmod>
      <changefreq>weekly</changefreq>
      <priority>0.8</priority>
   </url>
""")
    sitemap_part_list_text = "\n".join(sitemap_part_list)

    sitemap = f"""
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_part_list_text}
</urlset>
""".strip()

    robot_txt_path = disk.join_paths(output_folder, "robots.txt")
    io_.write(robot_txt_path, robots)

    sitemap_xml_path = disk.join_paths(output_folder, "sitemap.xml")
    io_.write(sitemap_xml_path, sitemap)


def run_service(port: str):
    database_excutor_for_remote_service.An_App.database_of_yingshaoxo.refactor_database()
    service_instance = App_Store_Service()

    html_folder_path = "../front_end/dist"
    generate_robots_txt_and_sitemap_xml(domain="http://127.0.0.1:3333", output_folder=html_folder_path)
    app_store_pure_python_rpc.run(service_instance, port=port, html_folder_path=html_folder_path)


run_service("3333")
