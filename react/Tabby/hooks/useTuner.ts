// Jack Lee
// jacklee@bu.edu
// useTuner.ts - hook for guitar tuner functionality

import { useState, useCallback, useEffect, useRef } from 'react';
import LiveAudioStream from 'react-native-live-audio-stream';
import { Buffer } from 'buffer';
import * as Haptics from 'expo-haptics';
import {
  AUDIO_CONFIG,
  GuitarString,
  NoteInfo,
  detectPitch,
  pcmToFloat32,
  applyAutoGain,
  calculateRMS,
  frequencyToNote,
  findClosestString,
  requestMicPermission,
} from '../utils/tuner';

export type TunerState = 'idle' | 'listening' | 'error';

interface TunerData {
  state: TunerState;
  error: string | null;
  frequency: number | null;
  note: string | null;
  octave: number | null;
  cents: number;
  isInTune: boolean;
  volume: number;
  isActive: boolean;
  targetString: GuitarString | null;
  closestString: GuitarString | null;
  start: () => Promise<void>;
  stop: () => void;
  setTargetString: (s: GuitarString | null) => void;
}

export function useTuner(): TunerData {
  const [state, setState] = useState<TunerState>('idle');
  const [error, setError] = useState<string | null>(null);
  const [targetString, setTargetString] = useState<GuitarString | null>(null);
  const [pitchData, setPitchData] = useState({
    frequency: null as number | null,
    noteInfo: null as NoteInfo | null,
    closestString: null as GuitarString | null,
    volume: 0,
    isActive: false,
  });

  const isInitialized = useRef(false);
  const lastProcessTime = useRef(0);
  const lastInTuneTime = useRef(0);
  const recentFrequencies = useRef<number[]>([]);

  // process audio samples
  const processAudio = useCallback((samples: Int16Array) => {
    const now = Date.now();
    if (now - lastProcessTime.current < AUDIO_CONFIG.processingIntervalMs) return;
    lastProcessTime.current = now;

    const floatSamples = pcmToFloat32(samples);
    const rms = calculateRMS(floatSamples);
    const volume = Math.min(1, rms * 10);

    const maxSample = Math.max(...Array.from(samples).map(Math.abs));
    if (maxSample < AUDIO_CONFIG.volumeThreshold) {
      setPitchData(prev => ({ ...prev, volume, isActive: false }));
      return;
    }

    const amplified = applyAutoGain(floatSamples);
    const rawFreq = detectPitch(amplified);

    if (rawFreq === null) {
      setPitchData(prev => ({ ...prev, volume, isActive: false }));
      return;
    }

    // smooth out readings
    recentFrequencies.current.push(rawFreq);
    if (recentFrequencies.current.length > 5) recentFrequencies.current.shift();
    const avgFreq = recentFrequencies.current.reduce((a, b) => a + b, 0) / recentFrequencies.current.length;

    setPitchData({
      frequency: avgFreq,
      noteInfo: frequencyToNote(avgFreq),
      closestString: findClosestString(avgFreq),
      volume,
      isActive: true,
    });
  }, []);

  // start tuner
  const start = useCallback(async () => {
    setError(null);
    recentFrequencies.current = [];

    const hasPermission = await requestMicPermission();
    if (!hasPermission) {
      setError('Microphone permission denied');
      return;
    }

    if (!isInitialized.current) {
      LiveAudioStream.init({
        sampleRate: AUDIO_CONFIG.sampleRate,
        channels: AUDIO_CONFIG.channels,
        bitsPerSample: AUDIO_CONFIG.bitsPerSample,
        audioSource: 6,
        bufferSize: AUDIO_CONFIG.bufferSize,
      });
      isInitialized.current = true;
    }

    LiveAudioStream.start();
    setState('listening');
  }, []);

  // stop tuner
  const stop = useCallback(() => {
    LiveAudioStream.stop();
    setState('idle');
    recentFrequencies.current = [];
    setPitchData({
      frequency: null,
      noteInfo: null,
      closestString: null,
      volume: 0,
      isActive: false,
    });
  }, []);

  // handle audio data when listening
  useEffect(() => {
    if (state !== 'listening') return;

    const handleData = (data: string) => {
      const buffer = Buffer.from(data, 'base64');
      const samples = new Int16Array(buffer.buffer, buffer.byteOffset, buffer.length / 2);
      processAudio(samples);
    };

    LiveAudioStream.on('data', handleData);
    return () => {
      // cleanup handled by library
    };
  }, [state, processAudio]);

  // cleanup on unmount
  useEffect(() => {
    return () => {
      if (state === 'listening') LiveAudioStream.stop();
    };
  }, [state]);

  // calculate cents (relative to target string if set)
  const cents = (() => {
    if (!pitchData.frequency) return 0;
    if (targetString) {
      return Math.round(1200 * Math.log2(pitchData.frequency / targetString.frequency));
    }
    return pitchData.noteInfo?.cents ?? 0;
  })();

  const isInTune = Math.abs(cents) <= 5 && pitchData.isActive;

  // haptic when in tune
  useEffect(() => {
    if (isInTune) {
      const now = Date.now();
      if (now - lastInTuneTime.current > 1000) {
        Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
        lastInTuneTime.current = now;
      }
    }
  }, [isInTune]);

  return {
    state,
    error,
    frequency: pitchData.frequency,
    note: pitchData.noteInfo?.note ?? null,
    octave: pitchData.noteInfo?.octave ?? null,
    cents,
    isInTune,
    volume: pitchData.volume,
    isActive: pitchData.isActive,
    targetString,
    closestString: pitchData.closestString,
    start,
    stop,
    setTargetString,
  };
}
