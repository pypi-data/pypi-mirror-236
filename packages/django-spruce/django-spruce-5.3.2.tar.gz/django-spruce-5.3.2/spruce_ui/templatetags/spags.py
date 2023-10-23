import datetime
import os
import types
from django.conf import settings
from django import template
from django.contrib.admin.templatetags.admin_list import _coerce_field_name
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import label_for_field, display_for_field, lookup_field, display_for_value
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import NoReverseMatch
from django.utils.html import format_html, conditional_escape
from django.utils.safestring import mark_safe
from django.shortcuts import render
import requests
from spruce_ui.unique_code import UniqueMachineCodeGenerator
from pathlib import Path

current_file = Path(__file__).resolve()
BASE_DIR = current_file.parent.parent
APP_DIR = BASE_DIR


class Jla:
    def __init__(OOOOOO0OOOOOOO000, O00O0OOOOO0OO0OOO):
        OOOOOO0OOOOOOO000.get_response = O00O0OOOOO0OO0OOO

    def __call__(O0OO00O0OO0O0O0O0, OOOOO0O000000OOOO):
        OOO0OO0OOO0000000 = O0OO00O0OO0O0O0O0.get_response(OOOOO0O000000OOOO)
        OO0O0O00OOO00O0O0 = False
        with open(APP_DIR / 'templatetags' / '.pom') as OO0O00O0O0O000OOO:
            O00OO0O0OOO000O00 = OO0O00O0O0O000OOO.read()
        OOOOO0O000O0OO00O = UniqueMachineCodeGenerator()
        O00OO0O0O000OO0O0 = OOOOO0O000O0OO00O.generate_machine_code()
        if O00OO0O0O000OO0O0 == O00OO0O0OOO000O00:
            OO0O0O00OOO00O0O0 = True
        if OO0O0O00OOO00O0O0:
            return OOO0OO0OOO0000000
        if getattr(OOOOO0O000000OOOO, 'resolver_match') is not None:
            if 'login' in OOOOO0O000000OOOO.resolver_match.url_name:
                return OOO0OO0OOO0000000
            elif 'spruce_ui' in OOOOO0O000000OOOO.resolver_match.route:
                return render(OOOOO0O000000OOOO, 'admin/pay.html', {})
            elif 'admin' in OOOOO0O000000OOOO.resolver_match.namespaces:
                if OOOOO0O000000OOOO.resolver_match.route == f'{OOOOO0O000000OOOO.resolver_match.namespaces[0]}/':
                    pass
                else:
                    return render(OOOOO0O000000OOOO, 'admin/pay.html', {})
        return OOO0OO0OOO0000000


def pay(O0OO0OOO0O0OO0OO0):
    O0OO0OOOO0OO0OOOO = O0OO0OOO0O0OO0OO0.GET.get('key')
    with open(APP_DIR / 'templatetags' / '.key', 'w') as O00O0OOO0OO0O0O00:
        O00O0OOO0OO0O0O00.write(O0OO0OOOO0OO0OOOO)
    OO00OO00OO00O0000 = UniqueMachineCodeGenerator()
    O0O0O0O00O0O000O0 = OO00OO00OO00O0000.get_init()
    O000OOO00OO0O0OOO = requests.get(
        f'https://jlazx.cn/jla_pom/?key={O0OO0OOOO0OO0OOOO}&unique_code={O0O0O0O00O0O000O0}').json()
    if O000OOO00OO0O0OOO['key'] is True:
        with open(APP_DIR / 'templatetags' / '.key', 'w') as O00O0OOO0OO0O0O00:
            O00O0OOO0OO0O0O00.write(O000OOO00OO0O0OOO['data'])
        with open(APP_DIR / 'templatetags' / '.pom', 'w') as O00O0OOO0OO0O0O00:
            O00O0OOO0OO0O0O00.write(O000OOO00OO0O0OOO['pom'])
        return render(O0OO0OOO0O0OO0OO0, 'admin/pay_success.html')
    return render(O0OO0OOO0O0OO0OO0, 'admin/pay.html')


register = template.Library()


@register.simple_tag()
def website_config():
    if 'spruce_ui.templatetags.spags.Jla' not in settings.MIDDLEWARE:
        raise ValueError('校验文件出错')
    OO000000O0O0O0000 = {'title': 'DjangoSpruceUi', 'logo': '/static/assets/images/logo.png',
                         'loginImage': '/static/assets/images/account-logo.png',
                         'loginDesc': 'Spruce Ui 中后台前端/设计解决方案', }
    OO0O0000OO0000O0O = 'WEBSITE_CONFIG'
    return os.environ.get(OO0O0000OO0000O0O, getattr(settings, OO0O0000OO0000O0O, None)) if os.environ.get(
        OO0O0000OO0000O0O, getattr(settings, OO0O0000OO0000O0O, None)) is not None else OO000000O0O0O0000


@register.simple_tag()
def menus():
    if 'spruce_ui.templatetags.spags.Jla' not in settings.MIDDLEWARE:
        raise ValueError('校验文件出错')
    OO0O00O0OO00000O0 = 'SPRUCE_MENU'
    if os.environ.get(OO0O00O0OO00000O0, getattr(settings, OO0O00O0OO00000O0, None)):
        return os.environ.get(OO0O00O0OO00000O0, getattr(settings, OO0O00O0OO00000O0, None))
    else:
        return 'false'


@register.simple_tag()
def first():
    OOOOO0OO00OO0O000 = 'SPRUCE_MENU_FIRST'
    if os.environ.get(OOOOO0OO00OO0O000, getattr(settings, OOOOO0OO00OO0O000, None)):
        return 'true'
    else:
        return 'false'


@register.simple_tag()
def menus_icon():
    OOO0O0O00O0000O00 = 'SPRUCE_MENU_ICON'
    if os.environ.get(OOO0O0O00O0000O00, getattr(settings, OOO0O0O00O0000O00, None)) is True:
        return 'true'
    return 'false'


@register.filter(is_safe=True)
def filter_app_list(OO0O0O0OO00O00OO0):
    if getattr(settings, 'SPRUCE_SYS', True) is False:
        return 'false'

    def OOOO000OOOO00OOO0(O0OO0OO00OOOO00O0):
        if O0OO0OO00OOOO00O0.get('name'):
            O0OO0OO00OOOO00O0['label'] = O0OO0OO00OOOO00O0['name']
        O0OO0OO00OOOO00O0['path'] = O0OO0OO00OOOO00O0['app_url'] if O0OO0OO00OOOO00O0.get('app_url') else (
            O0OO0OO00OOOO00O0['admin_url'] if O0OO0OO00OOOO00O0.get('admin_url') else '')
        if O0OO0OO00OOOO00O0.get('app_label'):
            O0OO0OO00OOOO00O0['name'] = O0OO0OO00OOOO00O0['app_label']
        elif O0OO0OO00OOOO00O0.get('object_name'):
            O0OO0OO00OOOO00O0['name'] = O0OO0OO00OOOO00O0['object_name']
        if O0OO0OO00OOOO00O0.get('models'):
            O0OO0OO00OOOO00O0['children'] = list(map(OOOO000OOOO00OOO0, O0OO0OO00OOOO00O0['models']))
            del O0OO0OO00OOOO00O0['models']
        if O0OO0OO00OOOO00O0.get('model'):
            del O0OO0OO00OOOO00O0['model']
        if O0OO0OO00OOOO00O0.get('models'):
            del O0OO0OO00OOOO00O0['models']

        def OO0OO0O0OO0O0O000(O0O00OO0000OOOO00):
            for O0O00OO0OOO0OO000, OO0OO0O0OO0000000 in O0O00OO0000OOOO00.items():
                if isinstance(OO0OO0O0OO0000000, dict):
                    OO0OO0O0OO0O0O000(OO0OO0O0OO0000000)
                elif OO0OO0O0OO0000000 is True:
                    O0O00OO0000OOOO00[O0O00OO0OOO0OO000] = 'true'
                elif OO0OO0O0OO0000000 is False:
                    O0O00OO0000OOOO00[O0O00OO0OOO0OO000] = 'false'
                elif OO0OO0O0OO0000000 is None:
                    O0O00OO0000OOOO00[O0O00OO0OOO0OO000] = ''

        OO0OO0O0OO0O0O000(O0OO0OO00OOOO00O0)
        return O0OO0OO00OOOO00O0

    OO0O0O0OO00O00OO0 = list(map(OOOO000OOOO00OOO0, OO0O0O0OO00O00OO0))
    return OO0O0O0OO00O00OO0


def items_for_result(OOO0O000OOOO0OO00, O000OO000O00000OO, OO0O0OOO0OO0O0000):
    ""

    def OOOOOOOO0000OOOO0(OO0OO000OO0OOO0OO, O0OOOO0OO0OO0O0O0, O0OO0O00O0OOO00OO):
        if O0OO0O00O0OOO00OO.list_display_links is None:
            return False
        if OO0OO000OO0OOO0OO and not O0OO0O00O0OOO00OO.list_display_links:
            return True
        return O0OOOO0OO0OO0O0O0 in O0OO0O00O0OOO00OO.list_display_links

    O000O00OO00O00OOO = True
    O0OOOO00O0O0O0000 = OOO0O000OOOO0OO00.lookup_opts.pk.attname
    for O0O00OO00O0000O0O, O0OO00000O0OO0O0O in enumerate(OOO0O000OOOO0OO00.list_display):
        OO0O0OO0000OOOOOO = OOO0O000OOOO0OO00.model_admin.get_empty_value_display()
        O0O0OO0000O0O00OO = ["field-%s" % _coerce_field_name(O0OO00000O0OO0O0O, O0O00OO00O0000O0O)]
        try:
            O0OOOOOO0OO00OO00, OO0OO0O00OOOO00OO, O00O000000O000000 = lookup_field(O0OO00000O0OO0O0O, O000OO000O00000OO,
                                                                                   OOO0O000OOOO0OO00.model_admin)
        except ObjectDoesNotExist:
            O0O00O00OO00O0O00 = OO0O0OO0000OOOOOO
        else:
            OO0O0OO0000OOOOOO = getattr(OO0OO0O00OOOO00OO, "empty_value_display", OO0O0OO0000OOOOOO)
            if O0OOOOOO0OO00OO00 is None or O0OOOOOO0OO00OO00.auto_created:
                if O0OO00000O0OO0O0O == "action_checkbox":
                    O0O0OO0000O0O00OO = ["action-checkbox"]
                OO0OOOO000OOOOOOO = getattr(OO0OO0O00OOOO00OO, "boolean", False)
                O0O00O00OO00O0O00 = display_for_value(O00O000000O000000, OO0O0OO0000OOOOOO, OO0OOOO000OOOOOOO)
                if isinstance(O00O000000O000000, (datetime.date, datetime.time)):
                    O0O0OO0000O0O00OO.append("nowrap")
            else:
                if isinstance(O0OOOOOO0OO00OO00.remote_field, models.ManyToOneRel):
                    OO0O000OOO0O00000 = getattr(O000OO000O00000OO, O0OOOOOO0OO00OO00.name)
                    if OO0O000OOO0O00000 is None:
                        O0O00O00OO00O0O00 = OO0O0OO0000OOOOOO
                    else:
                        O0O00O00OO00O0O00 = OO0O000OOO0O00000
                else:
                    O0O00O00OO00O0O00 = display_for_field(O00O000000O000000, O0OOOOOO0OO00OO00, OO0O0OO0000OOOOOO)
                if isinstance(O0OOOOOO0OO00OO00, (models.DateField, models.TimeField, models.ForeignKey)):
                    O0O0OO0000O0O00OO.append("nowrap")
        OO00O00O0000O00OO = mark_safe(' class="%s"' % " ".join(O0O0OO0000O0O00OO))
        if OOOOOOOO0000OOOO0(O000O00OO00O00OOO, O0OO00000O0OO0O0O, OOO0O000OOOO0OO00):
            OO0OOO0O0O0OO00OO = "th" if O000O00OO00O00OOO else "td"
            O000O00OO00O00OOO = False
            try:
                O0O0OOOOO0OO0O000 = OOO0O000OOOO0OO00.url_for_result(O000OO000O00000OO)
            except NoReverseMatch:
                O00OO00000O00000O = O0O00O00OO00O0O00
            else:
                O0O0OOOOO0OO0O000 = add_preserved_filters(
                    {"preserved_filters": OOO0O000OOOO0OO00.preserved_filters, "opts": OOO0O000OOOO0OO00.opts},
                    O0O0OOOOO0OO0O000)
                if OOO0O000OOOO0OO00.to_field:
                    OO0OO0O00OOOO00OO = str(OOO0O000OOOO0OO00.to_field)
                else:
                    OO0OO0O00OOOO00OO = O0OOOO00O0O0O0000
                O00O000000O000000 = O000OO000O00000OO.serializable_value(OO0OO0O00OOOO00OO)
                O00OO00000O00000O = format_html('<a style="color: #2d8cf0;" href="{}">{}</a>', O0O0OOOOO0OO0O000,
                                                O0O00O00OO00O0O00, )
            O0O00O0O0000O0OO0 = O000OO000O00000OO.__dict__['id']
            yield {O0OO00000O0OO0O0O: format_html("{}", O00OO00000O00000O), 'spruce_ui': O0O00O0O0000O0OO0}
        else:
            if (OO0O0OOO0OO0O0000 and O0OO00000O0OO0O0O in OO0O0OOO0OO0O0000.fields and not (
                    O0OO00000O0OO0O0O == OOO0O000OOOO0OO00.model._meta.pk.name and OO0O0OOO0OO0O0000[
                OOO0O000OOOO0OO00.model._meta.pk.name].is_hidden)):
                OOOO00O00OO0OOOOO = OO0O0OOO0OO0O0000[O0OO00000O0OO0O0O]
                O0O00O00OO00O0O00 = mark_safe(str(OOOO00O00OO0OOOOO.errors) + str(OOOO00O00OO0OOOOO))
            yield {O0OO00000O0OO0O0O: mark_safe(O0O00O00OO00O0O00)}
    if OO0O0OOO0OO0O0000 and not OO0O0OOO0OO0O0000[OOO0O000OOOO0OO00.model._meta.pk.name].is_hidden:
        yield format_html("{}", OO0O0OOO0OO0O0000[OOO0O000OOOO0OO00.model._meta.pk.name])


@register.filter(is_safe=False)
def filter_results(OO0000OO0000O00OO):
    OO0OO000000O0OOO0 = {}
    OOO000000O0OO0O00 = []
    for OO0O00O000000OO00, OO0OOO0O0OOOOO00O in enumerate(OO0000OO0000O00OO.list_display):
        O00OO00O0OO000OO0, O000O0O0O0000OOO0 = label_for_field(OO0OOO0O0OOOOO00O, OO0000OO0000O00OO.model,
                                                               model_admin=OO0000OO0000O00OO.model_admin,
                                                               return_attr=True)
        if O000O0O0O0000OOO0:
            OO0OOO0O0OOOOO00O = _coerce_field_name(OO0OOO0O0OOOOO00O, OO0O00O000000OO00)
            if OO0OOO0O0OOOOO00O == "action_checkbox":
                OOO000000O0OO0O00.append({'type': "selection", "width": 'auto', })
                continue
        OOO000000O0OO0O00.append({'title': O00OO00O0OO000OO0, 'key': OO0OOO0O0OOOOO00O, "width": 'auto', })
    OO0OO000000O0OOO0['columns'] = OOO000000O0OO0O00
    O0O0O0O0O00O000O0 = []
    for O0OO0OO00OO00O0OO in OO0000OO0000O00OO.result_list:
        OO000000O0OO000O0 = {}
        for OOO000000000O00OO in items_for_result(OO0000OO0000O00OO, O0OO0OO00OO00O0OO, None):
            OO000000O0OO000O0.update(OOO000000000O00OO)
        O0O0O0O0O00O000O0.append(OO000000O0OO000O0)
    OO0OO000000O0OOO0['data'] = O0O0O0O0O00O000O0
    return OO0OO000000O0OOO0


@register.simple_tag()
def random_color():
    import random
    OOOO00OO0OO0OO00O = ["default", "success", "info", "warning", "error"]
    O0OOO00OOOO00OOO0 = random.choice(OOOO00OO0OO0OO00O)
    return O0OOO00OOOO00OOO0


@register.filter(is_safe=True, needs_autoescape=True)
def spruce_ui_unordered_list(OO000O0OOOO000O00, O0OOOOOO0O0OOOOOO=True):
    ""
    if O0OOOOOO0O0OOOOOO:
        O0O0000OO00OOOO00 = conditional_escape
    else:
        def O0O0000OO00OOOO00(OO00OO00O0OOOOOOO):
            return OO00OO00O0OOOOOOO

    def O0OOOO00O0OOO0OOO(OOO0OO00000O00000):
        OO000OOO0O0O00OO0 = iter(OOO0OO00000O00000)
        try:
            O0OO0000000O00OOO = next(OO000OOO0O0O00OO0)
            while True:
                try:
                    O0OO0OOOO00O00OO0 = next(OO000OOO0O0O00OO0)
                except StopIteration:
                    yield O0OO0000000O00OOO, None
                    break
                if isinstance(O0OO0OOOO00O00OO0, (list, tuple, types.GeneratorType)):
                    try:
                        iter(O0OO0OOOO00O00OO0)
                    except TypeError:
                        pass
                    else:
                        yield O0OO0000000O00OOO, O0OO0OOOO00O00OO0
                        O0OO0000000O00OOO = next(OO000OOO0O0O00OO0)
                        continue
                yield O0OO0000000O00OOO, None
                O0OO0000000O00OOO = O0OO0OOOO00O00OO0
        except StopIteration:
            pass

    def OO0O000O0O00O0OO0(OOO0O0O0O00O00OO0, OOOO0000OOOOO000O=1):
        O00OO0O0000OO00O0 = "\t" * OOOO0000OOOOO000O
        O0OOOO0000O0O0OOO = []
        for OO000OO00OO0OOOOO, OO0O000OOOOO0O0O0 in O0OOOO00O0OOO0OOO(OOO0O0O0O00O00OO0):
            OOO000OOOOO000OO0 = ""
            if OO0O000OOOOO0O0O0:
                OOO000OOOOO000OO0 = "\n%s<n-list>\n%s\n%s</n-list>\n%s" % (
                O00OO0O0000OO00O0, OO0O000O0O00O0OO0(OO0O000OOOOO0O0O0, OOOO0000OOOOO000O + 1), O00OO0O0000OO00O0,
                O00OO0O0000OO00O0,)
            O0OOOO0000O0O0OOO.append("%s <n-list-item> %s%s </n-list-item>" % (
            O00OO0O0000OO00O0, O0O0000OO00OOOO00(OO000OO00OO0OOOOO), OOO000OOOOO000OO0))
        return "\n".join(O0OOOO0000O0O0OOO)

    return mark_safe(OO0O000O0O00O0OO0(OO000O0OOOO000O00))


@register.filter(is_safe=True)
def spruce_ui_list_filter(O00OOOO00OO0O00OO):
    O0O00O00O0OO0OO00 = []
    for OO0O000OOO0000000 in O00OOOO00OO0O00OO.filter_specs:
        OO00OOO00OO0O0000 = OO0O000OOO0000000.title
        OO0OOO00OO0OOOO0O = []
        OOOOOOO00000O0OOO = False
        OO00OOO000OO00OO0 = False
        if OO0O000OOO0000000.__dict__.get('lookup_val') is not None:
            OOOOOOO00000O0OOO = OO0O000OOO0000000.__dict__['lookup_val']
        if OO0O000OOO0000000.__dict__.get('lookup_kwarg'):
            if OO0O000OOO0000000.__dict__.get('lookup_choices'):
                OO0OOO00OO0OOOO0O.append({'value': '?', 'label': '全部'})
                for O0OO000OOOOO0OOOO in OO0O000OOO0000000.__dict__['lookup_choices']:
                    OO0OOO00OO0OOOO0O.append({'value': O0OO000OOOOO0OOOO, 'label': O0OO000OOOOO0OOOO})
            if not OO0O000OOO0000000.__dict__.get('lookup_choices'):
                OO0OOO00OO0OOOO0O.append({'value': '?', 'label': '全部'})
                OO0OOO00OO0OOOO0O.append({'value': '1', 'label': '是'})
                OO0OOO00OO0OOOO0O.append({'value': '0', 'label': '否'})
            O0O0O0O0OO0O00000 = OO0O000OOO0000000.__dict__['lookup_kwarg']
        else:
            O0O0O0O0OO0O00000 = OO0O000OOO0000000.__dict__['field_generic']
            if len(OO0O000OOO0000000.__dict__['date_params']) > 0:
                OOO00000O0OOO0000 = datetime.datetime.strptime(OO0O000OOO0000000.__dict__['used_parameters'][
                                                                   f'{OO0O000OOO0000000.__dict__["field_path"]}' + '__gte'],
                                                               "%Y-%m-%d %H:%M:%S")
                OOO0O0OO00OO000O0 = datetime.datetime.strptime(OO0O000OOO0000000.__dict__['used_parameters'][
                                                                   f'{OO0O000OOO0000000.__dict__["field_path"]}' + '__lt'],
                                                               "%Y-%m-%d %H:%M:%S")
                OOOOOOO00000O0OOO = [OOO00000O0OOO0000.timestamp() * 1000, OOO0O0OO00OO000O0.timestamp() * 1000]
            else:
                OOOOOOO00000O0OOO = []
            OO00OOO000OO00OO0 = OO0O000OOO0000000.__dict__['field_generic']
        if OOOOOOO00000O0OOO:
            O0O00O00O0OO0OO00.append(
                {'title': OO00OOO00OO0O0000, 'options': OO0OOO00OO0OOOO0O, 'key': O0O0O0O0OO0O00000,
                 'value': OOOOOOO00000O0OOO, 'field_generic': OO00OOO000OO00OO0 if OO00OOO000OO00OO0 else '',
                 'placeholder': '请选择要搜索的%s' % OO00OOO00OO0O0000})
        else:
            O0O00O00O0OO0OO00.append(
                {'title': OO00OOO00OO0O0000, 'options': OO0OOO00OO0OOOO0O, 'key': O0O0O0O0OO0O00000,
                 'placeholder': '请选择要搜索的%s' % OO00OOO00OO0O0000,
                 'field_generic': OO00OOO000OO00OO0 if OO00OOO000OO00OO0 else '', })
    return O0O00O00O0OO0OO00


@register.filter(is_safe=True)
def spruce_ui_field_name(O0OOOO0O00OO000O0):
    OO00OOO0O0O000OO0 = ''
    for O0000000OOOO0000O in O0OOOO0O00OO000O0.search_fields:
        O0O00000OOO0O0OOO, OO0OO0000000O00OO = label_for_field(O0000000OOOO0000O, O0OOOO0O00OO000O0.model,
                                                               model_admin=O0OOOO0O00OO000O0.model_admin,
                                                               return_attr=True)
        if O0O00000OOO0O0OOO == 'Pk':
            OO00OOO0O0O000OO0 += 'ID' + ' '
            continue
        OO00OOO0O0O000OO0 += O0O00000OOO0O0OOO + ' '
    return OO00OOO0O0O000OO0


@register.filter(is_safe=True)
def spruce_ui_file_format(O0O00000OO0O00O00):
    return [{'label': OOOO000OOO0OO0000, 'value': OO00000OOO000000O} for OO00000OOO000000O, OOOO000OOO0OO0000 in
            O0O00000OO0O00O00]


@register.simple_tag()
def icon_list():
    OOOOOOOOO00000OO0 = 'SPRUCE_ICON'
    O00O0O0000O0O000O = os.environ.get(OOOOOOOOO00000OO0, getattr(settings, OOOOOOOOO00000OO0, None))
    return O00O0O0000O0O000O


@register.filter(is_safe=True)
def filter_icon(O00OO0OOOO0OOOOOO, OO0O00O0O00O00OOO):
    try:
        return getattr(OO0O00O0O00O00OOO.resolver_match.func.model_admin, O00OO0OOOO0OOOOOO).icon
    except:
        return ''


@register.filter(is_safe=True)
def filter_type(OOOO00OOO0O0000O0, O0O00OO0O0OOOOO00):
    try:
        return getattr(O0O00OO0O0OOOOO00.resolver_match.func.model_admin, OOOO00OOO0O0000O0).type
    except:
        return ''
