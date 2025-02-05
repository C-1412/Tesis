from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from core.erp.models import Area

from crum import get_current_request

from config.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='Area', null=True, blank=True)

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        if self.area:
            item['area'] = {'id': self.area.id, 'name': self.area.name}
        else:
            item['area'] = None
        return item
    

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    group_data = {
                        'id': groups[0].id,
                        'name': groups[0].name
                    }
                    request.session['group'] = group_data
        except:
            pass
