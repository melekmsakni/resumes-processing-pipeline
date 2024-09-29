from .connection import get_db

# Fetch all documents from a collection
def fetch_all(collection_name, filters=None):
    db = get_db()
    collection = db[collection_name]
    if filters:
        return list(collection.find(filters))
    return list(collection.find({}))

# Fetch a single document based on a filter
def fetch_one(collection_name, filters):
    db = get_db()
    collection = db[collection_name]
    return collection.find_one(filters)

# Insert new document
def insert_document(collection_name, data):
    db = get_db()
    collection = db[collection_name]
    return collection.insert_one(data)

# Update document
def update_document(collection_name, filters, update_values):
    db = get_db()
    collection = db[collection_name]
    return collection.update_one(filters, {'$set': update_values})


# Delete a document based on a filter
def delete_document(collection_name, filters):
    db = get_db()
    collection = db[collection_name]
    return collection.delete_one(filters)

