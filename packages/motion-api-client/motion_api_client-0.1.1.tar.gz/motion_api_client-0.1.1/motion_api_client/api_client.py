import json
from datetime import datetime
from typing import overload, List
import requests
from motion_api_client.models.MotionTask import MotionTask
from motion_api_client.models.create_task_request import CreateTaskRequest, AutoScheduled
from motion_api_client.models.update_task_request import UpdateTaskRequest


class ApiClient:
    def __init__(self, motion_api_key: str, motion_env='DEV'):
        if motion_env == "DEV":
            self.__motion_url__ = "https://stoplight.io/mocks/motion/motion-rest-api/33447"
        else:
            self.__motion_url__ = "https://api.usemotion.com/v1"

        self.api_key = motion_api_key

        self.session = requests.session()
        self.session.headers.update({'X-API-Key': self.api_key, "content-type": "application/json"})

    def list_tasks(self):
        r = self.session.get(self.__motion_url__ + "/tasks")

        if r.status_code != 200:
            resp = r.json()
            raise Exception(f"Error creating task. HTTP code: {r.status_code}.\nError message: {resp['message']} ")

        response_json = r.json()
        task_list = [MotionTask(**t) for t in response_json["tasks"]]
        return task_list

    def delete_task(self, task_id: str):
        r = self.session.delete(self.__motion_url__ + '/tasks/' + task_id)
        if r.status_code != 204:
            resp = r.json()
            raise Exception(f"Error creating task. HTTP code: {r.status_code}.\nError message: {resp['message']} ")
        else:
            print("Deletion success")

    def retrieve_task(self, task_id: str):
        r = self.session.get(self.__motion_url__ + '/tasks/' + task_id)
        if r.status_code != 200:
            resp = r.json()
            raise Exception(f"Error creating task. HTTP code: {r.status_code}.\nError message: {resp['message']} ")
        json_response = r.json()
        task = MotionTask(**json_response)
        return task

    def create_task(self, body: CreateTaskRequest):

        json_body = json.dumps(body.to_dict())
        r = self.session.post(self.__motion_url__ + '/tasks', data=json_body)

        if r.status_code != 201:
            resp = r.json()
            raise Exception(f"Error creating task. HTTP code: {r.status_code}.\nError message: {resp['message']} ")

        return r.json()

    def create_task_from_dict(self, body):
        task_body = CreateTaskRequest(**body)

        json_body = json.dumps(task_body.to_dict())
        r = self.session.post(self.__motion_url__ + '/tasks', data=json_body, headers={'Content-Type': 'application/json'})

        if r.status_code != 201:
            resp = r.json()
            raise Exception(f"Error creating task. HTTP code: {r.status_code}.\nError message: {resp['message']} ")

        resp = r.json()

        return resp

    def update_task(self, task_id: str, body: UpdateTaskRequest):
        json_body = json.dumps(body.to_dict())
        request_path = f'{self.__motion_url__}/tasks/{task_id}'

        r = self.session.patch(request_path, data=json_body)

        if r.status_code != 200:
            resp = r.json()
            raise Exception(f"Error updating task. HTTP code: {r.status_code}\nError message: {resp['message']}")

        resp = r.json()
        return resp

    def get_my_user(self):
        r = self.session.get(self.__motion_url__ + '/users/me')

        if r.status_code != 200:
            resp = r.json()
            raise Exception(f'Error getting user. Http code: {r.status_code}\nError message: {resp["message"]}')
        return r.json()
