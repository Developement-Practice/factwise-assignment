import json
import os

import psycopg2


class TeamBase:
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
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
                            CREATE TABLE IF NOT EXISTS teams (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(64) NOT NULL UNIQUE,
                                description VARCHAR(256) NOT NULL,
                                creation_time TIMESTAMP NOT NULL DEFAULT NOW(),
                                admin VARCHAR(64) NOT NULL
                                )
                            ''')

    # create a team

    def create_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """

        try:
            result = ""
            json_request = json.loads(request)

            assert len(json_request['name']) <= 64
            assert len(json_request['description']) <= 128

            self.cursor.execute('''
                          INSERT INTO teams (name, description, admin) VALUES (%s, %s, %s) RETURNING id
                          ''',
                                (json_request['name'], json_request['description'], json_request['admin']))

            result = json.dumps({"id": self.cursor.fetchone()[0]})

            return result
        except Exception as e:
            print(e)

    # list all teams
    def list_teams(self) -> str:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        try:
            result = ""
            self.cursor.execute('''
                          SELECT * FROM teams
                          ''')

            result = json.dumps(self.cursor.fetchall())

            return result
        except Exception as e:
            print(e)

    # describe team
    def describe_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        try:
            result = ""
            json_request = json.loads(request)
            self.cursor.execute('''
                          SELECT * FROM teams WHERE id = %s
                          ''',
                                (json_request['id'],))

            result = json.dumps(self.cursor.fetchone())

            return result
        except Exception as e:
            print(e)

    # update team
    def update_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        try:
            result = ""
            json_request = json.loads(request)

            assert len(json_request['team']['name']) <= 64
            assert len(json_request['team']['description']) <= 128

            self.cursor.execute('''
                           UPDATE teams SET description = %s WHERE id = %s
                           ''',
                                (json_request['description'], json_request['id']))

            result = json.dumps({"id": self.cursor.fetchone()[0]})

            return result
        except Exception as e:
            print(e)

    # add users to team
    def add_users_to_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """

        try:
            result = ""
            json_request = json.loads(request)

            assert len(json_request['users']) <= 50

            self.cursor.execute('''
                           UPDATE teams SET users = %s WHERE id = %s
                           ''',
                                (json_request['users'], json_request['id']))

            result = json.dumps({"id": self.cursor.fetchone()[0]})

            return result
        except Exception as e:
            print(e)

    # add users to team
    def remove_users_from_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        try:
            result = ""
            json_request = json.loads(request)

            assert len(json_request['users']) <= 50

            self.cursor.execute('''
                           UPDATE teams SET users = %s WHERE id = %s
                           ''',
                                (json_request['users'], json_request['id']))

            result = json.dumps({"id": self.cursor.fetchone()[0]})

            return result
        except Exception as e:
            print(e)

    # list users of a team
    def list_team_users(self, request: str):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
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
