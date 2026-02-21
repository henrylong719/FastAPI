from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ...core.db import engine
from ...models import Item

router = APIRouter(prefix="/items", tags=["items"])


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/", response_model=Item)
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/", response_model=list[Item])
def list_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()