'''/models/blacklist_model.py'''
from .base_model import BaseModel


class RevokedTokens(BaseModel):
    '''class representing token blacklist model'''

    def add_to_blacklist(self, json_token_identifier):
        '''add token to blacklist'''
        query = "INSERT INTO blacklist (json_token_identifier) VALUES (%s);"
        self.cursor.execute(query, (json_token_identifier,))
        self.conn.commit()

    def is_jti_blacklisted(self, json_token_identifier):
        '''check if token is in blacklist'''
        self.cursor.execute(
            "select * from blacklist where json_token_identifier = (%s);", (json_token_identifier,))
        result = bool(self.cursor.fetchone())

        return result
