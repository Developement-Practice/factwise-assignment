import os
import json
import requests
import psycopg2


class UserBase:
    """
    Base interface implementation for API's to manage users.
    """

    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOSTNAME'),
            port=os.getenv('POSTGRES_PORT'),
            user=os.getenv('POSTGRES_USERNAME'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database=os.getenv('POSTGRES_DBNAME')
        )
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(64) NOT NULL UNIQUE,
                                display_name VARCHAR(64) NOT NULL
                                )
                            ''')

    # create a user

    def create_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """

        try:
            result = ""
            json_request = json.loads(request)

            self.cursor.execute('''
                           INSERT INTO users (name, display_name) VALUES (%s, %s) RETURNING id
                           ''',
                                (json_request['name'], json_request['display_name']))

            result = json.dumps({"id": self.cursor.fetchone()[0]})

            return result
        except Exception as e:
            print(e)

    def list_users(self) -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        self.cursor.execute('''
                        SELECT * FROM users
                        ''')

        result = self.cursor.fetchall()

        return json.dumps(result)

    # describe user
    def describe_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        try:
            result = ""
            json_request = json.loads(request)
            self.cursor.execute('''
                          SELECT * FROM users WHERE id = %s
                          ''',
                                (json_request['id'],))

            result = json.dumps(self.cursor.fetchone())

            return result
        except Exception as e:
            print(e)

    # update user

    def update_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """

        try:
            result = ""
            json_request = json.loads(request)

            self.cursor.execute('''
                           UPDATE users SET display_name = %s WHERE id = %s
                           ''',
                                (json_request['display_name'], json_request['id']))

            result = json.dumps({"id": self.cursor.fetchone()[0]})

            return result
        except Exception as e:
            print(e)

    def get_user_teams(self, request: str) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """

        try:
            result = ""
            json_request = json.loads(request)
            self.cursor.execute('''
                          SELECT * FROM users JOIN teams ON users.id = teams.user_id WHERE users.id = %s
                            ''', (json_request['id'],))

            result = json.dumps(self.cursor.fetchone())

            return result
        except Exception as e:
            print(e)
