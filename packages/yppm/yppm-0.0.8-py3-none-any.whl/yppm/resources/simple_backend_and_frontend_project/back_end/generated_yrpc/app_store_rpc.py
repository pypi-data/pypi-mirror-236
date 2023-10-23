from .app_store_objects import *


from fastapi import APIRouter, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os


router = APIRouter()


class Service_app_store:
    async def add_app(self, headers: dict[str, str], item: Add_App_Request) -> Add_App_Response:
        default_response = Add_App_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    async def search_app(self, headers: dict[str, str], item: Search_App_Request) -> Search_App_Response:
        default_response = Search_App_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    async def get_app_detail(self, headers: dict[str, str], item: Get_App_Detail_Request) -> Get_App_Detail_Response:
        default_response = Get_App_Detail_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response

    async def export_data(self, headers: dict[str, str], item: Export_Data_Request) -> Export_Data_Response:
        default_response = Export_Data_Response()

        try:
            pass
        except Exception as e:
            print(f"Error: {e}")
            #default_response.error = str(e)
            #default_response.success = False

        return default_response


def init(service_instance: Any):
    @router.post("/add_app/", tags=["app_store"])
    async def add_app(request: Request, item: Add_App_Request) -> Add_App_Response:
        item = Add_App_Request().from_dict(item.to_dict())
        headers = dict(request.headers.items())
        return (await service_instance.add_app(headers, item)).to_dict()

    @router.post("/search_app/", tags=["app_store"])
    async def search_app(request: Request, item: Search_App_Request) -> Search_App_Response:
        item = Search_App_Request().from_dict(item.to_dict())
        headers = dict(request.headers.items())
        return (await service_instance.search_app(headers, item)).to_dict()

    @router.post("/get_app_detail/", tags=["app_store"])
    async def get_app_detail(request: Request, item: Get_App_Detail_Request) -> Get_App_Detail_Response:
        item = Get_App_Detail_Request().from_dict(item.to_dict())
        headers = dict(request.headers.items())
        return (await service_instance.get_app_detail(headers, item)).to_dict()

    @router.post("/export_data/", tags=["app_store"])
    async def export_data(request: Request, item: Export_Data_Request) -> Export_Data_Response:
        item = Export_Data_Request().from_dict(item.to_dict())
        headers = dict(request.headers.items())
        return (await service_instance.export_data(headers, item)).to_dict()


def run(service_instance: Any, port: str, html_folder_path: str="", serve_html_under_which_url: str="/"):
    init(service_instance=service_instance)

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        router,
        prefix="/app_store",
    )

    if (html_folder_path != ""):
        if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
            app.mount(serve_html_under_which_url, StaticFiles(directory=html_folder_path, html = True), name="web")
            @app.get(serve_html_under_which_url, response_model=str)
            async def index_page():
                return FileResponse(os.path.join(html_folder_path, 'index.html'))
            @app.exception_handler(404) #type: ignore
            async def custom_404_handler(_, __): #type: ignore
                return FileResponse(os.path.join(html_folder_path, 'index.html'))
            print(f"The website is running at: http://127.0.0.1:{port}/")
        else:
            print(f"Error: You should give me an absolute html_folder_path than {html_folder_path}")

    print(f"You can see the docs here: http://127.0.0.1:{port}/docs")
    uvicorn.run( #type: ignore
        app=app,
        host="0.0.0.0",
        port=int(port)
    ) 


if __name__ == "__main__":
    service_instance = Service_app_store()
    run(service_instance, port="6060")