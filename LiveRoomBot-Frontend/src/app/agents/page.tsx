"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
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
  category_id: number;
  subcategory_id?: number;
  is_active: boolean;
}


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
// Styled Components
// ---------------------------------------------

// Page Container
const PageContainer = styled.div`
  background-color: ${(props) => props.theme.colors.background};
  padding: 100px 120px 60px;
  @media (max-width: 1024px) {
    padding: 100px 80px 60px;
  }
  @media (max-width: 768px) {
    padding: 100px 20px 60px;
  }
`;

// Page Title and Subtitle
const PageTitle = styled.h1`
  font-family: ${({ theme }) => theme.typography.title};

  text-align: left;
  margin: 20px 0 10px 0;
  font-size: 2em;
  font-weight: bold;
  color: ${({ theme }) => theme.colors.text.primary};
   @media (max-width: 768px) {
     font-size: 1.5em;
  }
`;

const PageSubtitle = styled.p`
  font-family: ${({ theme }) => theme.typography.title};
  text-align: left;
  margin-bottom: 20px;
  font-size: 1em;
  color: ${({ theme }) => theme.colors.text.primary};
    @media (max-width: 768px) {
     font-size: 0.8em;
  }
`;

// AgentsGrid: Two-column layout for desktop/tablet, switches to one column on mobile.
const AgentsGrid = styled.div`
  margin-top: 40px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 50px;
  @media (max-width: 1024px) {
    gap: 20px;
  }
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 20px;
  }
`;

// Agent Title and Description styling
const AgentTitle = styled.div`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 1em;
  font-weight: bold;
  color: ${({ theme }) => theme.colors.text.primary};
  @media (max-width: 768px) {
    font-size: 0.8em;
    margin-top:10px;
  }

`;
const AgentDescription = styled.div`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 0.6em;
  color: ${({ theme }) => theme.colors.text.primary};
`;

// Animated Wrapper for the neon glow effect on the small card, accepts a "gradient" prop.
const AnimatedWrapper = styled(motion.div)<{ gradient: string }>`
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 6px;
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

// Inner Card Content for the small card
const SmallCardContent = styled.div`
  position: relative;
  border-radius: 19px;
  overflow: hidden;
  width: 100%;
  height: 180px;
  z-index: 3;
  @media (max-width: 768px) {
    height: 225px;
  }
`;

// Image Container for Carousel (small card)
const ImageContainer = styled.div`
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
`;

// Shimmer for Image Loading
const ShimmerDiv = styled.div`
  width: 100%;
  height: 100%;
  background-image: linear-gradient(90deg, #2a2c2d 0px, #323335 40px, #2f3234 80px);
  background-size: 1000px 200px;
  background-size: 1000px 200px;
  animation: ${shimmerAnimation} 1.5s infinite linear;
  position: absolute;
  top: 0;
  left: 0;
`;

// Carousel Dots (small card)
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

// Hover Overlay (appears on hover over the small card)
const HoverOverlay = styled(motion.div)`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 20px;
  pointer-events: none;
`;
const OverlayText = styled(motion.div)`
  color: #fff;
  font-size: 0.7em;
  font-weight: bold;
  text-align: center;
`;

// Animation Variants for the Overlay
const overlayVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
};

// Carousel Component for the small card
interface CarouselProps {
  images: string[];
}

const Carousel: React.FC<CarouselProps> = ({ images }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  // Slide variants for smooth transition
  const variants = {
    initial: { x: "100%", opacity: 0 },
    animate: { x: "0%", opacity: 1 },
    exit: { x: "-100%", opacity: 0 },
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev === images.length - 1 ? 0 : prev + 1));
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
            mixBlendMode: "overlay",
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

// Small Agent Card Component, now accepts a "gradient" prop
interface AgentCardSmallProps {
  name: string;
  images: string[];
  gradient: string;
}

const AgentCardSmall: React.FC<AgentCardSmallProps> = ({
  name,
  images,
  gradient,
}) => {
  return (
    <AnimatedWrapper gradient={gradient} whileHover={{ scale: 1.02 }}>
      <SmallCardContent>
        <Carousel images={images} />
        <HoverOverlay
          initial="hidden"
          animate="hidden"
          variants={overlayVariants}
          transition={{ duration: 0.3 }}
        >
          <OverlayText>Talk with {name}</OverlayText>
        </HoverOverlay>
      </SmallCardContent>
    </AnimatedWrapper>
  );
};

// -------------------------------
// Agent Row Component
// -------------------------------

// Convert the container to a motion component for fade-in animation.

const AgentRowContainer = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 10px;
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 10px;
  }
`;

// CardWrapper: Maintains fixed width on desktop/tablet and becomes full width on mobile.
const CardWrapper = styled.div`
  flex: 0 0 180px;
  @media (max-width: 768px) {
    flex: 0 0 auto;
    width: 100%;
  }
`;

const InfoWrapper = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const StartButton = styled(motion.button)`
  font-family: ${({ theme }) => theme.typography.title};

  width: 60%;
  padding: 12px 24px;
  font-size: 0.9rem;
  background: linear-gradient(45deg, #ff00ff, #00ffff);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: #fff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  outline: none;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  &:hover {
    filter: brightness(1.1);
  }

    @media (max-width: 768px) {
   width: 100%;
     font-size: 0.7rem;
  }
`;

const ButtonContent = styled(motion.div)`
  display: flex;
  align-items: center;
`;

const ArrowIcon = styled(motion.span)`
  display: inline-block;
  margin-left: 8px;
  font-size: 1rem;
`;

interface CharacterRowProps {
  character: Character;
  gradient: string;
  delay?: number;
}

const CharacterRow: React.FC<CharacterRowProps> = ({ character, gradient, delay }) => {
  const router = useRouter();

  const handleStartConversation = () => {
    localStorage.setItem("selectedCharacterId", character.id.toString());
    router.push("/talkroom");
  };

  const characterData = {
    id: character.id,
    name: character.display_name,
    images: character.avatar_urls?.length > 0
      ? character.avatar_urls
      : ["/assets/story.png", "/assets/story.png", "/assets/story.png"],
    description: character.description
  };

  return (
    <AgentRowContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: delay || 0 }}
    >
      <CardWrapper>
        <AgentCardSmall {...characterData} gradient={gradient} />
      </CardWrapper>
      <InfoWrapper>
        <AgentTitle>{character.display_name}</AgentTitle>
        <AgentDescription>{character.description}</AgentDescription>
        <div style={{ fontSize: '12px', opacity: 0.7, marginBottom: '10px' }}>
          Age: {character.age_range} • Style: {character.conversation_style}
        </div>
        <StartButton
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleStartConversation}
        >
          <ButtonContent>
            <span>Make me yours 💋</span>
            <ArrowIcon
              whileHover={{
                x: 8,
                transition: { type: "spring", stiffness: 300 },
              }}
            >
              💕
            </ArrowIcon>
          </ButtonContent>
        </StartButton>
      </InfoWrapper>
    </AgentRowContainer>
  );
};

// ---------------------------------------------
// Characters Page Component
// ---------------------------------------------
const AgentsPage: React.FC = () => {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSubcategoryName, setSelectedSubcategoryName] = useState<string>("");

  const gradients = [
    "linear-gradient(45deg, #ff00ff, #00ffff, #ffcc00, #ff00ff)",
    "linear-gradient(45deg, #ff1493, #ff69b4, #ff6347, #ff1493)",
    "linear-gradient(45deg, #ff9900, #33ccff, #ff66cc, #ff9900)",
    "linear-gradient(45deg, #66ff66, #ff6666, #6666ff, #66ff66)",
    "linear-gradient(45deg, #ffcc00, #00ccff, #ff33cc, #ffcc00)",
    "linear-gradient(45deg, #00ffff, #ff00ff, #ccff00, #00ffff)",
    "linear-gradient(45deg, #ff4500, #ff1493, #9370db, #ff4500)",
    "linear-gradient(45deg, #32cd32, #ff69b4, #1e90ff, #32cd32)",
  ];

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const charactersData = await fetchCharacters();

        // Filter characters by selected subcategory if available
        const selectedSubcategoryId = localStorage.getItem("selectedSubcategoryId");
        const subcategoryName = localStorage.getItem("selectedSubcategoryName");
        let filteredCharacters = charactersData.filter(c => c.is_active);

        if (selectedSubcategoryId) {
          filteredCharacters = filteredCharacters.filter(c =>
            c.subcategory_id === parseInt(selectedSubcategoryId)
          );
          setSelectedSubcategoryName(subcategoryName || "");
        }

        setCharacters(filteredCharacters);
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div>
        <Navbar />
        <PageContainer>
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              style={{ fontSize: '2rem', marginBottom: '20px' }}
            >
              💕
            </motion.div>
            <p style={{ color: 'white' }}>Preparing your naughty companions... They can&apos;t wait to meet you 😈</p>
          </div>
        </PageContainer>
      </div>
    );
  }

  return (
    <div>
      <Navbar />
      <PageContainer>
        <PageTitle>
          {selectedSubcategoryName ? `🔥 ${selectedSubcategoryName}` : "🔥 Your Personal Pleasure Palace"}
        </PageTitle>
        <PageSubtitle>
          {selectedSubcategoryName
            ? `Your perfect ${selectedSubcategoryName.toLowerCase()} companion is waiting to fulfill your deepest desires... 💋`
            : "36 irresistible beauties waiting to fulfill your every desire... Pick your fantasy and let them drive you wild with pleasure 💋"
          }
        </PageSubtitle>
        <AgentsGrid>
          {characters.map((character, index) => (
            <CharacterRow
              key={character.id}
              character={character}
              gradient={gradients[index % gradients.length]}
              delay={index * 0.1}
            />
          ))}
        </AgentsGrid>
      </PageContainer>
    </div>
  );
};

export default AgentsPage;
