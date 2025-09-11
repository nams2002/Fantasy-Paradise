import React from 'react';
import styled, { keyframes } from 'styled-components';

const pulse = keyframes`
  0% { transform: scale(0.8); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(0.8); opacity: 0.5; }
`;

const wave = keyframes`
  0% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0); }
`;

const LoaderContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding: 2rem;
  backdrop-filter: blur(8px);
  border-radius: 16px;
`;

interface CircleProps {
  delay?: string;
}

const Circle = styled.div<CircleProps>`
  width: 12px;
  height: 12px;
  background: ${props => props.theme.colors.primary || '#0057E1'};
  border-radius: 50%;
  animation: ${pulse} 1.5s ease-in-out infinite,
             ${wave} 1.5s ease-in-out infinite;
  animation-delay: ${props => props.delay || '0s'};
  box-shadow: 0 0 20px ${props => props.theme.colors.primary || '#0057E1'}80;
`;

const AILoader = () => {
  return (
    <LoaderContainer>
      <Circle delay="0s" />
      <Circle delay="0.2s" />
      <Circle delay="0.4s" />
    </LoaderContainer>
  );
};

export default AILoader;