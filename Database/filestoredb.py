# Database/filestoredb.py

class FileStoreDB:
    def __init__(self):
        # store_id : [database_channel_message_ids]
        self.data = {}

    async def create_store(self, store_id: str):
        self.data[store_id] = []

    async def add_file(self, store_id: str, db_msg_id: int):
        if store_id not in self.data:
            self.data[store_id] = []
        self.data[store_id].append(db_msg_id)

    async def get_files(self, store_id: str):
        return self.data.get(store_id, [])

    async def delete_store(self, store_id: str):
        if store_id in self.data:
            del self.data[store_id]

    async def store_exists(self, store_id: str) -> bool:
        return store_id in self.data


fsdb = FileStoreDB()
