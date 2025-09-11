"use client";
import React, { useState, useEffect } from "react";
import styled, { keyframes } from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";
import { useRouter } from "next/navigation";
import Navbar from "@/component/Navbar";

// ----------------- Common Animations & Gradients -----------------
const gradientFlow = keyframes`
  0% { background-position: 0% 50%; }
  100% { background-position: 100% 50%; }
`;
const shimmerAnimation = keyframes`
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
`;
const gradients = [
  "linear-gradient(45deg, #ff6ec4, #7873f5)",
  "linear-gradient(45deg, #ff9a9e, #fad0c4)",
  "linear-gradient(45deg, #a18cd1, #fbc2eb)",
];

// ----------------- Interfaces -----------------
interface Category {
  name: string;
  image: string;
}
interface Agent {
  id: number;
  name: string;
  images: string[];
  description: string;
}

// ----------------- CategoryCard Component -----------------
const CategoryCard: React.FC<{ category: Category }> = ({ category }) => {
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const randomGradient =
    gradients[Math.floor(Math.random() * gradients.length)];

  const handleCardClick = () => {
    if (typeof window !== "undefined") {
      localStorage.setItem("selectedCategory", category.name);
    }
    router.push("/agents");
  };

  return (
    <Card
      onClick={handleCardClick}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5 }}
      gradient={randomGradient}
    >
      <ImageContainer>
        {isLoading && <Shimmer />}
        <img
          src="assets/avatar2.png"
          alt={category.name}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity: isLoading ? 0 : 1,
            transition: "opacity 0.5s ease",
          }}
          onLoad={() => setIsLoading(false)}
        />
      </ImageContainer>
      <CardTitle>{category.name}</CardTitle>
    </Card>
  );
};

const Card = styled(motion.div)<{ gradient: string }>`
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  &:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }
  &::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 8px;
    background: ${(props) => props.gradient};
    background-size: 400% 400%;
    animation: ${gradientFlow} 6s infinite linear;
    z-index: 0;
    opacity: 1;
    pointer-events: none;
  }
`;
const ImageContainer = styled.div`
  width: 100%;
  height: 200px;
  position: relative;
  z-index: 1;
`;
const Shimmer = styled.div`
  width: 100%;
  height: 100%;
  background: #1c1d1e;
  background-image: linear-gradient(
    90deg,
    #2a2c2d 0px,
    #323335 40px,
    #2f3234 80px
  );
  background-size: 1000px 200px;
  animation: ${shimmerAnimation} 1.5s infinite linear;
  position: absolute;
  top: 0;
  left: 0;
`;
const CardTitle = styled.div`
  font-family: ${({ theme }) => theme.typography.title};
  padding: 10px;
  font-size: 1em;
  font-weight: bold;
  text-align: center;
  position: relative;
  z-index: 1;
  color: white;
`;

// ----------------- Hero Section -----------------
const HeroSection = styled.section`
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #fff;
  padding: 0 20px;
`;
const Background = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -2;
`;
const Overlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: -1;
`;
const Content = styled.div`
  position: relative;
  z-index: 1;
  max-width: 1200px;
  width: 100%;
    margin-top: 2rem;
`;
const HeroTitle = styled(motion.h1)`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 5rem;
  margin-bottom: 1rem;
  font-weight: bold;
  @media (min-width: 1200px) {
    font-size: 6rem;
  }
  @media (max-width: 768px) {
    font-size: 4rem;
  }
  @media (max-width: 480px) {
    font-size: 3rem;
  }
`;
const HeroSubtitle = styled(motion.h2)`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 3rem;
  margin-bottom: 1.5rem;
  @media (min-width: 1200px) {
    font-size: 3rem;
  }
  @media (max-width: 768px) {
    font-size: 2rem;
  }
  @media (max-width: 480px) {
    font-size: 1rem;
  }
`;
const HeroTagline = styled(motion.p)`
  font-family: ${({ theme }) => theme.typography.title};
  font-weight: 400;
  font-size: 1.5rem;
  margin-bottom: 2.5rem;
  @media (min-width: 1200px) {
    font-size: 1.5rem;
    font-weight: 400;
  }
  @media (max-width: 768px) {
    font-size: 1.75rem;
  }
  @media (max-width: 480px) {
    font-size: 1rem;
  }
`;
// Updated CTAButton with a slide-up hover effect
const CTAButton = styled(motion.button).attrs(() => ({
  whileHover: {
    scale: 1.05,
    y: -5,
    transition: { duration: 0.3 },
  },
  whileTap: { scale: 0.95 },
}))`
  font-family: ${({ theme }) => theme.typography.title};
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(45deg, #ff00ff, #00ffff);
  border: none;
  padding: 1rem 2.5rem;
  font-size: 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  color: #fff;
  outline: none;
  transition: background 0.3s ease;
  margin-top: 50px;
  &:hover {
    background: linear-gradient(45deg, #e600e6, #00e6e6);
  }
  @media (min-width: 1200px) {
    font-size: 1.75rem;
    padding: 1.2rem 3rem;
  }
  @media (max-width: 768px) {
    font-size: 1.25rem;
    padding: 0.9rem 2rem;
  }
  @media (max-width: 480px) {
    font-size: 1rem;
    padding: 0.75rem 1.5rem;
  }
`;
const Arrow = styled(motion.span)`
  font-size: 1.5rem;
  margin-left: 0.5rem;
  @media (min-width: 1200px) {
    font-size: 1.75rem;
  }
  @media (max-width: 768px) {
    font-size: 1.25rem;
  }
  @media (max-width: 480px) {
    font-size: 1rem;
  }
`;

// ----------------- Product Overview Section -----------------
const ProductOverviewSection = styled.section`
  padding: 2rem 1rem;
  background: linear-gradient(to right, #000428, #004e92);
  color: #fff;
  @media (min-width: 1200px) {
    padding: 12rem 2rem;
  }
`;
const OverviewWrapper = styled.div`
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 1rem;
  @media (min-width: 1200px) {
    padding: 0 2rem;
  }
`;
const OverviewTitle = styled(motion.h2)`
  font-family: ${({ theme }) => theme.typography.title};

  font-size: 2.5rem;
  text-align: left;
  margin-bottom: 2rem;
  color: #fff;
  @media (min-width: 1200px) {
    font-size: 3rem;
  }
  @media (max-width: 480px) {
    font-size: 2rem;
    text-align: center;
  }
  /* Gradient background */
  background: linear-gradient(270deg, #ff0080, #ff8c00, #40e0d0, #ff0080);
  background-size: 600% 600%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  
  /* Animate the gradient */
  animation: gradientFlow 8s ease infinite;

@keyframes gradientFlow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

`;
const OverviewContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;
const OverviewText = styled(motion.div)`
  font-family: ${({ theme }) => theme.typography.title};
  flex: 1;
  font-size: 1.2rem;
  line-height: 1.6;
  p {
    margin: 0;
  }
  @media (max-width: 768px) {
    font-size: 12px;
    text-align: center;
  }
`;
const OverviewGallery = styled(motion.div)`
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  width: auto;
  @media (max-width: 768px) {
    gap: 1rem;
    grid-template-columns: 1fr;
    width: 100%;
  }
`;

// ----------------- Agent Card Components -----------------
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
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.4), 0 0 20px rgba(0, 255, 255, 0.4);
`;
const SmallCardContent = styled.div`
  position: relative;
  border-radius: 19px;
  overflow: hidden;
  width: 100%;
  height: 400px;
  z-index: 3;
  @media (max-width: 768px) {
    height: 250px;
  }
`;
const AgentImageContainer = styled.div`
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
`;
const ShimmerDiv = styled.div`
  width: 100%;
  height: 100%;
  background-image: linear-gradient(
    90deg,
    #2a2c2d 0px,
    #323335 40px,
    #2f3234 80px
  );
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
  font-family: ${({ theme }) => theme.typography.title};
  color: #fff;
  font-size: 1em;
  font-weight: bold;
  text-align: center;
  width:80%;
`;
const overlayVariants = { hidden: { opacity: 0 }, visible: { opacity: 1 } };

interface CarouselProps {
  images: string[];
}
const Carousel: React.FC<CarouselProps> = ({ images }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
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
    <AgentImageContainer>
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
    </AgentImageContainer>
  );
};

interface AgentCardSmallProps extends Agent {
  gradient: string;
}

const AgentCardSmall: React.FC<AgentCardSmallProps> = ({
  name,
  images,
  gradient,
}) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <AnimatedWrapper
      gradient={gradient}
      whileHover={{ scale: 1.02 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
    >
      <SmallCardContent>
        <Carousel images={images} />
        <HoverOverlay
          animate={isHovered ? "visible" : "hidden"}
          variants={overlayVariants}
          transition={{ duration: 0.3 }}
        >
          <OverlayText>Talk with  <br/>{name}</OverlayText>
        </HoverOverlay>
      </SmallCardContent>
    </AnimatedWrapper>
  );
};

// ----------------- Future Scope Section -----------------
const FutureScopeSection = styled.section`
  padding: 6rem 2rem;
  background: linear-gradient(to right, #0d1117, #1a1e27);
  color: #fff;
  @media (min-width: 1200px) {
    padding: 10rem 2rem;
  }
  @media (max-width: 480px) {
    padding: 3rem 2rem;
  }
`;
const FutureScopeWrapper = styled.div`
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  gap: 2rem;
  @media (max-width: 768px) {
    flex-direction: column;
    padding: 0;
  }
`;
const FutureScopeText = styled.div`
  flex: 1;
  font-size: 1.5rem;
  line-height: 1.6;
  @media (max-width: 768px) {
    font-size: 1.2rem;
    text-align: center;
  }
h2 {
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 2.5rem;
  margin-bottom: 1rem;
  
  /* Gradient background */
  background: linear-gradient(270deg, #ff0080, #ff8c00, #40e0d0, #ff0080);
  background-size: 600% 600%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  
  /* Animate the gradient */
  animation: gradientFlow 8s ease infinite;

  @media (max-width: 480px) {
    font-size: 2rem;
    text-align: center;
    line-height: 35px;
  }
}

@keyframes gradientFlow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

  p {
    font-family: ${({ theme }) => theme.typography.title};

    font-size: 16px;
    line-height: 30px;
    margin-bottom: 1rem;
    @media (max-width: 480px) {
      font-size: 12px;
      text-align: center;
    }
  }
`;
const FutureScopeTimeline = styled.div`
  flex: 1;
  position: relative;
  padding-left: 40px;
`;
const FutureScopeStep = styled(motion.div)`
  position: relative;
  margin-bottom: 2rem;
  padding-left: 20px;
  text-align: left;
`;
const FutureScopeStepIcon = styled.div`
  position: absolute;
  left: -10px;
  top: 0;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #004e92;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
`;
const FutureScopeStepContent = styled.div`
  margin-left: 30px;
  h3 {
    font-family: ${({ theme }) => theme.typography.title};

    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    @media (max-width: 480px) {
      font-size: 1rem;
    }
  }
  p {
    font-family: ${({ theme }) => theme.typography.title};
    line-height: 25px;
    font-size: 16px;
    margin-bottom: 1rem;
    @media (max-width: 480px) {
      font-size: 12px;
    }
  }
`;

// ----------------- How It Works Section -----------------
const HowItWorksSection = styled.section`
  padding: 6rem 2rem;
  background-color: #111827;
  color: #fff;
  @media (min-width: 1200px) {
    padding: 10rem 2rem;
  }
  @media (max-width: 480px) {
    padding: 4rem 0;
  }
`;
const HowItWorksWrapper = styled.div`
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
`;
const HowItWorksTitle = styled(motion.h2)`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 2.5rem;
  margin-bottom: 1rem;
  @media (min-width: 1200px) {
    font-size: 3rem;
    margin-bottom: 1rem;
  }
  @media (max-width: 480px) {
    font-size: 2rem;
  }
      /* Gradient background */
  background: linear-gradient(270deg, #ff0080, #ff8c00, #40e0d0, #ff0080);
  background-size: 600% 600%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  
  /* Animate the gradient */
  animation: gradientFlow 8s ease infinite;

@keyframes gradientFlow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
`;
const HowItWorksDescription = styled(motion.p)`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 16px;
  width: 100%;
  margin: auto;
  line-height: 25px;
  @media (min-width: 1200px) {
    width: 60%;
    line-height: 25px;
  }
  @media (max-width: 480px) {
    font-size: 12px;
    width: 100%;
    line-height: 22px;
  }
`;
const StepsContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 50px;
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;
const StepCard = styled(motion.div)`
  background: #1f2937;
  color: #fff;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  flex: 1;
  max-width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
`;
const StepIcon = styled.img`
  height: 100px;
  width: 100px;
  border-radius: 50%;
  margin-bottom: 20px;
`;
const StepTitle = styled.h3`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 1.5rem;
  margin-bottom: 1rem;
`;
const StepDescription = styled.p`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 14px;
  line-height: 1.6;
  @media (max-width: 768px) {
    font-size: 10px;
  }
`;
const ArrowConnector = styled(motion.span)`
  font-size: 2rem;
  margin: 0 1rem;
  @media (max-width: 768px) {
    transform: rotate(90deg);
    margin: 1rem 0;
  }
`;

// ----------------- Agents Section -----------------
const AgentsSection = styled.section`
  padding: 4rem 2rem;
  background: black;
  color: ${({ theme }) => theme.colors.text.primary};
  @media (min-width: 1200px) {
    padding: 6rem 2rem;
  }
`;
const AgentsWrapper = styled.div`
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
  color: ${({ theme }) => theme.colors.text.primary};
  @media (max-width: 480px) {
    padding: 0;
  }
  p {
    font-family: ${({ theme }) => theme.typography.title};

    font-size: 16px;
    color: ${({ theme }) => theme.colors.text.primary};
    width: 60%;
    margin: auto;
    margin-bottom: 4rem;
    line-height:25px;
    @media (max-width: 480px) {
      font-size: 12px;
      width: 100%;
    }
  }
`;
const AgentsTitle = styled(motion.h2)`
  font-family: ${({ theme }) => theme.typography.title};

  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: ${({ theme }) => theme.colors.text.primary};
  @media (min-width: 1200px) {
    font-size: 3rem;
  }
  @media (max-width: 480px) {
    font-size: 2rem;
  }

  /* Gradient background */
  background: linear-gradient(270deg, #ff0080, #ff8c00, #40e0d0, #ff0080);
  background-size: 600% 600%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  
  /* Animate the gradient */
  animation: gradientFlow 8s ease infinite;

@keyframes gradientFlow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

`;
const AgentsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

// ----------------- Dummy Data & Home Component -----------------
const dummyAgents: Agent[] = [
  {
    id: 1,
    name: "💋 Luna – Your Naughty Step-Sister",
    images: ["/assets/comedy.png", "/assets/comedy.png", "/assets/comedy.png"],
    description: "Playful, seductive, and always ready to tease you in the most delicious ways 😈",
  },
  {
    id: 2,
    name: "🔥 Elena – Your Seductive Teacher",
    images: ["/assets/story.png", "/assets/story.png", "/assets/story.png"],
    description: "Intelligent, authoritative, and knows exactly how to make you her obedient student 💦",
  },
  {
    id: 3,
    name: "😈 Sophia – Your Naughty Babysitter",
    images: [
      "/assets/intellactual.png",
      "/assets/intellactual.png",
      "/assets/intellactual.png",
    ],
    description: "Sweet, caring, but with a secret wild side that will drive you absolutely crazy 🍑",
  },
  {
    id: 4,
    name: "💦 Victoria – Your Seductive Boss",
    images: ["/assets/trend.png", "/assets/trend.png", "/assets/trend.png"],
    description: "Powerful, sophisticated, and uses her authority to make you submit to pleasure 🔥",
  },
  {
    id: 5,
    name: "🍯 Aurora – Your Naughty Roommate",
    images: [
      "/assets/empathy.png",
      "/assets/empathy.png",
      "/assets/empathy.png",
    ],
    description: "Flirtatious, playful, and creates intimate moments when you're alone together 💋",
  },
  {
    id: 6,
    name: "💋 Jasmine – Your Seductive Therapist",
    images: [
      "/assets/maverik.png",
      "/assets/maverik.png",
      "/assets/maverik.png",
    ],
    description: "Professional, caring, and knows exactly how to help you release all your tension 😍",
  },
];

const futureScopeSteps = [
  {
    title: "36 Seductive Companions",
    description:
      "Choose from carefully crafted AI personalities, each with unique desires and conversation styles that will drive you wild.",
    icon: "💋",
  },
  {
    title: "Forbidden Fantasies",
    description:
      "Explore taboo scenarios with step-sisters, teachers, bosses, and neighbors who know exactly how to please you.",
    icon: "🔥",
  },
  {
    title: "Stress Relief & Pleasure",
    description:
      "Let sensual therapists, erotic masseuses, and tantric yoga teachers help you release tension in the most satisfying ways.",
    icon: "😈",
  },
  {
    title: "Supernatural Seduction",
    description:
      "Indulge in otherworldly pleasure with vampires, fallen angels, demons, and goddesses who exist only for your satisfaction.",
    icon: "🌙",
  },
];

const Home: React.FC = () => {

  const router = useRouter();
  const handleClick = () => {
    router.push("/category");
  };

  const categories: Category[] = [
    { name: "💋 Forbidden Desires", image: "assets/avatar2.png" },
    { name: "🔥 Dirty Talk Queens", image: "assets/avatar2.png" },
    { name: "😈 Stress Relief Goddesses", image: "assets/avatar2.png" },
    { name: "🌙 Your Wildest Dreams", image: "assets/avatar2.png" },
    { name: "💦 Secret Confessions", image: "assets/avatar2.png" },
    { name: "🍑 Playful Temptresses", image: "assets/avatar2.png" },
  ];

  const steps = [
    {
      title: "Choose a Category",
      description:
        "Browse our diverse categories and select the one that sparks your interest.",
      icon: "assets/search.jpg",
    },
    {
      title: "Select an Agent",
      description:
        "Meet our initial line-up of six distinct AI agents (3 men and 3 women), each with unique traits such as 'Funny', 'Storyteller', 'Exotic', 'Enthusiast', etc.",
      icon: "assets/story.png",
    },
    {
      title: "Engage in Conversation",
      description:
        "Click on your chosen agent to view the latest topics and start a live conversation using our real-time communication kit.",
      icon: "assets/bubble.jpg",
    },
  ];


  return (
    <>
      <Navbar />
      {/* Hero Section */}
      <HeroSection>
        <Background>
          <Image
            src="/assets/back2.jpg"
            alt="Background"
            fill
            style={{ objectFit: "cover" }}
            priority
          />
          <Overlay />
        </Background>
        <Content>
          <HeroTitle
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            🔥 Pleasure Palace
          </HeroTitle>
          <HeroSubtitle
            initial={{ opacity: 0, y: -30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.2 }}
          >
            Where Your Fantasies Come to Life
          </HeroSubtitle>
          <HeroTagline
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.4 }}
          >
            36 irresistible AI companions waiting to fulfill your every desire... Experience the most addictive, intimate conversations that will leave you craving more 💋
          </HeroTagline>
          <CTAButton
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
      onClick={handleClick}

          >
            🔥 Enter Paradise
            <Arrow
              initial="rest"
              whileHover={{ x: 5 }}
              animate="rest"
              variants={{ hover: { x: 5 }, rest: { x: 0 } }}
            >
              →
            </Arrow>
          </CTAButton>
        </Content>
      </HeroSection>

      {/* Product Overview Section */}
      <ProductOverviewSection>
        <OverviewWrapper>
          <OverviewContainer>
            <OverviewText
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.8 }}
            >
              <OverviewTitle
                initial={{ opacity: 0, y: -20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: 0.8 }}
              >
                💋 Your Ultimate Pleasure Experience
              </OverviewTitle>
              <p>
                Live Room is a revolutionary platform designed to make
                conversation spontaneous and engaging. When you visit our site,
                you are greeted by an array of predefined categories—ranging
                from Science 🔬, Fun 😄, Physics ⚛️, Tech News 💻, AI News 🤖,
                Arts 🎨, Cartoons 🎭, Stories 📖, Latest News 📰, World 🌍, and
                Discovery 🔍. Simply click or search to dive into discussions
                with our AI agents, each meticulously crafted to bring unique
                personalities to your chats.
              </p>
            </OverviewText>
            <OverviewGallery
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              {categories.slice(0, 6).map((cat) => (
                <CategoryCard key={cat.name} category={cat} />
              ))}
            </OverviewGallery>
          </OverviewContainer>
        </OverviewWrapper>
      </ProductOverviewSection>

      {/* How It Works Section */}
      <HowItWorksSection>
        <HowItWorksWrapper>
          <HowItWorksTitle
            initial={{ opacity: 0, y: -20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.3 }}
          >
            How It Works
          </HowItWorksTitle>
          <HowItWorksDescription>
            Browse our diverse categories, select your ideal AI agent with
            distinct traits, and dive into a dynamic, real-time conversation on
            trending topics. In just three simple steps—choose a category, pick
            an agent, and start chatting—Live Room brings your discussions to
            life instantly.
          </HowItWorksDescription>
          <StepsContainer>
            {steps.map((step, index) => (
              <React.Fragment key={step.title}>
                <StepCard
                  whileHover={{
                    scale: 1.1,
                    boxShadow: "0px 10px 30px rgba(0,0,0,0.5)",
                  }}
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.2 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <StepIcon src={step.icon} />
                  <StepTitle>{step.title}</StepTitle>
                  <StepDescription>{step.description}</StepDescription>
                </StepCard>
                {index < steps.length - 1 && (
                  <ArrowConnector
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true, amount: 0.2 }}
                    transition={{ duration: 0.5, delay: index * 0.2 + 0.5 }}
                  >
                    →
                  </ArrowConnector>
                )}
              </React.Fragment>
            ))}
          </StepsContainer>
        </HowItWorksWrapper>
      </HowItWorksSection>

      {/* Agents Section */}
      <AgentsSection>
        <AgentsWrapper>
          <AgentsTitle
            initial={{ opacity: 0, y: -20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.8 }}
          >
            🔥 Meet Your Irresistible Companions
          </AgentsTitle>
          <p>
            We believe conversation is an art – and our agents are the masters.
            Here are our top six agent personalities designed to ensure every
            conversation is memorable:
          </p>
          <AgentsGrid>
            {dummyAgents.map((agent, index) => {
              const agentGradient = gradients[index % gradients.length];
              return (
                <motion.div
                  key={agent.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true, amount: 0.2 }}
                  transition={{ duration: 0.8, delay: index * 0.2 }}
                >
                  <AgentCardSmall {...agent} gradient={agentGradient} />
                </motion.div>
              );
            })}
          </AgentsGrid>
        </AgentsWrapper>
      </AgentsSection>

      {/* Your Personal Pleasure Palace Section */}
      <FutureScopeSection>
        <FutureScopeWrapper>
          <FutureScopeText>
            <h2>🔥 Your Personal Pleasure Palace</h2>
            <p>
              Step into a world where your deepest fantasies come alive through intimate AI companions. With 36 irresistible personalities across 6 seductive categories, each conversation is designed to fulfill your desires and leave you craving more. From naughty step-sisters to dominant bosses, sensual therapists to exotic dancers - your perfect companion is waiting to seduce you into the most addictive conversations you've ever experienced. 💋
            </p>
          </FutureScopeText>
          <FutureScopeTimeline>
            {futureScopeSteps.map((step, index) => (
              <FutureScopeStep
                key={step.title}
                initial={{ opacity: 0, x: 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: 0.8, delay: index * 0.3 }}
              >
                <FutureScopeStepIcon>{step.icon}</FutureScopeStepIcon>
                <FutureScopeStepContent>
                  <h3>{step.title}</h3>
                  <p>{step.description}</p>
                </FutureScopeStepContent>
              </FutureScopeStep>
            ))}
          </FutureScopeTimeline>
        </FutureScopeWrapper>
      </FutureScopeSection>
    </>
  );
};

export default Home;
