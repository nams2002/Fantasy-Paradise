import { DefaultTheme } from 'styled-components';

interface ColorPalette {
  50: string;
  100: string;
  200: string;
  300: string;
  400: string;
  500: string;
  600: string;
  700: string;
  800: string;
  900: string;
}

const colors = {
  blue: {
    50: '#eff6ff',
    100: '#dbeafe',
    200: '#bfdbfe',
    300: '#93c5fd',
    400: '#60a5fa',
    500: '#3b82f6',
    600: '#2563eb',
    700: '#1d4ed8',
    800: '#1e40af',
    900: '#1e3a8a',
  } as ColorPalette,
  gray: {
    50: '#ffffff',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  } as ColorPalette,
  orange: {
    50: '#fff7ed',
    100: '#ffedd5',
    200: '#fed7aa',
    300: '#fdba74',
    400: '#fb923c',
    500: '#f97316',
    600: '#ea580c',
    700: '#c2410c',
    800: '#9a3412',
    900: '#7c2d12',
  } as ColorPalette,
  green: {
    50: '#f0fdf4',
    100: '#dcfce7',
    200: '#bbf7d0',
    300: '#86efac',
    400: '#4ade80',
    500: '#22c55e',
    600: '#16a34a',
    700: '#15803d',
    800: '#166534',
    900: '#1B2B1B',
  } as ColorPalette,
};

const createTheme = (isDark: boolean): DefaultTheme => ({
  colors: {
    background: isDark ? colors.gray[900] : colors.gray[50],
    background2: isDark ? colors.gray[800] : colors.gray[100],
    header: isDark ? colors.gray[800] : colors.gray[50],
    footer: isDark ? colors.gray[800] : colors.gray[50],
    primary: colors.orange[300],
    primaryHover: isDark ? colors.orange[400] : colors.orange[600],
    primaryLight: isDark ? colors.orange[400] : colors.orange[300],
    primaryDark: isDark ? colors.orange[600] : colors.orange[700],
    text: {
      primary: isDark ? colors.gray[100] : colors.gray[900],
      secondary: isDark ? colors.gray[300] : colors.gray[600],
    },
    surface: {
      primary: isDark ? colors.gray[800] : colors.gray[50],
      secondary: isDark ? colors.gray[700] : colors.gray[200],
    },
    social: {
      twitter: '#1DA1F2',
      facebook: '#1877F2',
      instagram: '#E4405F',
    },
    box:{
      primary: isDark ? colors.green[800] : "#1B2B1B",
      secondary: isDark ? colors.gray[700] : "#bde9fb",
    }
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
  },
  transitions: {
    fast: '150ms ease',
    normal: '300ms ease',
    slow: '500ms ease',
  },
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
  },
  typography: {
    heading: 'var(--font-jockey-one)',
    body: 'var(--font-roboto)',
    logo: 'var(--font-caveat)',

    title: 'var(--font-Bruce-one)',
    para: 'var(--font-mangaregular)',
    light: 'var(--font-mangabold)',
    poky: 'var(--font-poky)',

  },

});

export const lightTheme = createTheme(false);
export const darkTheme = createTheme(true);



