from typing import List
from typing import Optional

from fastapi import Request


class ApiCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.name: Optional[str] = None
        self.provider: Optional[str] = None
        self.url: Optional[str] = None
        self.category: Optional[str] = None
        self.description: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.provider = form.get("provider")
        self.url = form.get("url")
        self.category = form.get("category")
        self.description = form.get("description")

    def is_valid(self):
        if not self.name or not len(self.name) >= 4:
            self.errors.append("A valid name is required")
        if not self.url or not (self.url.__contains__("http")):
            self.errors.append("Valid Url is required e.g. https://example.com")
        if not self.provider or not len(self.provider) >= 1:
            self.errors.append("A valid provider is required")
        if not self.description or not len(self.description) >= 20:
            self.errors.append("Description too short")
        if not self.errors:
            return True
        return False
