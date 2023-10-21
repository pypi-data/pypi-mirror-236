from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union

MongoDBIndex = Union[str, Tuple[Tuple[str, int], ...]]


class CollectionSpec(TypedDict):
    NAME: str
    INDEXES: List[Tuple[MongoDBIndex, Dict]]
    VALIDATOR: Optional[Dict[str, Any]]
    """A Json schema document applied by Mongo to validate documents.

    Validation is applied on document creation and update. Failing documents are
    rejected and the operation is not executed.

    The intention of this validation is to do basic checks that can save us from
    damaging the data in situation like:
    - running a buggy migration script
    - some service code change that has a weird bug only exercised at larger
      data sizes, and not in tests
    - manual mistakes during DB administrative tasks

    Examples of validation we may want to do:
    - the types of most fields
    - flag fields as required
    - flag numbers that must be positive
    - non empty strings

    Maintaining this validations updated has some costs, so it's not very
    useful to add every possible validation here. Examples of validation that
    would be better left out:
    - email field has an '@' sign
    - session_id has certain format
    """


class IcechunkSpec(TypedDict):
    VERSION: int
    METADATA_COLLECTION_NAME: str
    METADATA_DOCUMENT_ID: str
    CHUNKSTORE_KEY: str
    COLLECTIONS: Dict[str, CollectionSpec]


ICECHUNK_SPEC: IcechunkSpec = {
    "VERSION": 2,
    "METADATA_COLLECTION_NAME": "icechunk_metadata",
    "METADATA_DOCUMENT_ID": "root",
    "CHUNKSTORE_KEY": "chunkstore_uri",
    "COLLECTIONS": {
        "COMMITS": {
            "NAME": "commits",
            "INDEXES": [],
            "VALIDATOR": None,
        },
        "metadata": {
            "NAME": "metadata",
            "INDEXES": [
                ("session_id", {}),
                ((("node_id", 1), ("session_id", 1), ("coord", 1), ("deleted", 1), ("_id", -1)), {}),
            ],
            "VALIDATOR": None,
        },
        "chunks": {
            "NAME": "chunk_manifest",
            "INDEXES": [
                ("session_id", {}),
                ((("coord", 1), ("session_id", 1)), {}),
                ((("node_id", 1), ("session_id", 1), ("coord", 1), ("deleted", 1), ("_id", -1)), {}),
            ],
            "VALIDATOR": None,
        },
        "nodes": {
            "NAME": "nodes",
            "INDEXES": [
                ((("session_id", 1), ("path", 1), ("_id", -1)), {}),
                ((("session_id", 1), ("node_id", 1), ("_id", -1)), {}),
                ((("session_id", 1), ("path", 1), ("deleted", 1)), {"unique": True}),
            ],
            "VALIDATOR": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "title": "Node object validation",
                    "required": ["_id", "node_id", "session_id", "path", "deleted"],
                    "additionalProperties": False,
                    "properties": {
                        "_id": {"bsonType": "objectId"},
                        "node_id": {
                            "bsonType": "objectId",
                            "description": "The ID that represents this nodes. Different from the _id field, which is a document ID.",
                        },
                        "session_id": {"bsonType": "string", "description": "Session that modified the node, a required string"},
                        "path": {"bsonType": "string", "description": "The node path within the repository tree, a required string"},
                        "deleted": {
                            "bsonType": "int",
                            "enum": [0, 1],
                            "description": "Flag marking the node as deleted in this session: 0=False, 1=True",
                        },
                    },
                },
            },
        },
        "TAGS": {
            "NAME": "tags",
            "INDEXES": [],
            "VALIDATOR": None,
        },
        "BRANCHES": {
            "NAME": "branches",
            "INDEXES": [],
            "VALIDATOR": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "properties": {
                        "commit_id": {"bsonType": "objectId", "description": "The commit the branch is currently pointing to"},
                    },
                }
            },
        },
    },
}
