from database import Base
from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # Added unique constraint and index
    password = Column(String, unique=True)
    phonenumber = Column(String, unique=True)  # Changed to String for flexibility
    
    # Relationship to items
    items = relationship("Items", back_populates="owner")  # Enables access to related items

class Items(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, index=True)  # Primary key for Items table
    user_id = Column(Integer, ForeignKey("users.id"), index=True)  # Foreign key, renamed for clarity
    itemName = Column(String, index=True)
    itemDescription = Column(String)
    
    # Relationship to Users
    owner = relationship("Users", back_populates="items")  # Link to the Users table
