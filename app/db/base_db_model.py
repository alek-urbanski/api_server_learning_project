from typing import Any, Dict

from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    """Base class for orm"""

    pass

# I use from_orm method of pydantic BaseModel, 
# but approach below may be convenient in more complex scenarios
# def model_to_dict(obj: Base) -> Dict[str, Any]:
#    """Serialization of a base Model."""
#    mapper = orm.class_mapper(obj.__class__)
#    return {c.key: getattr(obj, c.key) for c in mapper.column_attrs}
