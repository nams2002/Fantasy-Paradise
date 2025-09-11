// app/providers.tsx
'use client';

import { ThemeProvider } from 'styled-components';
import { darkTheme, lightTheme } from '@/styles/theme';
import StyledComponentsRegistry from '@/lib/registry';
import { Provider } from 'react-redux';
import { store } from '@/store/store';
import { useAppSelector } from '@/store/hooks';

// Create a separate component for theme handling
const ThemeProviderWrapper = ({ children }: { children: React.ReactNode }) => {
  const isDarkTheme = useAppSelector((state) => state.theme.isDarkTheme);
  
  return (
    <ThemeProvider theme={isDarkTheme ? darkTheme : lightTheme}>
      {children}
    </ThemeProvider>
  );
};

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <Provider store={store}>
      <StyledComponentsRegistry>
        <ThemeProviderWrapper>
          {children}
        </ThemeProviderWrapper>
      </StyledComponentsRegistry>
    </Provider>
  );
}