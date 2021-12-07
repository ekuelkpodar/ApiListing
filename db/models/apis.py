from sqlalchemy import Column, Integer, String, Boolean, Date , ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Api(Base):
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    provider = Column(String,nullable=False)
    url = Column(String)
    category = Column(String,nullable=False)
    description = Column(String)
    date_posted = Column(Date)
    is_active = Column(Boolean(),default = True)
    owner_id = Column(Integer,ForeignKey('user.id'))
    owner = relationship("User",back_populates="apis")