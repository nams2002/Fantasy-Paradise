from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.conversation import Conversation as ConversationModel, Message as MessageModel
from app.models.character import Character as CharacterModel
from app.schemas.conversation import (
    Conversation, ConversationCreate, ConversationWithMessages,
    Message, MessageCreate, ChatRequest, ChatResponse
)
from app.services.openai_service import OpenAIService
from app.services.character_service import CharacterService

router = APIRouter()

# For demo purposes, we'll use a dummy user_id
# In production, this would come from authentication
DEMO_USER_ID = 1

@router.post("/start", response_model=Conversation)
def start_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    """Start a new conversation with a character"""
    # Verify character exists
    character = db.query(CharacterModel).filter(
        CharacterModel.id == conversation.character_id,
        CharacterModel.is_active == True
    ).first()
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Create conversation
    db_conversation = ConversationModel(
        user_id=DEMO_USER_ID,
        character_id=conversation.character_id,
        title=conversation.title or f"Chat with {character.display_name}"
    )
    
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    
    return db_conversation

@router.post("/message", response_model=ChatResponse)
def send_message(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Send a message and get character response"""
    openai_service = OpenAIService()
    
    # Get or create conversation
    if chat_request.conversation_id:
        conversation = db.query(ConversationModel).filter(
            ConversationModel.id == chat_request.conversation_id,
            ConversationModel.user_id == DEMO_USER_ID
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # For demo, we'll assume character_id = 1 if no conversation specified
        # In production, this should be handled differently
        raise HTTPException(status_code=400, detail="Conversation ID required")
    
    # Get character
    character = db.query(CharacterModel).filter(
        CharacterModel.id == conversation.character_id
    ).first()
    
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Save user message
    user_message = MessageModel(
        conversation_id=conversation.id,
        user_id=DEMO_USER_ID,
        character_id=character.id,
        content=chat_request.message,
        sender_type="user"
    )
    db.add(user_message)
    db.commit()
    
    # Get conversation history
    conversation_history = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation.id
    ).order_by(MessageModel.created_at).all()
    
    # Generate character response
    try:
        character_response = openai_service.generate_character_response(
            character, conversation_history[:-1], chat_request.message
        )
    except Exception as e:
        # Fallback response if OpenAI fails
        character_response = f"I'm having trouble thinking right now, but I'm still here for you! 💕"
    
    # Save character message
    character_message = MessageModel(
        conversation_id=conversation.id,
        user_id=DEMO_USER_ID,
        character_id=character.id,
        content=character_response,
        sender_type="character"
    )
    db.add(character_message)
    db.commit()
    db.refresh(character_message)
    
    return ChatResponse(
        message=character_response,
        character_name=character.display_name,
        conversation_id=conversation.id,
        message_id=character_message.id
    )

@router.get("/conversations", response_model=List[Conversation])
def get_conversations(db: Session = Depends(get_db)):
    """Get all conversations for the user"""
    conversations = db.query(ConversationModel).filter(
        ConversationModel.user_id == DEMO_USER_ID,
        ConversationModel.is_active == True
    ).order_by(ConversationModel.updated_at.desc()).all()
    
    return conversations

@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Get a specific conversation with all messages"""
    conversation = db.query(ConversationModel).filter(
        ConversationModel.id == conversation_id,
        ConversationModel.user_id == DEMO_USER_ID
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversation

@router.post("/send", response_model=dict)
def send_direct_message(
    request: dict,
    db: Session = Depends(get_db)
):
    """Send a direct message to a character (simplified endpoint for frontend)"""
    openai_service = OpenAIService()

    message = request.get("message")
    character_id = request.get("character_id", 1)
    user_id = request.get("user_id", DEMO_USER_ID)

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Get character
    character = db.query(CharacterModel).filter(
        CharacterModel.id == character_id,
        CharacterModel.is_active == True
    ).first()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Get or create conversation for this user and character
    conversation = db.query(ConversationModel).filter(
        ConversationModel.user_id == user_id,
        ConversationModel.character_id == character_id,
        ConversationModel.is_active == True
    ).first()

    if not conversation:
        # Create new conversation
        conversation = ConversationModel(
            user_id=user_id,
            character_id=character_id,
            title=f"Chat with {character.display_name}"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save user message
    user_message = MessageModel(
        conversation_id=conversation.id,
        user_id=user_id,
        character_id=character.id,
        content=message,
        sender_type="user"
    )
    db.add(user_message)
    db.commit()

    # Get conversation history (last 10 messages for context)
    conversation_history = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation.id
    ).order_by(MessageModel.created_at.desc()).limit(10).all()
    conversation_history.reverse()  # Reverse to get chronological order

    # Generate character response
    try:
        character_response = openai_service.generate_character_response(
            character, conversation_history[:-1], message, user_id
        )
    except Exception as e:
        print(f"OpenAI Error: {e}")  # Debug logging
        # Fallback response if OpenAI fails
        character_response = f"I'm having trouble thinking right now, but I'm still here for you! 💕"

    # Save character message
    character_message = MessageModel(
        conversation_id=conversation.id,
        user_id=user_id,
        character_id=character.id,
        content=character_response,
        sender_type="character"
    )
    db.add(character_message)
    db.commit()

    return {
        "response": character_response,
        "character_name": character.display_name,
        "conversation_id": conversation.id
    }
