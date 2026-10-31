from typing import Any

from pinecone import Pinecone

from semantic_search.config import get_settings


def clear_namespace(settings: Any, client_factory=Pinecone) -> None:
    client = client_factory(api_key=settings.pinecone_api_key)
    index = client.Index(settings.pinecone_index_name)
    index.delete(
        delete_all=True,
        namespace=settings.pinecone_namespace,
    )


def main() -> None:
    settings = get_settings()
    clear_namespace(settings)
    print(
        f"All vectors were deleted from namespace '{settings.pinecone_namespace}'. "
        "The index schema was preserved."
    )


if __name__ == "__main__":
    main()
