from rest_framework.routers import SimpleRouter

from .apps import UsersConfig
from .views import UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = []

urlpatterns += router.urls
