from ..simplified.exceptions import PermissionDenied
from ..simplified.simplified_api import simplified_api
import models


@simplified_api
class StatConfig(object):
    class Meta:
        model = models.StatConfig
        resultfields = ['id', 'name', 'period__id', 'user__id']
        searchfields = ['name']
        methods = ['create', 'read_model', 'read', 'update', 'delete', 'search']

    @classmethod
    def create_searchqryset(cls, user, **kwargs):
        qryset = models.StatConfig.objects.filter(user=user)
        return qryset

    @classmethod
    def write_authorize(cls, user, obj):
        if not obj.user == user:
            raise PermissionDenied()

    @classmethod
    def read_authorize(cls, user, obj):
        if not obj.user == user:
            raise PermissionDenied()
