// Jack Lee
// jacklee@bu.edu
// tuner.ts - utilities for guitar tuner

import { Platform, PermissionsAndroid, Alert, Linking } from 'react-native';
import { YIN } from 'pitchfinder';

// audio config
export const AUDIO_CONFIG = {
  sampleRate: 44100,
  channels: 1,
  bitsPerSample: 16,
  bufferSize: 4096,
  processingIntervalMs: 50,
  volumeThreshold: 100,
  maxGain: 40,
  yinThreshold: 0.1,
};

// standard tuning frequencies
export const STANDARD_TUNING = {
  E2: 82.41,
  A2: 110.0,
  D3: 146.83,
  G3: 196.0,
  B3: 246.94,
  E4: 329.63,
};

const NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const A4_FREQUENCY = 440;

export interface NoteInfo {
  note: string;
  octave: number;
  frequency: number;
  targetFrequency: number;
  cents: number;
  isInTune: boolean;
}

export interface GuitarString {
  name: string;
  note: string;
  frequency: number;
  stringNumber: number;
}

export const GUITAR_STRINGS: GuitarString[] = [
  { name: 'Low E', note: 'E2', frequency: STANDARD_TUNING.E2, stringNumber: 6 },
  { name: 'A', note: 'A2', frequency: STANDARD_TUNING.A2, stringNumber: 5 },
  { name: 'D', note: 'D3', frequency: STANDARD_TUNING.D3, stringNumber: 4 },
  { name: 'G', note: 'G3', frequency: STANDARD_TUNING.G3, stringNumber: 3 },
  { name: 'B', note: 'B3', frequency: STANDARD_TUNING.B3, stringNumber: 2 },
  { name: 'High e', note: 'E4', frequency: STANDARD_TUNING.E4, stringNumber: 1 },
];

// convert frequency to nearest note
export function frequencyToNote(frequency: number): NoteInfo {
  const semitonesFromA4 = 12 * Math.log2(frequency / A4_FREQUENCY);
  const roundedSemitones = Math.round(semitonesFromA4);
  const targetFrequency = A4_FREQUENCY * Math.pow(2, roundedSemitones / 12);
  const cents = Math.round(1200 * Math.log2(frequency / targetFrequency));
  const noteIndex = ((roundedSemitones % 12) + 12 + 9) % 12;
  const octave = 4 + Math.floor((roundedSemitones + 9) / 12);

  return {
    note: NOTE_NAMES[noteIndex],
    octave,
    frequency,
    targetFrequency,
    cents,
    isInTune: Math.abs(cents) <= 5,
  };
}

// find which guitar string is closest to detected frequency
export function findClosestString(frequency: number): GuitarString | null {
  if (frequency < 60 || frequency > 400) return null;

  let closest: GuitarString | null = null;
  let minDistance = Infinity;

  for (const string of GUITAR_STRINGS) {
    const cents = Math.abs(1200 * Math.log2(frequency / string.frequency));
    if (cents < minDistance) {
      minDistance = cents;
      closest = string;
    }
  }

  return minDistance <= 100 ? closest : null;
}

// pitch detection using YIN
const yinDetector = YIN({
  sampleRate: AUDIO_CONFIG.sampleRate,
  threshold: AUDIO_CONFIG.yinThreshold,
});

export function detectPitch(samples: Float32Array): number | null {
  const frequency = yinDetector(samples);
  if (frequency === null || frequency < 60 || frequency > 1000) return null;
  return frequency;
}

export function pcmToFloat32(pcmData: Int16Array): Float32Array {
  const floatData = new Float32Array(pcmData.length);
  for (let i = 0; i < pcmData.length; i++) {
    floatData[i] = pcmData[i] / 32768;
  }
  return floatData;
}

export function calculateRMS(samples: Float32Array): number {
  let sum = 0;
  for (let i = 0; i < samples.length; i++) {
    sum += samples[i] * samples[i];
  }
  return Math.sqrt(sum / samples.length);
}

export function applyAutoGain(samples: Float32Array): Float32Array {
  const currentRMS = calculateRMS(samples);
  if (currentRMS < 0.001) return samples;

  const gain = Math.min(0.1 / currentRMS, AUDIO_CONFIG.maxGain);
  const amplified = new Float32Array(samples.length);
  for (let i = 0; i < samples.length; i++) {
    amplified[i] = Math.max(-1, Math.min(1, samples[i] * gain));
  }
  return amplified;
}

// mic permissions
export async function requestMicPermission(): Promise<boolean> {
  if (Platform.OS !== 'android') return true;

  const granted = await PermissionsAndroid.request(
    PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
    {
      title: 'Microphone Permission',
      message: 'Tabby needs microphone access to tune your guitar.',
      buttonNeutral: 'Ask Me Later',
      buttonNegative: 'Cancel',
      buttonPositive: 'OK',
    }
  );

  if (granted === PermissionsAndroid.RESULTS.NEVER_ASK_AGAIN) {
    Alert.alert(
      'Microphone Permission Required',
      'Please enable microphone access in settings.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Open Settings', onPress: () => Linking.openSettings() },
      ]
    );
    return false;
  }

  return granted === PermissionsAndroid.RESULTS.GRANTED;
}
