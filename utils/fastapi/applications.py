from typing import Any, Dict

from fastapi import FastAPI

from .openapi import base_get_openapi


class BaseFastAPI(FastAPI):
    def openapi(self) -> Dict[str, Any]:
        if not self.openapi_schema:
            self.openapi_schema = base_get_openapi(
                title=self.title,
                version=self.version,
                openapi_version=self.openapi_version,
                description=self.description,
                routes=self.routes,
                tags=self.openapi_tags,
                servers=self.servers,
            )
        return self.openapi_schema
