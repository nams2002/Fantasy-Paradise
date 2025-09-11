from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    message_type: str = "text"
    sender_type: str  # "user" or "character"

class MessageCreate(MessageBase):
    conversation_id: int
    character_id: int

class Message(MessageBase):
    id: int
    conversation_id: int
    user_id: int
    character_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: Optional[str] = None

class ConversationCreate(ConversationBase):
    character_id: int

class Conversation(ConversationBase):
    id: int
    user_id: int
    character_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ConversationWithMessages(Conversation):
    messages: List[Message] = []
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    message: str
    character_name: str
    conversation_id: int
    message_id: int
