import styled from 'styled-components';
import { FaFacebook, FaInstagram } from 'react-icons/fa';
import { FaXTwitter } from 'react-icons/fa6';


const StyledFooter = styled.footer`
  background-color: ${({ theme }) => theme.colors.footer};
  color: ${({ theme }) => theme.colors.text.secondary};
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  border-top: 1px solid ${({ theme }) => theme.colors.surface.secondary};
  margin-top: auto;
  width: 100%;
`;

const ContentWrapper = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 800px;
  min-height: 55px;
`;

const CopyrightText = styled.div`
  font-family: ${({ theme }) => theme.typography.body};
  font-size: 0.75rem;
  font-weight: bold;
`;

const SocialLinks = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const SocialIcon = styled.a`
  color: ${({ theme }) => theme.colors.text.primary};
  font-size: 1.25rem;
  transition: color ${({ theme }) => theme.transitions.fast};

  &:hover {
    color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

const Footer = () => {
  return (
    <StyledFooter>
      <ContentWrapper>
        <CopyrightText>
        © 2025 LiveRoom. All content and AI features are proprietary.
        </CopyrightText>
        
        <SocialLinks>
            <SocialIcon href="https://x.com/BrainyBotHub" target='_blank' aria-label="Twitter">
                <FaXTwitter />
            </SocialIcon>
            <SocialIcon href="https://www.facebook.com/profile.php?id=61572354395900&sk=about" target='_blank' aria-label="Facebook">
                <FaFacebook />
            </SocialIcon>
            <SocialIcon href="https://www.instagram.com/smartsiksha/" target='_blank' aria-label="Instagram">
                <FaInstagram />
            </SocialIcon>
        </SocialLinks>
      </ContentWrapper>
    </StyledFooter>
  );
};

export default Footer;