import pymongo
import pandas as pd
import datetime
import uuid
import os
from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm
import structlog
import motor


logger = structlog.get_logger()

load_dotenv(find_dotenv())


class MongoDBManager:
    def __init__(
        self,
        mongo_db_cluster,
        mongodb_db_name,
        mongo_db_user=None,
        mongo_db_password=None,
        is_async=False,
    ):
        if mongo_db_user is None:
            mongo_db_user = os.environ.get("MONGO_DB_USER")

        if mongo_db_password is None:
            mongo_db_password = os.environ.get("MONGO_DB_PASSWORD")

        if not mongo_db_user and not mongo_db_password:
            raise ValueError("MongoDB user and password are not set")

        self.uri = f"mongodb+srv://{mongo_db_user}:{mongo_db_password}@{mongo_db_cluster}/{mongodb_db_name}?retryWrites=true&w=majority"
        self.mongodb_db_name = mongodb_db_name
        self.mongodb_collection_name = None

        self.client = (
            self.get_client() if not is_async else self.get_async_client()
        )

    def __version__(self):
        return "1.7.0"

    def get_client(self) -> tuple((pymongo.MongoClient, str)):
        """
        Get client to MongoDB
        """
        try:
            client = pymongo.MongoClient(
                self.uri,
            )
            return client
        except Exception as e:
            structlog.contextvars.bind_contextvars(function_name="get_client")
            logger.info(f"Unable to connect to the server - Error: {e}")

    def get_async_client(self) -> tuple((pymongo.MongoClient, str)):
        """
        Get async client to MongoDB
        """
        try:
            client = pymongo.MongoClient(
                self.uri,
            )
            client = motor.motor_asyncio.AsyncIOMotorClient(self.uri)
            return client
        except Exception as e:
            structlog.contextvars.bind_contextvars(
                function_name="get_async_client"
            )
            logger.info(f"Unable to connect to the server - Error: {e}")

    def set_collection_name(self, mongodb_collection_name: str):
        """
        Set collection to MongoDB database
        """
        self.mongodb_collection_name = mongodb_collection_name

    def get_collection_name(self) -> str:
        """
        Get collection name from MongoDB database
        """
        if self.mongodb_collection_name is None:
            raise ValueError("Collection name is not set")
        else:
            return self.mongodb_collection_name

    def get_collection(self) -> pymongo.collection.Collection:
        """
        Get collection from MongoDB database and collection specified in the constructor of the class MongoDB
        """
        self.client = self.get_client()
        if self.mongodb_collection_name is None:
            raise ValueError("Collection name is not set")
        else:
            return self.client.get_database(
                self.mongodb_db_name
            ).get_collection(self.mongodb_collection_name)

    def get_uri(self) -> str:
        """
        Get MongoDB URI
        """
        return self.uri

    def get_db_name(self):
        """
        Get MongoDB database name
        """
        return self.mongodb_db_name

    def get_collection_name(self) -> str:
        """
        Get MongoDB collection name
        """
        if self.mongodb_collection_name is None:
            raise ValueError("Collection name is not set")
        else:
            return self.mongodb_collection_name

    def insert_document_in_collection(self, item: dict):
        """
        Insert content to MongoDB database and collection specified in the constructor of the class MongoDB

        Parameters
        ----------
        item: dict

        Returns
        -------
        None

        Actions
        -------
        Insert content to MongoDB database and collection specified in the constructor of the class MongoDB
        """
        collection = self.get_collection()
        collection_name = self.get_collection_name()
        item_id = f"{collection_name.lower()}-{str(uuid.uuid4())}-{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

        if not "date" in item.keys():
            item["date"] = datetime.datetime.now()

        item[f"{collection_name}_id"] = item_id

        collection.insert_one(item)

    def insert_many_document_in_collection(self, items: list):
        """
        Insert document to MongoDB database and collection specified in the constructor of the class MongoDB

        Parameters
        ----------
        items: list

        Returns
        -------
        None

        Actions
        -------
        Insert document to MongoDB database and collection specified in the constructor of the class MongoDB
        """
        collection = self.get_collection()
        collection_name = self.get_collection_name()
        items_id = [
            f"{collection_name.lower()}-{str(uuid.uuid4())}-{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
            for item in items
        ]

        logger.info(
            f"Add to {len(items)} items in {collection_name} id & date."
        )

        for item, item_id in tqdm(zip(items, items_id)):
            if not "date" in item.keys():
                item["date"] = datetime.datetime.now()

            item[f"{collection_name}_id"] = item_id

        collection.insert_many(items)
        logger.info(f"Insert {len(items)} items in {collection_name}.")

    def update_document_in_collection(
        self, item: dict, collection_id: str, collection_id_name: str = None
    ):
        """
        Update document in MongoDB database and collection specified in the constructor of the class MongoDB

        Parameters
        ----------
        collection_id: str
        item: dict

        Returns
        -------
        None
        """
        collection_name = self.get_collection_name()
        collection = self.get_collection()
        item["update_date"] = datetime.datetime.now()
        collection.update_one(
            {
                collection_id_name
                if collection_id_name
                else f"{collection_name.lower()}_id": collection_id
            },
            {"$set": item},
            upsert=True,
        )

    def update_many_documents_in_collection(
        self, items: list, collection_id_name: str = None
    ):
        """
        Update document in MongoDB database and collection specified in the constructor of the class MongoDB

        Parameters
        ----------
        collection_id: str
        item: dict

        Returns
        -------
        None
        """
        collection_name = self.get_collection_name()
        collection = self.get_collection()
        operations = []

        for item in tqdm(items):
            item["update_date"] = datetime.datetime.now()
            filter_query = {
                collection_id_name
                if collection_id_name
                else f"{collection_name.lower()}_id": item[collection_id_name]
                if collection_id_name
                else item[f"{collection_name.lower()}_id"]
            }
            update_operation = pymongo.UpdateOne(
                filter_query, {"$set": item}, upsert=True
            )
            operations.append(update_operation)

        logger.info(
            f"Updating {len(operations)} items in {collection_name}..."
        )

        collection.bulk_write(operations)

        logger.info(
            f"Updated {len(operations)} items in {collection_name} in ."
        )

    def get_all_documents_from_collection(
        self, mongodb_collection_name: str = None
    ) -> list:
        """
        Get documents from MongoDB database and collection specified in the constructor of the class MongoDB

        Parameters
        ----------
        mongodb_collection_name: str

        Returns
        -------
        list

        Actions
        -------
        Get documents from MongoDB database and collection specified in the constructor of the class MongoDB
        """
        if mongodb_collection_name is not None:
            self.set_collection_name(
                mongodb_collection_name=mongodb_collection_name
            )

        collection = self.get_collection()
        return list(collection.find({}))

    def get_distinct_documents_from_collection(
        self, mongodb_collection_name: str = None, field: str = None
    ) -> list:
        """
        Get distinct documents based on field from MongoDB database and collection specified in the constructor of the class MongoDB

        Parameters
        ----------
        mongodb_collection_name: str
        field: str

        Returns
        -------
        list

        Actions
        -------
        Get distinct documents from MongoDB database and collection specified in the constructor of the class MongoDB
        """
        if mongodb_collection_name is not None:
            self.set_collection_name(
                mongodb_collection_name=mongodb_collection_name
            )

        data = self.get_all_documents_from_collection()
        df = pd.DataFrame(data)
        df = df.drop_duplicates(subset=[field])
        return [row.to_dict() for i, row in df.iterrows()]

    def delete_content_in_collection(self, collection_id: str):
        """
        Delete content in MongoDB database and collection specified in the constructor of the class MongoDB

        Parameters
        ----------
        collection_id: str

        Returns
        -------
        None

        Actions
        -------
        Delete content in MongoDB database and collection specified in the constructor of the class MongoDB
        """
        collection_name = self.get_collection_name()
        collection = self.get_collection()
        collection.delete_one({f"{collection_name.lower()}_id": collection_id})

    def delete_all_documents_from_collection(self):
        """
        Delete all documents from MongoDB database and collection specified in the constructor of the class MongoDB

        Parameters
        ----------
        None

        Returns
        -------
        None

        Actions
        -------
        Delete all documents from MongoDB database and collection specified in the constructor of the class MongoDB
        """
        collection = self.get_collection()
        collection.delete_many({})
