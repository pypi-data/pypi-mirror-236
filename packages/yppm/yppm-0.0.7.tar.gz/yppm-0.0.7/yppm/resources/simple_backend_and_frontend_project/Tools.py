#!/usr/bin/env /home/yingshaoxo/anaconda3/bin/python3
import os

from auto_everything.base import Python, Terminal
from auto_everything.develop import YRPC
from auto_everything.disk import Disk
from auto_everything.database import Database_Of_Yingshaoxo


py = Python()
t = Terminal()
yrpc = YRPC()
disk = Disk()


class Tools():
    def __init__(self) -> None:
        self.project_root_folder = disk.get_directory_path(os.path.realpath(os.path.abspath(__file__)))

    def generate_protocol_files(self):
        input_folder=disk.join_paths(self.project_root_folder, "./protocol")
        input_files = ["app_store.proto"]
        output_folder_for_python=disk.join_paths(self.project_root_folder, "./back_end/generated_yrpc")
        output_folder_for_javascript=disk.join_paths(self.project_root_folder, "./front_end/src/generated_yrpc")

        yrpc.generate_code(
            which_language="typescript",
            input_folder=input_folder,
            input_files=input_files,
            output_folder=output_folder_for_javascript
        )

        yrpc.generate_code(
            which_language="python",
            input_folder=input_folder,
            input_files=input_files,
            output_folder=output_folder_for_python
        )

        Database_Of_Yingshaoxo.generate_code_from_yrpc_protocol(
            which_language="python",
            input_folder=input_folder,
            input_files=input_files,
            output_folder=output_folder_for_python
        )

    def build_front_end(self):
        t.run(f"""
        cd {self.project_root_folder}
        cd front_end
        npm i
        npm run build
        #rm -fr ../back_end/vue/*
        #mkdir -p ../back_end/vue/*
        #cp -fr dist/* ../back_end/vue/
        """)

    # def rebuild_docker_image(self):
    #     # self.build_front_end()
    #     t.run(f"""
    #     cd {self.project_root_folder}
    #     docker-compose -f docker-compose.service.yaml down
    #     docker rmi yingshaoxo/it_has_alternatives
    #     docker-compose -f docker-compose.service.yaml up -d
    #     """)


py.make_it_runnable()
py.fire(Tools)
