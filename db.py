import os
import sys
import uuid

import pymongo
from pymongo.results import InsertOneResult


class Mongo:
    def __init__(self):
        client = pymongo.MongoClient(
            host=["mongo_service:27017"],
            serverSelectionTimeoutMS=3000,  # 3 second timeout
            username=os.environ["USER"],
            password=os.environ["PASSWORD"],
            uuidRepresentation="standard"
        )

        # todo: delete for prod
        client.drop_database('zowt-db')

        # example db input
        mongo_db = client["zowt-db"]
        self.users = mongo_db["users"]
        self.topics = mongo_db["topics"]
        self.comments = mongo_db["comments"]

        user1 = self.add_user("iwijn")
        user2 = self.add_user("klaas")
        topic1 = self.add_topic("belastingen")
        topic2 = self.add_topic("twitter")
        comment1 = self.add_comment(topic1["_id"], user1["_id"], "belastingen bad weee")

    def get_users(self) -> [dict]:
        return [user for user in self.users.find()]

    def get_topics(self) -> [dict]:
        return [topic for topic in self.topics.find()]

    def get_comments(self, topic_id):
        return [comment for comment in self.comments.find() if f"{comment['topic_id']}" == f"{topic_id}"]

    def get_topic(self, topic_id) -> [dict]:
        return self.topics.find_one({"_id": f"{topic_id}"})

    def get_user(self, user_id) -> [dict]:
        return self.users.find_one({"_id": f"{user_id}"})

    def add_user(self, name) -> dict:
        _id = self.users.insert_one({
            "_id": f"{uuid.uuid4()}",
            "name": name
        }).inserted_id
        return self.users.find_one({"_id": f"{_id}"})

    def add_topic(self, name) -> dict:
        _id = self.topics.insert_one({
            "_id": f"{uuid.uuid4()}",
            "name": name
        }).inserted_id
        return self.topics.find_one({"_id": f"{_id}"})

    def add_comment(self, topic_id, user_id, content) -> dict:
        _id = self.comments.insert_one({
            "_id": f"{uuid.uuid4()}",
            "user_id": f"{user_id}",
            "topic_id": f"{topic_id}",
            "content": content
        }).inserted_id
        return self.comments.find_one({"_id": f"{_id}"})
