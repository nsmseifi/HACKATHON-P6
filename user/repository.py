from repository_model import BasicRepository



class UserRepository(BasicRepository):
    def get_all_by_person(self, person_id):
        query_data = dict(filter=dict(person_id=person_id))
        result = self.model.mongoquery(
            self.db_session.query(self.model)).query(
            **query_data).end().all()
        return result
    def get_by_username(self, username):
        query_data = dict(filter=dict(username=username))
        result = self.model.mongoquery(
            self.db_session.query(self.model)).query(
            **query_data).end().first()
        return result



class PersonRepository(BasicRepository):
    pass


