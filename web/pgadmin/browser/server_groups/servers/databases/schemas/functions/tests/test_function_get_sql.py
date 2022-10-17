##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2022, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

import json
import uuid
from unittest.mock import patch

from pgadmin.browser.server_groups.servers.databases.tests import utils as \
    database_utils
from pgadmin.utils.route import BaseTestGenerator
from regression.python_test_utils import test_utils as utils
from . import utils as funcs_utils
from .. import FunctionView


class FunctionSqlTestCase(BaseTestGenerator):
    """ This class for function SQL """
    scenarios = [
        (
            'Fetch Function SQL',
            dict(
                url='/browser/function/sql/',
                is_positive_test=True,
                mocking_required=False,
                mock_data={},
                expected_data={
                    "status_code": 200
                }
            ),
        ),
        (
            'Fetch Function SQL fail',
            dict(
                url='/browser/function/sql/',
                is_positive_test=False,
                mocking_required=True,
                mock_data={
                    "function_name": 'pgadmin.utils.driver.psycopg2.'
                                     'connection.Connection.execute_2darray',
                    "return_value": "(False, 'Mocked Internal Server Error "
                                    "while SQL for functions.')"
                },
                expected_data={
                    "status_code": 500
                }
            ),
        )
    ]

    def sql(self, func_id):
        return self.tester.get(
            self.url
            + str(utils.SERVER_GROUP)
            + '/'
            + str(self.server_id)
            + '/'
            + str(self.db_id)
            + '/'
            + str(self.schema_id)
            + '/'
            + str(func_id),
            content_type='html/json',
        )

    def runTest(self):
        """ This function will get function nodes under schema. """
        super(FunctionSqlTestCase, self).runTest()
        self = funcs_utils.set_up(self)
        func_name = f"test_function_delete_{str(uuid.uuid4())[1:8]}"
        function_info = funcs_utils.create_function(
            self.server, self.db_name, self.schema_name, func_name)

        func_id = function_info[0]

        if self.is_positive_test:
            response = self.sql(func_id)
        else:
            with patch(self.mock_data["function_name"],
                       return_value=eval(self.mock_data["return_value"])):
                response = self.sql(func_id)

        self.assertEqual(response.status_code,
                         self.expected_data['status_code'])
        # Disconnect the database
        database_utils.disconnect_database(self, self.server_id, self.db_id)
