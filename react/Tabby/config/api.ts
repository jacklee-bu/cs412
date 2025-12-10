// Jack Lee
// jacklee@bu.edu
// api.ts - centralized API configuration with auto-detection

import Constants from 'expo-constants';
import { Platform } from 'react-native';

// Get the local IP from Expo's dev server
const getApiBase = (): string => {
  // In production, use your deployed server
  if (!__DEV__) {
    return 'https://cs-webapps.bu.edu/jacklee/cs412/project';
  }

  // For development, detect the host from Expo
  const debuggerHost = Constants.expoConfig?.hostUri;

  if (debuggerHost) {
    // Extract just the IP/hostname (remove the port)
    const host = debuggerHost.split(':')[0];
    return `http://${host}:8000/project`;
  }

  // Fallback for web or if detection fails
  if (Platform.OS === 'web') {
    return 'http://localhost:8000/project';
  }

  // Last resort fallback
  return 'http://localhost:8000/project';
};

export const API_BASE = getApiBase();
