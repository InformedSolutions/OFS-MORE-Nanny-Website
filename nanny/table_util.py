from .db_gateways import NannyGatewayActions


class Table:
    """
    Table class for generating info required during the rendering of generic-summary-template. This will in turn render
    the summary table for a given task.
    """
    error_summary_title = 'There was a problem'

    def get_errors(self):
        for row in self.row_list:
            arc_comments_response = NannyGatewayActions().list('arc-comments',
                                                               params={'application_id': self.application_id,
                                                                       'field_name': row.data_name})
            if arc_comments_response.status_code == 200:
                # Handler dispatch for different relation types.
                if self.__response_is_many_to_one(arc_comments_response.record):
                    row.error = self.__get_errors_many_to_one_handler(arc_comments_response, row)

                else:
                    row.error = self.__get_errors_one_to_one_handler(arc_comments_response)

    @staticmethod
    def __response_is_many_to_one(response_record):
        return len(response_record) > 1

    @staticmethod
    def __get_errors_one_to_one_handler(arc_comments_response):
        """
        Handler for many-to-one arc comment relations.
        :param arc_comments_response: A nanny_gateway response for ArcComments.
            Assumed that the response.record contains a single dictionary.
        :return: An error string, or None.
        """
        return arc_comments_response.record[0]['comment'] if bool(arc_comments_response.record[0]['flagged']) else None

    @staticmethod
    def __get_errors_many_to_one_handler(arc_comments_response, row):
        """
        Handler for many-to-one arc comment relations.
        :param arc_comments_response: A nanny_gateway response for ArcComments.
            Assumed that the response.record contains multiple dictionaries.
        :param row: The current table row.
        :return: An error string, or None.
        """
        if row.row_pk in [None, '']:
            raise ValueError('row_pk must not be left blank when a many_to_one error relation exists.')

        arc_comments_record_list = arc_comments_response.record

        for ac_record in arc_comments_record_list:
            endpoint = ac_record['endpoint_name']

            endpoint_pk = Table.__get_endpoint_pk(endpoint)
            endpoint_response = NannyGatewayActions().read(endpoint, params={endpoint_pk: row.row_pk})

            if endpoint_response.status_code == 200:
                if ac_record.get('table_pk') == row.row_pk:
                    if bool(ac_record['flagged']):
                        return ac_record['comment']
                    else:
                        return None

        # If this return is reached, no arc_comment was found for this row.
        return None

    @staticmethod
    def __get_endpoint_pk(endpoint):
        nanny_actions = NannyGatewayActions()
        return nanny_actions.get_endpoint_pk(endpoint)

    def get_error_amount(self):
        return sum([1 for row in self.row_list if row.error is not None])

    def __init__(self, application_id, table_pk=None):
        """
        :attr: row_list: list of Row objects which comprise the table.
        """
        self.row_list = []
        self.title = ''
        self.application_id = application_id
        self.table_pk = table_pk


class Row:
    """
    Class to contain a specific row rendered in a table on the generic summary template.
    """

    def __init__(self, data_name, row_name, value, back_link, change_link_description, error=None, row_pk=None):
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
        self.row_pk = row_pk
