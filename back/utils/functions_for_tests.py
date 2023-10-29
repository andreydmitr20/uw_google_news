""" functions for unit testing """

import json
import logging
from random import randint

import pytest
from rest_framework.test import APIClient


"""
    pytest.ini:
    [pytest]
    DJANGO_SETTINGS_MODULE = gitarista.settings
    python_files = tests.py test_*.py *_tests.py
    log_cli = 1
    log_cli_level = INFO
    log_cli_format = %(message)s
    ; log_cli_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
    ; log_cli_date_format=%Y-%m-%d %H:%M:%S
"""


@pytest.fixture
def client():
    return APIClient()


class Endpoints:
    """ base test endpoint class """

    pytestmark = pytest.mark.django_db

    logger = logging.getLogger(__name__)

    # @staticmethod
    def log(self, a):
        """ log """
        self.logger.info(a)

    def is_equal(self,
                 received,
                 expected,
                 fields_to_skip: list = []) -> bool:
        """ compare two python objects """
        if isinstance(received, list):
            len1 = len(received)
            if not isinstance(expected, list):
                return False
            len2 = len(expected)
            if len1 != len2:
                return False
            if len1 == 1:
                return self.is_equal(received[0],
                                     expected[0],
                                     fields_to_skip)
            if len1 == 0:
                return True
            return False
        elif isinstance(received, dict):
            if not isinstance(expected, dict):
                return False
            count = 0
            count_skipped = 0
            for key, value in received.items():

                if not key in expected.keys():
                    if not key in fields_to_skip:
                        self.log(f'NOT FOUND: {key}')
                        return False
                    self.log(f'skipped: {key}')
                    count_skipped += 1
                else:
                    if expected[key] != value:
                        return False
                count += 1
            if count != len(expected.keys())+count_skipped:
                self.log(
                    f'keys count:\n{received.keys()}\n{expected.keys()}')
                return False
            return True
        return json.dumps(received) == json.dumps(expected)

    def get_pk_field_value(self, model, pk, fieldname):
        """ get_field_value by pk"""
        return getattr(model.objects.get(pk=pk), fieldname)

    def get_fk_field_value(self, model, pk, fk_fieldname, fieldname):
        """ get_field_value by fk"""
        return getattr(
            getattr(model.objects.get(pk=pk), fk_fieldname),
            fieldname
        )

    @staticmethod
    def api_client():
        """ api_client """
        return APIClient

    # def fill_model(self, model):
    #     """ fill model with test_data"""
    #     if not hasattr(self, 'test_data') or self.test_data is None:
    #         self.log(f'There are no test data for model: {model.__name__}')
    #         return
    #     # TODO
    #     # obj.objects.bulk_create([obj(row) for row in test_data])
    #     # obj.save()
    #     for data_dict in self.test_data:
    #         new_row = model.objects.create(**data_dict)
    #         new_row.save()

    # @staticmethod
    def fill(self,
             data_class,
             models: list,
             stop_on_model=None
             ):
        """ fill db by data in order """

        def fill_model(model):
            try:
                for data_dict in data_class.data[model.__name__]:
                    new_data_dict = {}
                    for key, value in data_dict.items():
                        # have to put model instance instead of pk value
                        if key.endswith('_id'):
                            # self.log(f'key {key} val: {value}')
                            field_model = data_class.model_by_fieldname.get(
                                key, None)
                            if not field_model is None:
                                value = field_model.objects.get(pk=value)
                                # self.log(f'key {key} val: {value}')
                        new_data_dict[key] = value
                    new_row = model.objects.create(**new_data_dict)
                    new_row.save()
            except Exception as exc:
                raise Exception(
                    f'Failed to fill with test data model: {model.__name__}') from exc

        if len(models) == 0:
            models = data_class.models_in_order

        model = None

        for model in models:
            fill_model(model)
            if not stop_on_model is None and model.__name__ == stop_on_model.__name__:
                break
        return data_class.data[model.__name__]

    # @staticmethod
    # def get_data_for_model(model):
    #     return DataForTests.data[model.__name__]

    def get(self,
            client,
            api_endpoint,
            status_code=200,
            negative_status_code_test=False):

        self.log(f'GET {api_endpoint}')
        response = client.get(api_endpoint)
        self.log(f'\n{response.data}\n')

        result = response.status_code == status_code

        if negative_status_code_test:
            result = not result
        assert result
        return response

    def post(self,
             client,
             api_endpoint,
             data,
             status_code=201,
             negative_status_code_test=False):

        self.log(f'POST {api_endpoint}')
        self.log(f'{data}')

        response = client.post(api_endpoint,
                               content_type='application/json',
                               data=data)
        self.log(f'\n{response.data}\n')

        result = response.status_code == status_code

        if negative_status_code_test:
            result = not result
        assert result
        return response

    def put(self,
            client,
            api_endpoint,
            data,
            status_code=200,
            negative_status_code_test=False):

        self.log(f'PUT {api_endpoint}')
        self.log(f'{data}')

        response = client.put(api_endpoint,
                              content_type='application/json',
                              data=data)
        self.log(f'\n{response.data}\n')

        result = response.status_code == status_code
        if negative_status_code_test:
            result = not result
        assert result
        return response

    def delete(self,
               client,
               api_endpoint,
               status_code=204,
               negative_status_code_test=False):

        self.log(f'DELETE {api_endpoint}\n')

        response = client.delete(api_endpoint)

        result = response.status_code == status_code
        if negative_status_code_test:
            result = not result
        assert result
        return response

    def get_assert(self,
                   client,
                   api_endpoint,
                   expected_data=None,
                   status_code=200,
                   negative_expected_data_test=False,
                   negative_status_code_test=False,
                   fields_to_skip=[]
                   ):

        response = self.get(client,
                            api_endpoint,
                            status_code=status_code,
                            negative_status_code_test=negative_status_code_test)

        if expected_data is None:
            expected_data = []
        else:
            expected_data = [expected_data]

        log_text = '\nexpected:'
        if negative_expected_data_test:
            log_text = 'not '+log_text

        self.log(f'{log_text} {expected_data}')
        result = self.is_equal(
            response.data,
            expected_data,
            fields_to_skip
        )
        if negative_expected_data_test:
            result = not result
        assert result
        return response


class ListEndpoints(Endpoints):
    """ tests for table with pk_id """
    data_class = None
    endpoint = None
    model = None
    model_pk_field_name = None
    model_search_field_name = None
    model_short_field_name = None
    temp_data = None

    # --------------------

    def test_get_count_bad(self, client):

        test_data = self.fill(self.data_class, [self.model])

        self.get_assert(
            client,

            self.endpoint +
            '0/',

            expected_data={'count': len(test_data)},
            negative_expected_data_test=True)

        self.get_assert(
            client,

            self.endpoint +
            '100000/',
            expected_data=None,
            status_code=400,
            negative_status_code_test=True)

    # ++++++++++++++++++++

    def test_get_count0(self, client):

        self.get_assert(
            client,
            self.endpoint +
            '0/?page=0',

            expected_data={'count': 0})

    def test_get_count(self, client):

        test_data = self.fill(self.data_class, [self.model])

        self.get_assert(
            client,

            self.endpoint +
            '0/?page=0',

            expected_data={'count': len(test_data)})

    def test_get_search(self, client):

        test_data = self.fill(self.data_class, [self.model])

        pk_id = randint(1, len(test_data))

        search_text = (
            test_data[pk_id-1][self.model_search_field_name]
            .replace(' ', '%20')
        )

        self.get_assert(
            client,

            self.endpoint +
            '0/?page_size=1000&search=' +
            search_text,

            expected_data={
                self.model_pk_field_name: pk_id,
                **test_data[pk_id-1]
            }
        )

    def test_get_short(self, client):

        test_data = self.fill(self.data_class, [self.model])

        pk_id = randint(1, len(test_data))

        if self.model_short_field_name is None:
            self.model_short_field_name = self.model_search_field_name

        self.get_assert(
            client,

            self.endpoint +
            str(pk_id) +
            '/?page_size=1000&short=1',

            expected_data={
                self.model_pk_field_name: pk_id,
                self.model_short_field_name:
                test_data[pk_id -
                          1][self.model_short_field_name]
            }
        )

    def test_post(self, client):

        test_data = self.fill(self.data_class, [self.model])

        expected_data = {
            self.model_pk_field_name: len(test_data)+1,
            **self.temp_data
        }

        response = self.post(
            client,
            self.endpoint +
            '0/',
            self.temp_data
        )

        # self.log(f'resp: {response.data}\n exp: {expected_data}\n')
        assert self.is_equal(response.data, expected_data)

        self.get_assert(
            client,

            self.endpoint +
            str(expected_data[self.model_pk_field_name])+'/',

            expected_data
        )

    def test_put(self, client):

        test_data = self.fill(self.data_class, [self.model])

        pk_id = randint(1, len(test_data))
        api_endpoint = self.endpoint + str(pk_id)+'/'
        expected_data = {
            self.model_pk_field_name: pk_id,
            ** test_data[pk_id-1]
        }

        self.get_assert(client, api_endpoint, expected_data)

        response = self.put(client, api_endpoint, self.temp_data)

        expected_data = {
            **expected_data,
            **self.temp_data
        }

        assert self.is_equal(
            response.data,
            expected_data
        )

        self.get_assert(client, api_endpoint, expected_data)

    def test_delete(self, client):

        test_data = self.fill(self.data_class, [self.model])

        pk_id = randint(1, len(test_data))
        api_endpoint = self.endpoint + str(pk_id)+'/'
        expected_data = {
            self.model_pk_field_name: pk_id,
            **test_data[pk_id-1]
        }

        self.get_assert(client, api_endpoint, expected_data)
        self.delete(client, api_endpoint)
        self.get_assert(client, api_endpoint, None)


class CompositeEndpoints(Endpoints):
    """ tests for table with composite pk from foreign keys """

    data_class = None

    endpoint = None
    endpoint_suffix = None
    model = None
    model_main_field_id_name = None
    model_search_field_id_name = None
    model_search_field_name = None
    model_second_field_name = None

    temp_data = None

    # --------------------

    def test_get_count_bad(self, client):

        test_data = self.fill(self.data_class,
                              [],
                              self.model)

        self.get_assert(
            client,

            self.endpoint +
            '0/' +
            self.endpoint_suffix +
            '0/',

            expected_data={'count': len(test_data)},
            negative_expected_data_test=True)

        self.get_assert(
            client,

            self.endpoint +
            '0/' +
            self.endpoint_suffix +
            '100000/',
            expected_data=None,
            status_code=400,
            negative_status_code_test=True)

    # ++++++++++++++++++++

    def test_get_count0(self, client):

        self.get_assert(
            client,
            self.endpoint +
            '0/' +
            self.endpoint_suffix +
            '0/' +
            '?page=0',

            expected_data={'count': 0})

    def test_get_count(self, client):

        test_data = self.fill(self.data_class,
                              [],
                              self.model)
        self.get_assert(
            client,
            self.endpoint +
            '0/' +
            self.endpoint_suffix +
            '0/' +
            '?page=0',

            expected_data={'count': len(test_data)})

    def test_get_search(self, client):

        test_data = self.fill(self.data_class,
                              [],
                              self.model)

        pk_id = randint(1, len(test_data))

        search_field_value = self.get_fk_field_value(
            self.model,
            pk_id,
            self.model_search_field_id_name,
            self.model_search_field_name
        )
        search_text = search_field_value.replace(' ', '%20')

        self.get_assert(
            client,

            self.endpoint +
            '0/' +
            self.endpoint_suffix +
            str(
                self.get_fk_field_value(
                    self.model,
                    pk_id,
                    self.model_search_field_id_name,
                    self.model_search_field_id_name
                )
            ) +
            '/' +
            '?page_size=1000&page=0&search=' +
            search_text,

            expected_data={'count': 0},
            negative_expected_data_test=True
        )

    def test_post(self, client):

        test_data = self.fill(self.data_class,
                              [],
                              self.model)

        pk_id = len(test_data)+1
        api_endpoint = (self.endpoint +
                        str(self.temp_data[self.model_main_field_id_name])+'/' +
                        self.endpoint_suffix +
                        str(self.temp_data[self.model_search_field_id_name])+'/'
                        )

        expected_data = {
            'id': pk_id,
            **self.temp_data
        }

        response = self.post(
            client,
            api_endpoint,
            {}
        )

        self.log(f'resp: {response.data}\n exp: {expected_data}\n')
        assert self.is_equal(response.data, expected_data)

        del expected_data['id']
        expected_data[self.model_second_field_name] = self.get_fk_field_value(
            self.model,
            pk_id,
            self.model_search_field_id_name,
            self.model_search_field_name
        )

        self.get_assert(
            client,
            api_endpoint,
            expected_data
        )

    def test_delete(self, client):

        test_data = self.fill(self.data_class,
                              [],
                              self.model)

        pk_id = randint(1, len(test_data))

        api_endpoint = (self.endpoint +
                        str(test_data[pk_id-1][self.model_main_field_id_name])+'/' +
                        self.endpoint_suffix +
                        str(test_data[pk_id-1]
                            [self.model_search_field_id_name])+'/'
                        )

        expected_data = {
            **test_data[pk_id-1],
            self.model_second_field_name: self.get_fk_field_value(
                self.model,
                pk_id,
                self.model_search_field_id_name,
                self.model_search_field_name
            )
        }

        self.get_assert(client, api_endpoint, expected_data)
        self.delete(client, api_endpoint)
        self.get_assert(client, api_endpoint, None)
