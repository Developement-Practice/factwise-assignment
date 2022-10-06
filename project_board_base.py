import os
import json
import psycopg2

class ProjectBoardBase:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
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
                            CREATE TABLE IF NOT EXISTS project_boards (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(64) NOT NULL,
                                description VARCHAR(128) NOT NULL,
                                team_id INTEGER NOT NULL,
                                creation_time TIMESTAMP NOT NULL
                                )
                                ''')

    # create a board

    def create_board(self, request: str):
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """

        try:
            result = ""
            json_request = json.loads(request)

            assert len(json_request['name']) <= 64
            assert len(json_request['description']) <= 128

            self.cursor.execute('''
                            INSERT INTO project_boards (name, description, team_id, creation_time) VALUES (%s, %s, %s, %s) RETURNING id
                            ''',
                                (json_request['name'], json_request['description'], json_request['team_id'],
                                 json_request['creation_time']))

            result = json.dumps({"id": self.cursor.fetchone()[0]})

            return result

        except Exception as e:
            print(e)

    # close a board
    def close_board(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        try:
            result = ""
            json_request = json.loads(request)

            self.cursor.execute('''
                           UPDATE project_boards SET status = %s WHERE id = %s
                           ''',
                                (json_request['status'], json_request['id']))

            result = json.dumps({"id": self.cursor.fetchone()[0]})

            return result
        except Exception as e:
            print(e)

    # add task to board

    def add_task(self, request: str) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<board_name>",
            "description" : "<description>",
            "user_id" : "<team id>"
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        try:
            result = ""
            json_request = json.loads(request)

            assert len(json_request['title']) <= 64
            assert len(json_request['description']) <= 128

            self.cursor.execute('''
                            INSERT INTO tasks (title, description, user_id, creation_time) VALUES (%s, %s, %s, %s) RETURNING id
                            ''',
                                (json_request['title'], json_request['description'], json_request['user_id'],
                                 json_request['creation_time']))

            result = json.dumps({"id": self.cursor.fetchone()[0]})

            return result
        except Exception as e:
            print(e)

    # update the status of a task
    def update_task_status(self, request: str):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        pass

    # list all open boards for a team
    def list_boards(self, request: str) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        try:
            result = ""
            json_request = json.loads(request)

            self.cursor.execute('''
                           SELECT * FROM project_boards WHERE id = %s
                           ''',
                                (json_request['id'],))

            result = json.dumps(self.cursor.fetchone())

            return result
        except Exception as e:
            print(e)

    def export_board(self, request: str) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        try:
            result = ""
            json_request = json.loads(request)

            self.cursor.execute('''
                           SELECT * FROM project_boards WHERE id = %s
                           ''',
                                (json_request['id'],))

            result = json.dumps(self.cursor.fetchone())

            out_file = open("out.txt", "w")
            out_file.write(result)

        except Exception as e:
            print(e)
