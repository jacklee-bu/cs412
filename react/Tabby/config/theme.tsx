// Jack Lee
// jacklee@bu.edu
// theme.tsx - dark mode support

import { createContext, useContext } from 'react';
import { useColorScheme } from 'react-native';
import { lightColors, darkColors } from '../assets/styles/my_styles';

type ColorScheme = typeof lightColors;

export function useThemeColors(): ColorScheme {
  const colorScheme = useColorScheme();
  return colorScheme === 'dark' ? darkColors : lightColors;
}

export function useIsDarkMode(): boolean {
  const colorScheme = useColorScheme();
  return colorScheme === 'dark';
}
