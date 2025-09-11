import React, { useEffect, useRef, useState } from 'react';
import styled from 'styled-components';

interface VideoPlayerProps {
  src: string;
  autoPlay?: boolean;
  loop?: boolean;
  muted?: boolean;
  playsInline?: boolean;
}

const StyledVideo = styled.video`
  width: 100%;
  height: 100%;
  object-fit: cover;
`;

const VideoOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.2);
  opacity: 0;
  transition: opacity 0.3s ease;
`;

const ControlButton = styled.button<{ $isPaused: boolean }>`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s ease, opacity 0.3s ease;
  opacity: 0;

  &:hover {
    transform: scale(1.1);
    background: white;
  }

  &::before {
    content: '';
    width: 0;
    height: 0;
    display: block;
    ${({ $isPaused }) =>
      $isPaused
        ? `
      border-style: solid;
      border-width: 15px 0 15px 25px;
      border-color: transparent transparent transparent #000;
      margin-left: 5px;
    `
        : `
      width: 20px;
      height: 25px;
      border-left: 8px solid #000;
      border-right: 8px solid #000;
      margin: 0;
    `}
  }
`;

const VideoWrapper = styled.div`
  position: relative;
  width: 100%;
  height: 100%;

  &:hover ${VideoOverlay} {
    opacity: 1;
  }

  &:hover ${ControlButton} {
    opacity: 1;
  }
`;

const VideoPlayer: React.FC<VideoPlayerProps> = ({
  src,
  autoPlay = true,
  loop = true,
  muted = true,
  playsInline = true,
}) => {
  const [isClient, setIsClient] = useState(false);
  const [isPaused, setIsPaused] = useState(!autoPlay);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    setIsClient(true);
  }, []);

  const togglePlayPause = () => {
    if (videoRef.current) {
      if (videoRef.current.paused) {
        videoRef.current.play();
        setIsPaused(false);
      } else {
        videoRef.current.pause();
        setIsPaused(true);
      }
    }
  };

  if (!isClient) {
    return <div style={{ width: '100%', height: '100%', background: '#f0f0f0' }} />;
  }

  return (
    <VideoWrapper>
      <StyledVideo
        ref={videoRef}
        src={src}
        autoPlay={autoPlay}
        loop={loop}
        muted={muted}
        playsInline={playsInline}
      />
      <VideoOverlay>
        <ControlButton
          onClick={togglePlayPause}
          $isPaused={isPaused}
          aria-label={isPaused ? "Play video" : "Pause video"}
        />
      </VideoOverlay>
    </VideoWrapper>
  );
};

export default VideoPlayer;