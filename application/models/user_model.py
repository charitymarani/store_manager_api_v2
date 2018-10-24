'''/models.usermodel.py'''
from werkzeug.security import generate_password_hash, check_password_hash
from .base_model import BaseModel
from ..utils import select_with_condition, select_no_condition


class User(BaseModel):
    '''User class model'''

    def put(self, name, username, email, password, role):
        '''Create a new user account'''
        pw_hash = generate_password_hash(password)
        result = select_with_condition('users', 'username', username)
        # check if username exists
        if "message" not in result:
            return dict(message="Username already exists. Try a different one.", error=409)

        result2 = select_with_condition('users', 'email', email)
        # check if email exists
        if "message" not in result2:
            return dict(message="Email already in use. Try a different one.", error=409)

        query = """INSERT INTO users(name, username, email, password,role)
                 VALUES(%s, %s, %s, %s, %s);"""
        self.cursor.execute(query, (name, username, email, pw_hash, role))
        self.conn.commit()
        # check that user was signed up
        result3 = select_with_condition('users', 'username', username)
        if "message" in result3:
            return dict(message="Failed to signup, try again.", error=404)

        return dict(message="Welcome " + username + "!")

    def verify_password(self, username, password):
        '''verify the password a user enters while logging in'''
        self.cursor.execute(
            "SELECT username, password FROM users WHERE username = (%s);", (username,))
        result = self.cursor.fetchone()

        if not result:

            return dict(message="Username does not exist in our records", error=401)
        verify = check_password_hash(result['password'], password)
        if verify:

            return "True"

        return dict(message="The password you entered is incorrect", error=401)

    def get_all_users(self):
        '''get all users'''
        result = select_no_condition('users', 'user_id')
        return result

    def get_user_by_username(self, username):
        '''get user details by username'''
        result = select_with_condition('users', 'username', username)
        return result
