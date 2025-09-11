"use client";
import styled from "styled-components";
import Link from "next/link";
import React, { useState, useCallback } from "react";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { toggleTheme } from "@/store/features/themeSlice";
import { usePathname } from "next/navigation";
// import Image from 'next/image';
// import Logo from '../../public/assets/logo2.png';

const NavContainer = styled.div`
  width: 100%;
  z-index: 1000;
  background-color: ${({ theme }) => theme.colors.background};
`;

const Header = styled.header`
  background-color: ${({ theme }) => theme.colors.background};
  margin: 0 auto;
  padding: 0.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 80px;
  position: fixed;
  z-index: 100;
  width: 100%;
`;

const LogoContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  cursor: pointer;
`;

const LogoImage = styled.div`
  font-family: ${({ theme }) => theme.typography.title};
  font-size: 1.5rem;
  color: ${({ theme }) => theme.colors.text.primary};
  letter-spacing: 1px;
`;

const LogoTagline = styled.div`
  font-size: 10px;
  color: ${({ theme }) => theme.colors.text.secondary};
  font-style: italic;
  font-weight: bold;
  margin-top: 0.25rem;
  font-family: ${({ theme }) => theme.typography.title};
  max-width: 400px;
`;

const NavLinks = styled.nav`
  display: flex;
  gap: 2.5rem;
  align-items: center;
  margin-left: auto;

  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    display: none;
  }
`;

const NavLink = styled(Link)<{ $isActive?: boolean }>`
  font-family: ${({ theme }) => theme.typography.title};
  color: ${({ theme, $isActive }) =>
    $isActive ? theme.colors.text.primary : theme.colors.primary};
  text-decoration: none;
  font-size: 1rem;
  position: relative;
  transition: color ${({ theme }) => theme.transitions.fast};

  &:hover {
    color: ${({ theme }) => theme.colors.primary};
  }
`;

const ThemeToggle = styled.button`
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: ${({ theme }) => theme.colors.text.primary};
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color ${({ theme }) => theme.transitions.fast};
  margin-left: 1.5rem;

  &:hover {
    color: ${({ theme }) => theme.colors.primary};
  }
`;

const NavGroup = styled.div`
  display: flex;
  align-items: center;
`;

const MobileMenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  color: ${({ theme }) => theme.colors.text.primary};

  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    display: flex;
    align-items: center;
    justify-content: center;
  }
`;

const MobileMenu = styled.nav<{ $isOpen: boolean }>`
  display: none;

  @media (max-width: ${({ theme }) => theme.breakpoints.md}) {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 15%;
    left: 0;
    right: 0;
    z-index: 999;
    background-color: ${({ theme }) => theme.colors.surface.primary};
    padding: 1rem;
    transform: ${({ $isOpen }) =>
      $isOpen ? "translateY(0)" : "translateY(-100%)"};
    opacity: ${({ $isOpen }) => ($isOpen ? 1 : 0)};
    visibility: ${({ $isOpen }) => ($isOpen ? "visible" : "hidden")};
    transition: all ${({ theme }) => theme.transitions.normal};
    box-shadow: ${({ theme }) => theme.shadows.lg};
  }
`;

const MobileNavLink = styled(NavLink)`
  padding: 1rem;
  width: 100%;
  text-align: center;
`;

const Navbar: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const dispatch = useAppDispatch();
  const isDarkTheme = useAppSelector((state) => state.theme.isDarkTheme);
  const pathname = usePathname();

  const toggleMobileMenu = useCallback(() => {
    setIsMobileMenuOpen((prev) => !prev);
  }, []);

  const handleThemeToggle = () => {
    dispatch(toggleTheme());
  };

  return (
    <NavContainer>
      <Header>
        <LogoContainer>
          <Link href="/" passHref>
            <LogoImage>🔥 Pleasure Palace</LogoImage>
            <LogoTagline>where fantasies come alive 💋</LogoTagline>
          </Link>
          {/* <Image src={Logo} alt="SmartSiksha" height={100}/> */}
        </LogoContainer>

        <NavGroup>
          <NavLinks>
            <NavLink href="/" $isActive={pathname === "/"}>
              Home
            </NavLink>
            <NavLink href="/category" $isActive={pathname === "/category"}>
              🔥 Temptations
            </NavLink>

            {/* <NavLink href="/contact" $isActive={pathname === '/contact'}>
              Contact Us
            </NavLink> */}
          </NavLinks>

          <ThemeToggle onClick={handleThemeToggle} aria-label="Toggle theme">
            {isDarkTheme ? (
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="5" />
                <line x1="12" y1="1" x2="12" y2="3" />
                <line x1="12" y1="21" x2="12" y2="23" />
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
                <line x1="1" y1="12" x2="3" y2="12" />
                <line x1="21" y1="12" x2="23" y2="12" />
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
              </svg>
            ) : (
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
              </svg>
            )}
          </ThemeToggle>

          <MobileMenuButton
            onClick={toggleMobileMenu}
            aria-label="Toggle mobile menu"
            aria-expanded={isMobileMenuOpen}
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              {isMobileMenuOpen ? (
                <>
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </>
              ) : (
                <>
                  <line x1="3" y1="12" x2="21" y2="12" />
                  <line x1="3" y1="6" x2="21" y2="6" />
                  <line x1="3" y1="18" x2="21" y2="18" />
                </>
              )}
            </svg>
          </MobileMenuButton>
        </NavGroup>

        <MobileMenu $isOpen={isMobileMenuOpen}>
          <MobileNavLink
            href="/"
            $isActive={pathname === "/"}
            onClick={toggleMobileMenu}
          >
            Home
          </MobileNavLink>
          <MobileNavLink
            href="/category"
            $isActive={pathname === "/category"}
            onClick={toggleMobileMenu}
          >
            🔥 Temptations
          </MobileNavLink>

          {/* <MobileNavLink href="/about" $isActive={pathname === '/about'} onClick={toggleMobileMenu}>
            About Us
          </MobileNavLink>
          <MobileNavLink href="/contact" $isActive={pathname === '/contact'} onClick={toggleMobileMenu}>
            Contact Us
          </MobileNavLink> */}
        </MobileMenu>
      </Header>
    </NavContainer>
  );
};

export default Navbar;
