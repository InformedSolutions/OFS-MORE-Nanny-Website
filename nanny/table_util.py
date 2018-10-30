from .db_gateways import NannyGatewayActions


class Table:
    """
    Table class for generating info required during the rendering of generic-summary-template. This will in turn render
    the summary table for a given task.
    """
    error_summary_title = 'There was a problem'

    def __init__(self, application_id, table_pk=None):
        """
        :attr: row_list: list of Row objects which comprise the table.
        """
        self.row_list = []
        self.title = ''
        self.application_id = application_id
        self.table_pk = table_pk

    def get_errors(self):
        for row in self.row_list:
            api_response = NannyGatewayActions().list('arc-comments', params={'application_id': self.application_id, 'field_name': row.data_name})
            if api_response.status_code == 200 and bool(api_response.record[0]['flagged']):
                row.error = api_response.record[0]['comment']
            else:
                row.error = None

    def get_error_amount(self):
        return sum([1 for row in self.row_list if row.error is not None])

    def add_row(self, row):
        """
        A method to add a row to a tables row list
        :param row: The new row object
        :return:
        """
        self.row_list.append(row)

    def get_row_list(self):
        """
        Standar get method for row list
        :return:
        """
        return self.row_list


class Row:
    """
    Class to contain a specific row rendered in a table on the generic summary template.
    """
    def __init__(self, data_name, row_name, value, back_link, change_link_description, error=None):
        """
        :param data_name: The name of the field as stored in the database
        :param row_name: The name of the field as rendered on the template
        :param value: The value of the field
        :param back_link: The view which, when reversed, redirects to the page where the value is defined
        :param change_link_description: An optional change link textual description value
        :param error: The error associated with the field, empty by default, only populated on table.get_errors
        """
        self.data_name = data_name
        self.row_name = row_name
        self.value = value
        self.back_link = back_link
        self.change_link_description = change_link_description
        self.error = error
