from demands import JSONServiceClient


class ContinuousLearningApiClient(object):
    """
    Client for Continuous Learning Service.

    :param str auth_token:

        An access token.

    :param str api_url:
        The full URL of the API.

    """

    def __init__(self, auth_token, api_url, session=None):
        headers = {'Authorization': 'Token ' + auth_token}
        if session is None:
            session = JSONServiceClient(url=api_url,
                                        headers=headers)
        self.session = session

    def get_trackers(self, params=None):
        return self.session.get('/tracker/', params=params)

    def get_tracker(self, item):
        return self.session.get('/tracker/%s/' % item)

    def get_answers(self, params=None):
        return self.session.get('/answer/', params=params)

    def get_quizzes(self, params=None):
        return self.session.get('/quiz/', params=params)

    def get_quiz(self, item):
        return self.session.get('/quiz/%s/' % item)

    def create_quiz(self, quiz):
        return self.session.post('/quiz/', data=quiz)

    def update_quiz(self, quiz_id, quiz):
        return self.session.put('/quiz/%s/' % quiz_id, data=quiz)

    def get_questions(self, params=None):
        return self.session.get('/question/', params=params)

    def get_question(self, item):
        return self.session.get('/question/%s/' % item)

    def create_question(self, question):
        return self.session.post('/question/', data=question)

    def update_question(self, question_id, question):
        return self.session.put('/question/%s/' % question_id, data=question)


class IdentityStoreApiClient(object):
    """
    Client for Identity Store Service.

    :param str auth_token:

        An access token.

    :param str api_url:
        The full URL of the API.

    """

    def __init__(self, auth_token, api_url, session=None):
        headers = {'Authorization': 'Token ' + auth_token}
        if session is None:
            session = JSONServiceClient(url=api_url,
                                        headers=headers)
        self.session = session

    def get_identities(self, params=None):
        return self.session.get('/identities/', params=params)

    def get_identity(self, item):
        return self.session.get('/identities/%s/' % item)

    def search_identities(self, field, value):
        # this is used for searching 'details' field to avoid DRF lacks
        # use "details__preferred_language" for example field
        params = {field: value}
        return self.session.get('/identities/search/', params=params)

    def get_identity_by_address(self, address_type, address_value):
        params = {"details__addresses__%s" % address_type: address_value}
        return self.session.get('/identities/search/', params=params)
