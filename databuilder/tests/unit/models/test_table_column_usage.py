import unittest

from databuilder.models.table_column_usage import ColumnReader, TableColumnUsage
from typing import no_type_check


class TestTableColumnUsage(unittest.TestCase):

    @no_type_check  # mypy is somehow complaining on assignment on expected dict.
    def test_serialize(self):
        # type: () -> None

        col_readers = [ColumnReader(database='db', cluster='gold', schema='scm', table='foo', column='*',
                                    user_email='john@example.com'),
                       ColumnReader(database='db', cluster='gold', schema='scm', table='bar', column='*',
                                    user_email='jane@example.com')]
        table_col_usage = TableColumnUsage(col_readers=col_readers)

        node_row = table_col_usage.next_node()
        actual = []
        while node_row:
            actual.append(node_row)
            node_row = table_col_usage.next_node()

        expected = [{'is_active': True,
                     'LABEL': 'User',
                     'KEY': 'john@example.com',
                     'email': 'john@example.com'},
                    {'is_active': True,
                     'LABEL': 'User',
                     'KEY': 'jane@example.com',
                     'email': 'jane@example.com'}]
        self.assertEqual(expected, actual)

        rel_row = table_col_usage.next_relation()
        actual = []
        while rel_row:
            actual.append(rel_row)
            rel_row = table_col_usage.next_relation()

        expected = [{'read_count:UNQUOTED': 1, 'END_KEY': 'john@example.com', 'START_LABEL': 'Table',
                     'END_LABEL': 'User', 'START_KEY': 'db://gold.scm/foo', 'TYPE': 'READ_BY', 'REVERSE_TYPE': 'READ'},
                    {'read_count:UNQUOTED': 1, 'END_KEY': 'jane@example.com', 'START_LABEL': 'Table',
                     'END_LABEL': 'User', 'START_KEY': 'db://gold.scm/bar', 'TYPE': 'READ_BY', 'REVERSE_TYPE': 'READ'}]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
