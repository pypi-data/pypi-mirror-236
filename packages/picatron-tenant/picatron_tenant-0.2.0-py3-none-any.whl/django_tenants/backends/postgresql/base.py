from importlib import import_module
from collections.abc import Iterable

from django.conf import settings

from django_tenants import app_settings
from django_tenants.backends.postgresql.schema import RLSDatabaseSchemaEditor

ORIGINAL_BACKEND = getattr(settings, 'ORIGINAL_BACKEND', 'django.db.backends.postgresql')

original_backend = import_module(ORIGINAL_BACKEND + '.base')


class DatabaseWrapper(original_backend.DatabaseWrapper):
    SchemaEditorClass = RLSDatabaseSchemaEditor

    def __init__(self, *args, **kwargs):
        self.main_tenant = None
        self.sub_tenant = None
        self.descendant_tenants = None

        self.tenant = None
        self.descendants = None

        super().__init__(*args, **kwargs)

    def set_tenant(self, tenant):
        self.tenant = tenant

    def set_tenant_descendants(self, descendants):
        if isinstance(descendants, Iterable):
            self.descendants = list(descendants)
        else:
            self.descendants = None

    def set_main_tenant(self, main_tenant):
        self.main_tenant = main_tenant

    def set_sub_tenant(self, sub_tenant):
        self.sub_tenant = sub_tenant

    def set_descendant_tenants(self, tenants):
        # In order to hit the query before the assignment (because of lazy queries) list casting is necessary.
        if isinstance(tenants, Iterable):
            self.descendant_tenants = list(tenants)

    def _cursor(self, name=None):
        cursor = super(DatabaseWrapper, self)._cursor(name=name)  # NOQA

        if cursor.cursor.withhold:
            return cursor
        if name:
            return cursor

        self._update_cursor_for_administration_tenant(cursor)
        self._update_cursor_for_main_tenant(cursor)
        self._update_cursor_for_sub_tenant(cursor)
        self._update_cursor_for_descendant_tenants(cursor)

        return cursor

    def _get_comma_seperated_descendants(self):
        if self.descendant_tenants:
            return ",".join([str(descendant.pk) for descendant in self.descendant_tenants])
        else:
            return None

    def _update_cursor_for_administration_tenant(self, cursor):  # NOQA
        cursor.execute(f'SET picatron.admin_tenant = {app_settings.MAIN_TENANT_ID}')

    def _update_cursor_for_main_tenant(self, cursor):
        tenant_id = self.main_tenant.pk if self.main_tenant else app_settings.MAIN_TENANT_ID
        cursor.execute(f'SET picatron.main_tenant = {tenant_id}')

    def _update_cursor_for_sub_tenant(self, cursor):
        tenant_id = self.sub_tenant.pk if self.sub_tenant else app_settings.MAIN_TENANT_ID
        cursor.execute(f'SET picatron.sub_tenant = {tenant_id}')

    def _update_cursor_for_descendant_tenants(self, cursor):
        descendants = self._get_comma_seperated_descendants()
        if descendants:
            cursor.execute(f'SET picatron.descendant_tenants TO "{descendants}"')
        else:
            cursor.execute(f'SET picatron.descendant_tenants TO DEFAULT')


class FakeTenant:
    """
    We can't import any db model in a backend (apparently?), so this class is used
    for wrapping schema names in a tenant-like structure.
    """
    def __init__(self):
        self.is_main = True
