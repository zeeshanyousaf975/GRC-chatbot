from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import uuid4, UUID

class Message(BaseModel):
    """Chat message model"""
    id: UUID = Field(default_factory=uuid4)
    content: str
    role: str  # 'user' or 'assistant'
    timestamp: datetime = Field(default_factory=datetime.now)

class Conversation(BaseModel):
    """Conversation model containing multiple messages"""
    id: UUID = Field(default_factory=uuid4)
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def add_message(self, content: str, role: str) -> Message:
        """Add a new message to the conversation"""
        message = Message(content=content, role=role)
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message 