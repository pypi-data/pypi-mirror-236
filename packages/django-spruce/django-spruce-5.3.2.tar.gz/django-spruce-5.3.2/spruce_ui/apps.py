from django.apps import AppConfig


class SpruceUiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spruce_ui'

    def ready(OO0O0O00000000O00):
        from spruce_ui.views import custom_404_view, custom_403_view, custom_500_view
        from django.conf import urls
        urls.handler404 = custom_404_view
        urls.handler403 = custom_403_view
        urls.handler500 = custom_500_view
        try:
            import django
            from django.conf import settings
            O0OOOO000O000OO00 = django.get_version()
            if int(O0OOOO000O000OO00.split('.')[0]) >= 3:
                for OOO00O0O0O00O00O0, OOOO0O0000O0000O0 in enumerate(settings.MIDDLEWARE):
                    if OOOO0O0000O0000O0 == 'django.middleware.clickjacking.XFrameOptionsMiddleware':
                        settings.MIDDLEWARE.pop(OOO00O0O0O00O00O0)
            settings.MIDDLEWARE.append('spruce_ui.templatetags.spags.Jla')
        except Exception as O00OOO0OOO0O000O0:
            raise O00OOO0OOO0O000O0
