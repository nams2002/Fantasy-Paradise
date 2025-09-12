"use client";
import React, { useEffect, useState } from "react";
import styled, { keyframes } from "styled-components";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import Navbar from "@/component/Navbar";

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

// Define the data structure
interface Category {
  id: number;
  name: string;
  description: string;
  image_url?: string;
  is_active: boolean;
}

interface Subcategory {
  id: number;
  name: string;
  description: string;
  image_url?: string;
  is_active: boolean;
  category_id: number;
  sort_order: number;
}

interface DisplayCategory {
  id: number;
  name: string;
  image: string;
}

// API Functions

const fetchSubcategories = async (): Promise<Subcategory[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/subcategories/`);
    if (!response.ok) throw new Error('Failed to fetch subcategories');
    return await response.json();
  } catch (error) {
    console.error('Error fetching subcategories:', error);
    return [];
  }
};

// Array of gradient strings to choose from
const gradients = [
  "linear-gradient(45deg, #ff00ff, #00ffff, #ffcc00, #ff00ff)",
  "linear-gradient(45deg, #ff1493, #ff69b4, #ff6347, #ff1493)",
  "linear-gradient(45deg, #ff9900, #33ccff, #ff66cc, #ff9900)",
  "linear-gradient(45deg, #66ff66, #ff6666, #6666ff, #66ff66)",
  "linear-gradient(45deg, #ffcc00, #00ccff, #ff33cc, #ffcc00)",
  "linear-gradient(45deg, #00ffff, #ff00ff, #ccff00, #00ffff)",
];

// Subcategory name mappings for display - TEMPTING & PROVOCATIVE
const subcategoryDisplayNames: { [key: string]: string } = {
  // Romantic Companions
  "step_sisters": "😈 Naughty Step-Sisters",
  "teachers": "🔥 Seductive Teachers",
  "roommates": "💦 Intimate Roommates",
  "bosses": "💋 Dominant Bosses",
  "neighbors": "🍑 Flirty Neighbors",
  "ex_lovers": "🔥 Irresistible Ex-Lovers",

  // Flirty Chat
  "phone_sex": "📞 Phone Sex Operators",
  "cam_girls": "📹 Webcam Performers",
  "sexting": "💬 Sexting Specialists",
  "voice_actors": "🎭 Erotic Voice Artists",
  "chat_hosts": "💋 Chat Room Hosts",
  "flirt_coaches": "😘 Flirtation Coaches",

  // Mood Boosters
  "therapists": "🛋️ Sensual Therapists",
  "masseuses": "💆 Erotic Masseuses",
  "yoga_instructors": "🧘 Tantric Yoga Teachers",
  "life_coaches": "✨ Motivational Goddesses",
  "meditation_guides": "🕯️ Mindfulness Mistresses",
  "wellness_experts": "🌿 Holistic Healers",

  // Fantasy Roleplay
  "vampires": "🧛‍♀️ Seductive Vampires",
  "angels": "👼 Fallen Angels",
  "demons": "😈 Tempting Demons",
  "witches": "🔮 Enchanting Witches",
  "goddesses": "⚡ Divine Goddesses",
  "aliens": "👽 Exotic Aliens",

  // Intimate Conversations
  "confessors": "🤫 Secret Keepers",
  "counselors": "💭 Intimate Counselors",
  "best_friends": "👯 Naughty Best Friends",
  "diary_keepers": "📔 Personal Diary Holders",
  "soul_mates": "💕 Destined Soul Mates",
  "pen_pals": "✉️ Erotic Pen Pals",

  // Entertainment & Fun
  "comedians": "😂 Naughty Comedians",
  "dancers": "💃 Exotic Dancers",
  "singers": "🎤 Sultry Singers",
  "gamers": "🎮 Gamer Girls",
  "artists": "🎨 Erotic Artists",
  "party_hosts": "🎉 Party Goddesses"
};

// Convert API subcategories to display format
const convertToDisplayCategories = (apiSubcategories: Subcategory[]): DisplayCategory[] => {
  return apiSubcategories.map(subcat => ({
    id: subcat.id,
    name: subcategoryDisplayNames[subcat.name] || subcat.description,
    image: subcat.image_url || "/assets/avatar1.png"
  }));
};

// Keyframes for shimmer (for image loading) and gradient animation
const shimmerAnimation = keyframes`
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
`;

const gradientFlow = keyframes`
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
`;

// Styled Components

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

const SearchBarContainer = styled.div`
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
`;

const SearchInput = styled.input`
  background-color: ${(props) => props.theme.colors.background};
  color: ${({ theme }) => theme.colors.text.primary};
  font-family: ${({ theme }) => theme.typography.title};
  width: 100%;
  max-width: 700px;
  padding: 18px 15px;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
  &:hover,
  &:focus {
    outline: none;
    border-color: #aaa;
  }
`;

const MotionSearchInput = motion(SearchInput);

const searchVariants = {
  focus: { scale: 1.05, boxShadow: "0 4px 16px rgba(0, 0, 0, 0.2)" },
  blur: { scale: 1, boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)" },
};

const SectionWrapper = styled.div`
  margin-bottom: 60px;
`;

const SectionHeading = styled.h2`
  font-family: ${({ theme }) => theme.typography.title};

  color: ${({ theme }) => theme.colors.text.primary};
  margin: 20px 0 5px 0;
  font-size: 1.75rem;
  text-align: left;
  @media (max-width: 1024px) {
    font-size: 1.5rem;
  }
  @media (max-width: 768px) {
    font-size: 1.5rem;
  }
`;

const SectionDescription = styled.p`
  font-family: ${({ theme }) => theme.typography.title};

  color: ${({ theme }) => theme.colors.text.primary};
  margin: 5px 0 30px 0;
  font-size: 0.8rem;
  text-align: left;
  @media (max-width: 1024px) {
    font-size: 0.7rem;
  }
  @media (max-width: 768px) {
    font-size: 0.7rem;
    line-height:18px;
  }
`;

const GridContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  @media (max-width: 1024px) {
    grid-template-columns: repeat(3, 1fr);
  }
  @media (max-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }
  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
`;

// Updated Card component with animated gradient background.
const Card = styled(motion.div)<{ gradient: string }>`
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow 0.3s ease;
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.4), 0 0 10px rgba(0, 255, 255, 0.4);

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
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
  position: relative;
  z-index: 1;
  color: white;
`;

// Framer Motion variants for card hover/tap effects
const cardVariants = {
  hover: { scale: 1.05 },
  tap: { scale: 0.95 },
};

// CategoryCard component with fade-in animation on load.
// Updated the image style to use opacity rather than display to ensure the image is visible once loaded.
const CategoryCard: React.FC<{ category: DisplayCategory }> = ({ category }) => {
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const randomGradient =
    gradients[Math.floor(Math.random() * gradients.length)];

  const handleCardClick = () => {
    if (typeof window !== "undefined") {
      localStorage.setItem("selectedSubcategoryId", category.id.toString());
      localStorage.setItem("selectedSubcategoryName", category.name);
    }
    router.push("/agents");
  };

  return (
    <Card
      onClick={handleCardClick}
      variants={cardVariants}
      whileHover="hover"
      whileTap="tap"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      gradient={randomGradient}
    >
      <ImageContainer>
        {isLoading && <Shimmer />}
        <img
          src={category.image}
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

interface SectionProps {
  heading: string;
  description: string;
  items: DisplayCategory[];
}

const Section: React.FC<SectionProps> = ({ heading, description, items }) => {
  return (
    <SectionWrapper>
      <SectionHeading>{heading}</SectionHeading>
      <SectionDescription>{description}</SectionDescription>
      <GridContainer>
        {items.map((item) => (
          <CategoryCard key={item.id} category={item} />
        ))}
      </GridContainer>
    </SectionWrapper>
  );
};

const Category: React.FC = () => {
  const [categories, setCategories] = useState<DisplayCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [isSearchFocused, setIsSearchFocused] = useState(false);

  useEffect(() => {
    window.scrollTo(0, 0);

    const loadCategories = async () => {
      setLoading(true);
      try {
        const apiSubcategories = await fetchSubcategories();
        const displayCategories = convertToDisplayCategories(apiSubcategories.filter(subcat => subcat.is_active));
        setCategories(displayCategories);
      } catch (error) {
        console.error('Error loading subcategories:', error);
      } finally {
        setLoading(false);
      }
    };

    loadCategories();
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
            <p style={{ color: 'white' }}>Preparing your naughty temptations... They&apos;re getting ready to seduce you 😈💋</p>
          </div>
        </PageContainer>
      </div>
    );
  }

  // Split subcategories into groups for display (6 subcategories per section)
  const forbiddenDesires = categories.slice(0, 6);      // Romantic companions subcategories
  const dirtyTalkQueens = categories.slice(6, 12);      // Flirty chat subcategories
  const stressReliefGoddesses = categories.slice(12, 18); // Mood boosters subcategories
  const wildestDreams = categories.slice(18, 24);       // Fantasy roleplay subcategories
  const secretConfessions = categories.slice(24, 30);   // Intimate conversations subcategories
  const playfulTemptresses = categories.slice(30, 36);  // Entertainment & fun subcategories

  return (
    <div>
      <Navbar />
      <PageContainer>
        <SearchBarContainer>
          <MotionSearchInput
            placeholder="Find your naughty fantasy... 😈"
            onFocus={() => setIsSearchFocused(true)}
            onBlur={() => setIsSearchFocused(false)}
            animate={isSearchFocused ? "focus" : "blur"}
            variants={searchVariants}
            whileHover={{ scale: 1.03 }}
            initial="blur"
          />
        </SearchBarContainer>
        {forbiddenDesires.length > 0 && (
          <Section
            heading="💋 Forbidden Desires"
            description="These naughty beauties are dying to please you... Choose your forbidden pleasure and let them make you feel incredible 💋"
            items={forbiddenDesires}
          />
        )}
        {dirtyTalkQueens.length > 0 && (
          <Section
            heading="🔥 Dirty Talk Queens"
            description="Masters of seductive conversation who know exactly what to say to drive you wild with desire..."
            items={dirtyTalkQueens}
          />
        )}
        {stressReliefGoddesses.length > 0 && (
          <Section
            heading="😈 Stress Relief Goddesses"
            description="Let these divine healers help you unwind and release all your tension in the most satisfying ways..."
            items={stressReliefGoddesses}
          />
        )}
        {wildestDreams.length > 0 && (
          <Section
            heading="🌙 Your Wildest Dreams"
            description="Step into your most taboo fantasies with supernatural beings who'll fulfill your deepest desires..."
            items={wildestDreams}
          />
        )}
        {secretConfessions.length > 0 && (
          <Section
            heading="💦 Secret Confessions"
            description="Share your darkest secrets with trusted confidants who'll never judge, only pleasure you more..."
            items={secretConfessions}
          />
        )}
        {playfulTemptresses.length > 0 && (
          <Section
            heading="🍑 Playful Temptresses"
            description="Fun-loving entertainers who know how to mix pleasure with play for the ultimate experience..."
            items={playfulTemptresses}
          />
        )}
      </PageContainer>
    </div>
  );
};

export default Category;
