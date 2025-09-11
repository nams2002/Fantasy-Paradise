'use client';

import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';

// Enhanced Animations
const slideUp = keyframes`
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
`;

// const pulse = keyframes`
//   0% { transform: scale(1); }
//   50% { transform: scale(1.05); }
//   100% { transform: scale(1); }
// `;

const shimmer = keyframes`
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
`;

// Styled Components with Enhanced Effects
const Container = styled.div`
  min-height: 100vh;
  background-color: ${(props) => props.theme.colors.background};
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(
      circle at center,
      rgba(37, 99, 235, 0.1) 0%,
      rgba(37, 99, 235, 0) 70%
    );
    z-index: 0;
  }
`;

const ContentWrapper = styled.div`
  position: relative;
  max-width: 440px;
  width: 100%;
  padding: 3.5rem;
  background: ${(props) => props.theme.colors.surface.primary};
  border-radius: 2rem;
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  animation: ${slideUp} 1s cubic-bezier(0.16, 1, 0.3, 1);
  backdrop-filter: blur(10px);

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 2rem;
    padding: 2px;
    background: linear-gradient(
      45deg,
      rgba(37, 99, 235, 0.5),
      rgba(59, 130, 246, 0.5)
    );
    -webkit-mask: linear-gradient(#fff 0 0) content-box,
                 linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box,
          linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
  }
`;

const Title = styled.h1`
  color: ${(props) => props.theme.colors.text.primary};
  font-size: 2.75rem;
  text-align: center;
  font-weight: 800;
  margin-bottom: 2.5rem;
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 50%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: -0.75rem;
    left: 50%;
    transform: translateX(-50%);
    width: 50px;
    height: 4px;
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    border-radius: 2px;
  }
`;

const ButtonsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 2rem;
`;

interface SocialButtonProps {
  $provider: 'google' | 'facebook';
  $isHovered?: boolean;
}

const SocialButton = styled.button<SocialButtonProps>`
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  width: 100%;
  padding: 1.25rem 1.75rem;
  border-radius: 1.25rem;
  border: none;
  font-size: 1.1rem;
  font-weight: 600;
  background: ${(props) =>
    props.$provider === 'google'
      ? 'linear-gradient(135deg, #ffffff, #f0f0f0)'
      : 'linear-gradient(135deg, #1877f2, #145dbb)'};
  color: ${(props) =>
    props.$provider === 'google' ? '#000000' : '#ffffff'};
  box-shadow: ${(props) =>
    props.$provider === 'google'
      ? '0 5px 15px rgba(0, 0, 0, 0.1)'
      : '0 5px 15px rgba(24, 119, 242, 0.3)'};
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 200%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
    );
    animation: ${shimmer} 2s infinite;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  &:hover {
    transform: translateY(-4px);
    box-shadow: ${(props) =>
      props.$provider === 'google'
        ? '0 15px 30px rgba(0, 0, 0, 0.15)'
        : '0 15px 30px rgba(24, 119, 242, 0.4)'};

    &::before {
      opacity: 1;
    }
  }

  &:active {
    transform: translateY(-2px);
  }

  svg {
    width: 1.75rem;
    height: 1.75rem;
    fill: currentColor;
    transition: transform 0.3s ease;
  }

  &:hover svg {
    transform: scale(1.1);
  }
`;

const OrDivider = styled.div`
  display: flex;
  align-items: center;
  margin: 2rem 0;
  color: ${props => props.theme.colors.text.secondary};
  font-size: 0.9rem;

  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      ${props => props.theme.colors.text.secondary}40,
      transparent
    );
  }

  span {
    padding: 0 1rem;
    font-weight: 500;
  }
`;

export default function Login() {
  const [hoveredButton, setHoveredButton] = useState<'google' | 'facebook' | null>(null);

  const handleSocialLogin = (provider: 'google' | 'facebook') => {
    console.log(`${provider} login clicked`);
    // Add login logic here
  };

  return (
    <Container>
      <ContentWrapper>
        <Title>Welcome Back</Title>
        <ButtonsContainer>
          <SocialButton
            $provider="google"
            $isHovered={hoveredButton === 'google'}
            onClick={() => handleSocialLogin('google')}
            onMouseEnter={() => setHoveredButton('google')}
            onMouseLeave={() => setHoveredButton(null)}
          >
            <svg viewBox="0 0 24 24">
              <path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z" />
            </svg>
            Continue with Google
          </SocialButton>
          <OrDivider><span>or</span></OrDivider>
          <SocialButton
            $provider="facebook"
            $isHovered={hoveredButton === 'facebook'}
            onClick={() => handleSocialLogin('facebook')}
            onMouseEnter={() => setHoveredButton('facebook')}
            onMouseLeave={() => setHoveredButton(null)}
          >
            <svg viewBox="0 0 24 24">
              <path d="M13.397,20.997v-8.196h2.765l0.411-3.209h-3.176V7.548c0-0.926,0.258-1.56,1.587-1.56h1.684V3.127C15.849,3.039,15.025,2.997,14.201,3c-2.444,0-4.122,1.492-4.122,4.231v2.355H7.332v3.209h2.753v8.202H13.397z" />
            </svg>
            Continue with Facebook
          </SocialButton>
        </ButtonsContainer>
      </ContentWrapper>
    </Container>
  );
}