from scrapy.utils.project import get_project_settings


class RedisPipeline(object):
    __REDIS_SETTING_MAPS__ = {
        'REDIS_HOST': 'host',
        'REDIS_PORT': 'port',
        'REDIS_DB': 'db'
    }

    def __init__(self):
        settings = get_project_settings()
        print(settings)