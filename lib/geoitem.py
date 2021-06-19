from abc import ABC, abstractmethod


class AbstractGeoItem(ABC):

    @abstractmethod
    def get_geo_item(self, row, x, y):
        pass


class GoogleGeoItem(AbstractGeoItem):

    def __init__(self, form_link):
        self.form_link = form_link

    def get_geo_item(self, row, x, y):
        data = {
            'x': x,
            'y': y,
            'name': row.obj_name,
            'reg_id': row.reg_id,
            'type': row.type,
            'date': row.date,
            'address': row.address,
            'form_link': f'{self.form_link}{row.reg_id}',
            'state': '-',
            'comment': ''
        }
        return data


class YandexGeoItem(AbstractGeoItem):
    def __init__(self, form_link):
        self.form_link = form_link

    @staticmethod
    def _get_default_description(row):
        return f'<strong>{row.reg_id}</strong></br>{row.address}</br>Тип: {row.type}</br>Дата: {row.date or ""}'

    def _get_extended_description(self, row):
        description = self._get_default_description(row)
        url = f'{self.form_link}{row.reg_id}'
        href = f'<a href="{url}">Заполнить анкету</a>'
        return f'{description}</br>{href}'

    def get_geo_item(self, row, x, y):
        description = self._get_extended_description(row)
        data = {
            'x': x,
            'y': y,
            'description': description,
            'name': row.obj_name,
            'reg_id': row.id
        }
        return data


def geo_item_factory(geo_service, form_link):
    if geo_service == 'google':
        return GoogleGeoItem(form_link)
    elif geo_service == 'yandex':
        return YandexGeoItem(form_link)
    return GoogleGeoItem(form_link)
