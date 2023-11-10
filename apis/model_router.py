from .models import SiteConfig

class MyDBRouter(object):

    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        if model == SiteConfig:
            return 'site_configs'
        return None

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        if model == SiteConfig:
            return 'site_configs'
        return None