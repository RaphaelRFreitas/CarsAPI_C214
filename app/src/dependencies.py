"""
"""

from app.src.repositories import Repository, MongoRepository


def get_repository() -> Repository:
    """
    """
    return MongoRepository()


REPOSITORY_INJECTION = get_repository()
