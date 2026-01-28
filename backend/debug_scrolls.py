from main import collection

scrolls = collection.get()
for doc, id_, meta in zip(scrolls["documents"], scrolls["ids"], scrolls["metadatas"]):
    print(f"ID: {id_}")
    print(f"Text: {doc}")
    print(f"Author: {meta.get('author', 'Unknown')}")
    print(f"Timestamp: {meta.get('timestamp', 'Unknown')}")
    print("------")
