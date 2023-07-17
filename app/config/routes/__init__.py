from app.config.routes.routes import *
from app.internal.routes import api, tasks, universities, categories, user

__routes__ = Routes(routers=(api.router, tasks.router, universities.router, categories.router, user.router, ))