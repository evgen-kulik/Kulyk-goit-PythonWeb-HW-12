from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter  # для обмеження кількості запитів

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


# dependencies=[Depends(RateLimiter(times=2, seconds=5))] - обмеження кількості запитів
@router.get(
    "/",
    response_model=List[ContactResponse],
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def get_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contacts function returns a list of contacts.

    :param skip: int: Skip the first n contacts
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Get the database session
    :param current_user: User: Get the user id from the jwt token
    :param : Get the contact id from the url
    :return: A list of contacts
    :doc-author: Trelent
    """

    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contact function is a GET endpoint that returns the contact with the given ID.
    It requires an authorization token in order to access it.

    :param contact_id: int: Specify the contact_id that is passed in the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :param : Get the contact id from the url
    :return: A contact object
    :doc-author: Trelent
    """

    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post(
    "/",
    response_model=ContactResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Specify the data type of the request body
    :param db: Session: Get the database session
    :return: A contactmodel object
    :doc-author: Trelent
    """

    return await repository_contacts.create_contact(body, db)


@router.put(
    "/{tag_id}",
    response_model=ContactResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def update_contact(
    body: ContactModel,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_contact function updates a contact in the database.

    :param body: ContactModel: Pass the contact model to the function
    :param contact_id: int: Identify the contact to be updated
    :param db: Session: Pass in the database session
    :param current_user: User: Get the current user from the database
    :param : Get the contact id from the url
    :return: The updated contact
    :doc-author: Trelent
    """

    contact = await repository_contacts.update_contact(
        contact_id, body, db, current_user
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def remove_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact to be removed
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user from the database
    :param : Get the contact id from the url
    :return: The contact that was deleted
    :doc-author: Trelent
    """

    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
