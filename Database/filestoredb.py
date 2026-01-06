class FileStoreDB:
    def __init__(self):
        self.data = {}

    async def create_store(self, store_id):
        self.data[store_id] = []

    async def add_file(self, store_id, msg_id):
        self.data[store_id].append(msg_id)

    async def get_files(self, store_id):
        return self.data.get(store_id)

    async def delete_store(self, store_id):
        if store_id in self.data:
            del self.data[store_id]

fsdb = FileStoreDB()

