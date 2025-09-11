// src/styles/styled.d.ts
import 'styled-components';

declare module 'styled-components' {
  export interface DefaultTheme {
    colors: {
      background: string;
      background2: string;
      header: string;
      footer: string;
      primary: string;
      primaryHover: string;
      primaryLight: string;
      primaryDark: string;
      text: {
        primary: string;
        secondary: string;
      };
      surface: {
        primary: string;
        secondary: string;
      };
      social: {
        twitter: string;
        facebook: string;
        instagram: string;
      };
      box: {
        primary: string;
        secondary: string;
      };
    };
    shadows: {
      sm: string;
      md: string;
      lg: string;
    };
    transitions: {
      fast: string;
      normal: string;
      slow: string;
    };
    breakpoints: {
      sm: string;
      md: string;
      lg: string;
      xl: string;
    };
    typography: {
      heading: string;
      body: string;
      logo: string;

      title:string;
      para:string;
      light:string;
      poky:string;
    };
  }
}