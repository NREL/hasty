# from django.conf import settings
# import pytest

# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     pass


# @pytest.fixture(scope='session')
# def django_db_modify_db_settings(request):
#     settings.DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': 'test.db'
#         }
#     }
