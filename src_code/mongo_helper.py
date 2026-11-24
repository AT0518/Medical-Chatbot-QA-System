from pymongo import MongoClient


def _connect():
    
    connection_string = "mongodb+srv://ritiksharmaofficial2_db_user:eXICLjO7zKyh8Gsw@cluster0.ou8fbat.mongodb.net"

    client = MongoClient(connection_string)

    # Test Connection
    client.admin.command("ping")

    print("Connected Successfully!")
    return client

# Database

def _write_to_db(data, database_name = "HospitalDB", collection_name = "patients"):
    
    client = _connect()
    
    db = client[database_name]

    # Collection
    collection = db[collection_name]
    
    result = collection.insert_many(data)
    if result is not None:
        return True
    return False


def _read_from_db(database_name = "HospitalDB", collection_name = "patients"):
    
    records = []
    client = _connect()
    
    db = client[database_name]
    
        # Collection
    collection = db[collection_name]
    
    for doc in collection:
        records.append(doc)
        
    return records    
    

        
        
    

