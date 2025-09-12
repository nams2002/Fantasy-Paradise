"use client";

import React, { useState, useEffect, useRef } from "react";
import styled, { keyframes } from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import Navbar from "@/component/Navbar";

// ---------------------------------------------
// API Configuration
// ---------------------------------------------
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

// ---------------------------------------------
// Interfaces
// ---------------------------------------------
interface Character {
  id: number;
  name: string;
  display_name: string;
  description: string;
  avatar_urls: string[];
  personality: string;
  conversation_style: string;
  age_range: string;
  background_story: string;
}

interface Message {
  id: number;
  sender: "human" | "bot";
  text: string;
  timestamp?: Date;
}

interface TrendingTopic {
  id: number;
  title: string;
  description: string;
}

const naughtyTopics: TrendingTopic[] = [
  {
    id: 1,
    title: "💋 Forbidden Confessions",
    description: "Tell me your dirtiest secrets... I promise I won't judge, only pleasure you more 😈",
  },
  {
    id: 2,
    title: "🔥 Release Your Tension",
    description: "Let me help you unwind in the most satisfying way... You deserve to feel amazing 💦",
  },
  {
    id: 3,
    title: "😈 Taboo Roleplay",
    description: "Step into your wildest fantasies... I'll be whoever you want me to be, daddy 🍑",
  },
  {
    id: 4,
    title: "💦 Your Deepest Cravings",
    description: "Share what makes you throb with desire... I'm here to make it all come true 🔥",
  },
  {
    id: 5,
    title: "🍯 Sweet Seduction",
    description: "Let me worship you and give you all the attention your body is craving right now 💋",
  },
];

// ---------------------------------------------
// Keyframes & Animations
// ---------------------------------------------
const gradientFlow = keyframes`
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
`;

const shimmerAnimation = keyframes`
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
`;

// ---------------------------------------------
// Layout Styled Components using CSS Grid
// ---------------------------------------------
const TalkroomContainer = styled.div`
  display: grid;
  grid-template-columns: 2fr 2fr;
  height: 100vh;
  background: linear-gradient(to right, #000428, #004e92);
  padding-top: 120px;

  @media (max-width: 1024px) {
    padding-top: 80px;
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
    min-height: 100vh; /* Ensure background covers full mobile screen */
  }
`;

// Left Column: Agent Info Card & Trending Topics
const LeftColumn = styled.div`
  padding: 20px 60px;
  background: transparent;
  @media (max-width: 480px) {
    padding: 20px;
  }
`;

// Right Column: Chat Section
const RightColumn = styled.div`
  padding: 20px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(5px);

  @media (max-width: 480px) {
    padding: 15px;
    margin: 10px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
  }
`;

// ---------------------------------------------
// Chat Window Styled Components
// ---------------------------------------------
const ChatWindow = styled.div`
  flex: 1;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 20px;
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  @media (max-width: 480px) {
    padding: 15px;
    margin: 10px;
    border-radius: 8px;
  }
`;

// New container to anchor messages at bottom
const MessagesContainer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow-y: auto;
  padding: 15px;
  max-height: calc(100vh - 300px);
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 15px;

  /* Custom scrollbar */
  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  @media (max-width: 480px) {
    padding: 10px;
    margin-bottom: 10px;
  }
`;

// Chat Input Components
const ChatInputContainer = styled.div`
  display: flex;
  gap: 12px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);

  @media (max-width: 480px) {
    padding: 15px;
    gap: 10px;
  }
`;

const ChatInput = styled.input`
  flex: 1;
  padding: 14px 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 14px;
  font-family: ${({ theme }) => theme.typography.title};
  outline: none;
  transition: all 0.3s ease;

  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
    font-style: italic;
  }

  &:focus {
    border-color: #ff00ff;
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.3);
    transform: scale(1.02);
  }

  @media (max-width: 480px) {
    padding: 12px 16px;
    font-size: 13px;
  }
`;

const SendButton = styled.button`
  padding: 14px 24px;
  background: linear-gradient(135deg, #ff00ff, #00ffff, #ff00ff);
  background-size: 200% 200%;
  border: none;
  border-radius: 25px;
  color: white;
  font-weight: bold;
  font-family: ${({ theme }) => theme.typography.title};
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 0, 255, 0.3);
  animation: ${gradientFlow} 3s ease infinite;

  &:hover {
    transform: scale(1.05) translateY(-2px);
    box-shadow: 0 8px 25px rgba(255, 0, 255, 0.5);
  }

  &:active {
    transform: scale(0.98);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    animation: none;
  }

  @media (max-width: 480px) {
    padding: 12px 20px;
    font-size: 13px;
  }
`;

const ChatMessageContainer = styled(motion.div)`
  display: flex;
  align-items: flex-end;
  gap: 10px;
  margin: 8px 0;
  padding: 4px 0;
`;

const ChatBubble = styled.div<{ sender: "human" | "bot" }>`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 14px;
  line-height: 1.4;
  @media (max-width: 480px) {
    font-size: 12px;
    line-height: 1.3;
  }
  background: ${(props) =>
    props.sender === "human"
      ? "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
      : "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"};
  color: #fff;
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 75%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);

  /* Add some animation */
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  }
`;

const Avatar = styled.img`
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;

  &:hover {
    transform: scale(1.1);
    border-color: rgba(255, 255, 255, 0.6);
  }

  @media (max-width: 480px) {
    width: 32px;
    height: 32px;
  }
`;

// ---------------------------------------------
// Agent Info Card (Left Column)
// ---------------------------------------------
const AnimatedWrapper = styled(motion.div)<{ gradient: string }>`
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 6px;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;

  @media (max-width: 480px) {
    max-width: 150px;
  }

  &::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 20px;
    background: ${(props) => props.gradient};
    background-size: 400% 400%;
    animation: ${gradientFlow} 6s infinite linear;
    z-index: 2;
    opacity: 0.9;
    pointer-events: none;
  }
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.4),
              0 0 20px rgba(0, 255, 255, 0.4);
`;

const SmallCardContent = styled.div`
  position: relative;
  border-radius: 19px;
  width: 100%;
  height: 340px;
  z-index: 3;

  @media (max-width: 480px) {
    width: 150px;
    height: 150px;
    margin: 0 auto;
  }
`;

const ImageContainer = styled.div`
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;

  @media (max-width: 480px) {
    border-radius: 15px;
  }
`;

const ShimmerDiv = styled.div`
  width: 100%;
  height: 100%;
  background-image: linear-gradient(90deg, #2a2c2d 0px, #323335 40px, #2f3234 80px);
  animation: ${shimmerAnimation} 1.5s infinite linear;
  position: absolute;
  top: 0;
  left: 0;
`;

const DotsContainer = styled.div`
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 4px;
`;

const DotDiv = styled.div<{ active: boolean }>`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: ${(props) =>
    props.active ? "#fff" : "rgba(255,255,255,0.5)"};
`;

const AgentTextContainer = styled.div`
  color: ${({ theme }) => theme.colors.text.primary};
  margin-top: 30px;
  text-align: center;
  font-family: ${({ theme }) => theme.typography.title};

  h2 {
    color: ${({ theme }) => theme.colors.text.primary};
    font-size: 24px;
    margin-bottom: 5px;
    @media (max-width: 768px) {
      font-size: 16px;
    }
    @media (max-width: 480px) {
      font-size: 14px;
    }
  }

  p {
    font-size: 16px;
    @media (max-width: 768px) {
      font-size: 14px;
    }
    @media (max-width: 480px) {
      font-size: 12px;
    }
  }
`;

// ---------------------------------------------
// Carousel Component
// ---------------------------------------------
interface CarouselProps {
  images: string[];
}

const Carousel: React.FC<CarouselProps> = ({ images }) => {
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const variants = {
    initial: { x: "100%", opacity: 0 },
    animate: { x: "0%", opacity: 1 },
    exit: { x: "-100%", opacity: 0 },
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) =>
        prev === images.length - 1 ? 0 : prev + 1
      );
      setIsLoading(true);
    }, 3000);
    return () => clearInterval(interval);
  }, [images.length]);

  return (
    <ImageContainer>
      <AnimatePresence initial={false}>
        <motion.img
          key={currentIndex}
          src={images[currentIndex]}
          alt={`Agent image ${currentIndex + 1}`}
          variants={variants}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={{ duration: 0.5, ease: "easeInOut" }}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            position: "absolute",
            top: 0,
            left: 0,
            borderRadius: "inherit",
          }}
          onLoad={() => setIsLoading(false)}
        />
      </AnimatePresence>
      {isLoading && <ShimmerDiv />}
      <DotsContainer>
        {images.map((_, idx) => (
          <DotDiv key={idx} active={idx === currentIndex} />
        ))}
      </DotsContainer>
    </ImageContainer>
  );
};

interface CharacterInfoCardProps {
  character: Character;
  gradient: string;
}

const CharacterInfoCard: React.FC<CharacterInfoCardProps> = ({
  character,
  gradient,
}) => {
  const images = character.avatar_urls?.length > 0
    ? character.avatar_urls
    : ["/assets/story.png", "/assets/story.png", "/assets/story.png"];

  return (
    <>
      <motion.div
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
      >
        <AnimatedWrapper gradient={gradient}>
          <SmallCardContent>
            <Carousel images={images} />
          </SmallCardContent>
        </AnimatedWrapper>
      </motion.div>
      <AgentTextContainer>
        <h2>{character.display_name}</h2>
        <p>{character.description}</p>
        <div style={{ marginTop: '10px', fontSize: '12px', opacity: 0.8 }}>
          <p>Age: {character.age_range} • Style: {character.conversation_style}</p>
        </div>
      </AgentTextContainer>
    </>
  );
};

// ---------------------------------------------
// Trending Topics Styled Components
// ---------------------------------------------
const TrendingTopicsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 24px;
`;

const TrendingTopicCard = styled(motion.div)`
  background: linear-gradient(45deg, #6a11cb, #2575fc);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: #fff;
  cursor: pointer;
  @media (max-width: 768px) {
    padding: 12px;
  }
  h3 {
    font-family: ${({ theme }) => theme.typography.title};
    color: ${({ theme }) => theme.colors.text.primary};
    font-size: 16px;
    margin-bottom: 10px;
    @media (max-width: 768px) {
      font-size: 14px;
    }
  }
  p {
    font-family: ${({ theme }) => theme.typography.title};
    color: ${({ theme }) => theme.colors.text.primary};
    font-size: 12px;
    line-height: 20px;
    @media (max-width: 768px) {
      font-size: 10px;
    }
  }
`;

// ---------------------------------------------
// Modal Components for Mobile Trending Topics
// ---------------------------------------------
const TrendingTopicsButton = styled.button`
    font-family: ${({ theme }) => theme.typography.title};
  background: #2575fc;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 10px;
  cursor: pointer;
  margin-top: 24px;
  width:100%;
`;

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const ModalContent = styled.div`
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
  position: relative;
`;

const CloseButton = styled.button`
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
`;

// ---------------------------------------------
// Siri-Type Animated Speaker Logo
// ---------------------------------------------
const SiriLogoWrapper = styled(motion.div)`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  position: absolute;
  bottom: 100px;
  left: 70%;
  transform: translateX(-50%);
  background: #0070f3;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: visible;

    @media (max-width: 420px) {
    left: 50%;
     bottom: 30px;
  }
`;

const PulseCircle = styled(motion.div)`
  position: absolute;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #0070f3;
`;

const SiriIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 14a3 3 0 003-3V5a3 3 0 10-6 0v6a3 3 0 003 3z" />
    <path d="M19 11a1 1 0 00-1-1h-1a1 1 0 00-1 1 5 5 0 01-10 0 1 1 0 00-1-1H6a1 1 0 00-1 1 7 7 0 007 7v3h2v-3a7 7 0 007-7z" />
  </svg>
);

const SiriLogo: React.FC<{ onClick: () => void }> = ({ onClick }) => {
  return (
    <SiriLogoWrapper onClick={onClick}>
      <PulseCircle
        animate={{ scale: [1, 1.5, 1], opacity: [0.5, 0, 0.5] }}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
      />
      <SiriIcon />
    </SiriLogoWrapper>
  );
};

// ---------------------------------------------
// API Functions
// ---------------------------------------------
const fetchCharacters = async (): Promise<Character[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/characters/`);
    if (!response.ok) throw new Error('Failed to fetch characters');
    return await response.json();
  } catch (error) {
    console.error('Error fetching characters:', error);
    return [];
  }
};

const sendMessage = async (message: string, characterId: number): Promise<string> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        character_id: characterId,
        user_id: 1, // Demo user ID
      }),
    });

    if (!response.ok) throw new Error('Failed to send message');
    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error('Error sending message:', error);
    return "I'm having trouble responding right now, but I'm still here for you! 💕";
  }
};

// ---------------------------------------------
// Main Talkroom Component
// ---------------------------------------------
const Talkroom: React.FC = () => {
  const [selectedCharacter, setSelectedCharacter] = useState<Character | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isMobile, setIsMobile] = useState<boolean>(false);
  const [showTrendingModal, setShowTrendingModal] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load characters from API
    const loadCharacters = async () => {
      const fetchedCharacters = await fetchCharacters();

      // Get selected character from localStorage or use first character
      const storedCharacterId = localStorage.getItem("selectedCharacterId");
      const selectedChar = storedCharacterId
        ? fetchedCharacters.find(c => c.id === parseInt(storedCharacterId))
        : fetchedCharacters[0];

      if (selectedChar) {
        setSelectedCharacter(selectedChar);
        setMessages([
          {
            id: 1,
            sender: "bot",
            text: `Mmm, hello gorgeous... I'm ${selectedChar.display_name}. ${selectedChar.description} I've been waiting for you to come play with me... What naughty thoughts are running through your mind right now? 😈💋`,
            timestamp: new Date(),
          },
        ]);
      }
    };

    loadCharacters();

    // Check screen width for mobile
    const checkMobile = () => setIsMobile(window.innerWidth <= 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !selectedCharacter || isLoading) return;

    const userMessage: Message = {
      id: messages.length + 1,
      sender: "human",
      text: inputMessage.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await sendMessage(inputMessage.trim(), selectedCharacter.id);

      const botMessage: Message = {
        id: messages.length + 2,
        sender: "bot",
        text: response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Simulate voice interaction when the Siri logo is clicked.
  const handleVoiceClick = () => {
    const suggestions = [
      "I want you so bad right now 🔥",
      "Make me forget all my stress, baby 💋",
      "Tell me what you'd do to me 😈",
      "I'm so hard/wet thinking about you 💦",
      "Be my naughty little secret 🍑",
      "I need you to take control of me 😍",
      "Show me how good you can make me feel 🔥"
    ];

    const randomSuggestion = suggestions[Math.floor(Math.random() * suggestions.length)];
    setInputMessage(randomSuggestion);
  };

  if (!selectedCharacter) return <div>Loading...</div>;

  return (
    <div>
      <Navbar />
      <TalkroomContainer>
        {/* Left Column: Character Info & Trending Topics */}
        <LeftColumn>
          <CharacterInfoCard
            character={selectedCharacter}
            gradient="linear-gradient(45deg, #ff00ff, #00ffff, #ffcc00, #ff00ff)"
          />
          {isMobile ? (
            <>
              <TrendingTopicsButton
                onClick={() => setShowTrendingModal(true)}
              >
                🔥 Turn Me On With These Topics
              </TrendingTopicsButton>
              {showTrendingModal && (
                <ModalOverlay>
                  <ModalContent>
                    <CloseButton
                      onClick={() => setShowTrendingModal(false)}
                    >
                      &times;
                    </CloseButton>
                    <TrendingTopicsContainer>
                      {naughtyTopics.map((topic, index) => (
                        <TrendingTopicCard
                          key={topic.id}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{
                            delay: index * 0.2,
                            duration: 0.5,
                          }}
                          whileHover={{
                            scale: 1.05,
                            transition: {
                              type: "spring",
                              stiffness: 300,
                            },
                          }}
                          onClick={() => {
                            setInputMessage(topic.description);
                            setShowTrendingModal(false);
                          }}
                        >
                          <h3>{topic.title}</h3>
                          <p>{topic.description}</p>
                        </TrendingTopicCard>
                      ))}
                    </TrendingTopicsContainer>
                  </ModalContent>
                </ModalOverlay>
              )}
            </>
          ) : (
            <TrendingTopicsContainer>
              {naughtyTopics.map((topic, index) => (
                <TrendingTopicCard
                  key={topic.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.2, duration: 0.5 }}
                  whileHover={{
                    scale: 1.05,
                    transition: { type: "spring", stiffness: 300 },
                  }}
                  onClick={() => setInputMessage(topic.description)}
                >
                  <h3>{topic.title}</h3>
                  <p>{topic.description}</p>
                </TrendingTopicCard>
              ))}
            </TrendingTopicsContainer>
          )}
        </LeftColumn>

        {/* Right Column: Chat Interface */}
        <RightColumn>
          <ChatWindow>
            <MessagesContainer>
              <AnimatePresence>
                {messages.map((msg) => (
                  <ChatMessageContainer
                    key={msg.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.5 }}
                    style={{
                      justifyContent:
                        msg.sender === "human" ? "flex-end" : "flex-start",
                    }}
                  >
                    {msg.sender === "bot" && (
                      <Avatar
                        src={selectedCharacter.avatar_urls?.[0] || "/assets/story.png"}
                        alt="Character"
                      />
                    )}
                    <ChatBubble sender={msg.sender}>{msg.text}</ChatBubble>
                    {msg.sender === "human" && (
                      <Avatar src="/assets/trend.png" alt="User" />
                    )}
                  </ChatMessageContainer>
                ))}
                {isLoading && (
                  <ChatMessageContainer
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    style={{ justifyContent: "flex-start" }}
                  >
                    <Avatar
                      src={selectedCharacter.avatar_urls?.[0] || "/assets/story.png"}
                      alt="Character"
                    />
                    <ChatBubble sender="bot">
                      <motion.div
                        animate={{ opacity: [0.5, 1, 0.5] }}
                        transition={{ duration: 1.5, repeat: Infinity }}
                      >
                        Typing...
                      </motion.div>
                    </ChatBubble>
                  </ChatMessageContainer>
                )}
              </AnimatePresence>
              <div ref={messagesEndRef} />
            </MessagesContainer>

            <ChatInputContainer>
              <ChatInput
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={`Tell ${selectedCharacter.display_name} your desires... 💋`}
                disabled={isLoading}
              />
              <SendButton
                onClick={handleSendMessage}
                disabled={isLoading || !inputMessage.trim()}
              >
                💋 Send
              </SendButton>
            </ChatInputContainer>


          </ChatWindow>
        </RightColumn>
      </TalkroomContainer>
          <SiriLogo onClick={handleVoiceClick} />

    </div>
  );
};

export default Talkroom;
