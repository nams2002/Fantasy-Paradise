"use client";
import React from "react";
import styled from "styled-components";
import { FaFacebook, FaInstagram } from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";
// import Link from 'next/link';
import Navbar from "@/component/Navbar";
import Image from "next/image";
import Footer from "@/component/Footer";

const ContactPage = () => {
  return (
    <>
      <PageContainer>
        <Navbar />
        <MainContent>
          <ContactImageContainer>
            <StyledImage
              src="/assets/contactUs.jpg"
              alt="Contact Us Banner"
              priority
              fill
            />
          </ContactImageContainer>

          <ContentBox>
            <TitleSection>
              <CompanyTitle>SmartSiksha</CompanyTitle>
              <Tagline>
                Let&apos;s Build the Future of
                <br /> Learning, Together.
              </Tagline>
              <Divider />
            </TitleSection>

            <DescriptionSection>
              <Description>
                At SmartSiksha, we&apos;re on a mission to revolutionize
                education by putting the power of AI-driven tutoring into the
                hands of students, teachers, and lifelong learners. Today, our
                platform lets you create custom AI tutors trained on your unique
                study materials, with personalities that adapt to your learning
                style—whether you need a funny science companion or a
                no-nonsense exam coach. But this is just the beginning. In the
                coming months, we&apos;ll launch voice-enabled learning,
                teacher-led AI avatars, and a global marketplace where educators
                can share their expertise with students worldwide.
              </Description>
            </DescriptionSection>
          </ContentBox>

          <ContactSection>
            <ContactContainer>
              <ContactGroup>
                <ContactLabel>Call</ContactLabel>
                <ContactInfo>+917895744872</ContactInfo>
              </ContactGroup>

              <ContactGroup>
                <ContactLabel>Email</ContactLabel>
                <ContactInfo>brainybothub@gmail.com</ContactInfo>
              </ContactGroup>

              <ContactGroup>
                <ContactLabel>Follow</ContactLabel>
                <SocialLinks>
                  <SocialIcon
                    href="https://x.com/BrainyBotHub"
                    aria-label="Twitter"
                    target="_blank"
                  >
                    <FaXTwitter />
                  </SocialIcon>
                  <SocialIcon
                    href="https://www.facebook.com/profile.php?id=61572354395900&sk=about"
                    aria-label="Facebook"
                    target="_blank"
                  >
                    <FaFacebook />
                  </SocialIcon>
                  <SocialIcon
                    href="https://www.instagram.com/smartsiksha/"
                    aria-label="Instagram"
                    target="_blank"
                  >
                    <FaInstagram />
                  </SocialIcon>
                </SocialLinks>
              </ContactGroup>
            </ContactContainer>
          </ContactSection>
        </MainContent>
      </PageContainer>
      <Footer />
    </>
  );
};

export default ContactPage;

const PageContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: ${({ theme }) => theme.colors.background};
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
`;

const ContactImageContainer = styled.div`
  position: relative;
  width: 80%;
  height: 70vh;
  margin-top: 10px;

  @media (max-width: ${({ theme }) => theme.breakpoints.lg}) {
    height: 50vh;
  }

  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    height: 30vh;
    min-height: 270px;
    object-fit: fill;
  }
`;

const StyledImage = styled(Image)`
  object-fit: cover;
  object-position: center;
`;

const ContentBox = styled.div`
  display: flex;
  background-color: ${({ theme }) => theme.colors.background2};
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;
  padding: 6rem 12rem;
  width: 80%;
  margin: 0 auto;
  margin-bottom: 40px;

  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    padding: 25px;
    width: 100%;
    flex-direction: column;
  }
`;

const TitleSection = styled.div`
  flex: 0 0 auto;
  max-width: 400px;
`;

const CompanyTitle = styled.h1`
  font-family: ${({ theme }) => theme.typography.heading};
  font-size: 2.5rem;
  color: ${({ theme }) => theme.colors.text.primary};
  margin: 0;
  font-weight: 500;
  line-height: 1.2;
`;

const Tagline = styled.h2`
  font-family: ${({ theme }) => theme.typography.heading};
  font-size: 2.5rem;
  color: ${({ theme }) => theme.colors.text.primary};
  margin: 0rem 0;
  font-weight: 500;
  line-height: 1.2;
`;

const Divider = styled.hr`
  width: 40px;
  border: none;
  border-top: 2px solid ${({ theme }) => theme.colors.text.primary};
  margin: 2rem 0;
`;

const DescriptionSection = styled.div`
  flex: 0 0 50%;
  max-width: 370px;
  margin-left: 4rem;
  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    margin-left: 0;
  }
`;

const Description = styled.p`
  font-family: ${({ theme }) => theme.typography.body};
  font-size: 1rem;
  color: ${({ theme }) => theme.colors.text.primary};
  line-height: 1.2;
  margin: 0;
  text-align: left;
  font-weight: bold;
  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    font-weight: lighter;
    line-height: 1.4;
  }
`;

const ContactSection = styled.section`
  width: 100%;
  // background-color: ${({ theme }) => theme.colors.surface.primary};
  background-color: ${({ theme }) => theme.colors.box.primary};
  padding: 4rem;
  margin-bottom: 30px;
`;

const ContactContainer = styled.div`
  display: flex;
  justify-content: space-between;
  max-width: 1000px;
  margin: 0 auto;
  padding: 2.5rem;
  background-color: ${({ theme }) => theme.colors.surface.primary};

  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    flex-direction: column;
    gap: 2rem;
    align-items: center;
  }
`;

const ContactGroup = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
`;

const ContactLabel = styled.h4`
  font-family: ${({ theme }) => theme.typography.body};
  font-size: 1rem;
  color: ${({ theme }) => theme.colors.text.primary};
  margin: 0;
  font-weight: 400;
  padding: 0.5rem 2rem;
`;

const ContactInfo = styled.p`
  font-family: ${({ theme }) => theme.typography.body};
  font-size: 1rem;
  color: ${({ theme }) => theme.colors.text.primary};
  margin: 0;
  font-weight: 600;
`;

const SocialLinks = styled.div`
  display: flex;
  gap: 1rem;
`;

const SocialIcon = styled.a`
  color: ${({ theme }) => theme.colors.text.primary};
  font-size: 1.25rem;
  transition: color ${({ theme }) => theme.transitions.fast};

  &:hover {
    color: ${({ theme }) => theme.colors.primaryHover};
  }
`;
