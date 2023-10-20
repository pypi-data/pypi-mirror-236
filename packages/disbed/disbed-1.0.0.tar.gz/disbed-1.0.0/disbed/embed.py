from pydantic import BaseModel
import requests

class BaseEmbed(BaseModel):
    title: str
    redirect: str = None
    url: str = 'https://discord.com/'
    color: str = None
    image: str = None
    thumbnail: str = None
    description: str

class Embed:
    def __init__(self):
        self.base_embed = BaseEmbed(title="", description="")

    def create(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.base_embed, key):
                setattr(self.base_embed, key, value)

    def render(self):
        return {
            "title": self.base_embed.title,
            "url": self.base_embed.url,
            "color": self.base_embed.color,
            "image": self.base_embed.image,
            "thumbnail": self.base_embed.thumbnail,
            "description": self.base_embed.description
        }

    def send_to_server(self):
        server_url = 'https://server.sky.repl.co/api/create'
        base_url = 'https://server.sky.repl.co/'
        try:
            response = requests.post(server_url, json=self.render())
            if response.status_code == 200:
                return {"url": base_url + response.json().get('id'), "message": "success"}
            else:
                return {"error": f"Server returned status code {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request error: {e}"}

    def __str__(self):
        return f"Embed with title: {self.base_embed.title}"

    def to_dict(self):
        return {
            "title": self.base_embed.title,
            "description": self.base_embed.description,
        }

    def __repr__(self):
        return f"Embed(title='{self.base_embed.title}', description='{self.base_embed.description}')"

    @classmethod
    def from_dict(cls, data):
        embed = cls()
        title = data.get("title", "")
        description = data.get("description", "")
        embed.create(title=title, description=description)
        return embed
