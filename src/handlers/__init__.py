from .basic import basic_router
from .admin import admin_router
from .add_users import add_router
from .delete_users import delete_router

admin_router.include_routers(add_router, delete_router)
routers = (basic_router, admin_router)
