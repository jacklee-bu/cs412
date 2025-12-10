// Jack Lee
// jacklee@bu.edu
// TunerGauge.tsx - needle gauge for tuner

import React from 'react';
import { View, StyleSheet } from 'react-native';
import Animated, { useAnimatedStyle, withSpring } from 'react-native-reanimated';

interface TunerGaugeProps {
  cents: number;
  isActive: boolean;
  isInTune: boolean;
  colors: any;
}

export function TunerGauge({ cents, isActive, isInTune, colors }: TunerGaugeProps) {
  const clampedCents = Math.max(-50, Math.min(50, cents));
  const targetRotation = (clampedCents / 50) * 45;

  const needleStyle = useAnimatedStyle(() => ({
    transform: [{ rotate: `${withSpring(targetRotation, { damping: 15, stiffness: 100 })}deg` }],
  }), [targetRotation]);

  const needleColor = !isActive ? colors.textMuted : isInTune ? colors.success : colors.error;

  return (
    <View style={[styles.container, { backgroundColor: colors.surface }]}>
      <View style={styles.gaugeArc}>
        {[-50, -25, 0, 25, 50].map((tick) => (
          <View
            key={tick}
            style={[
              styles.tick,
              {
                backgroundColor: tick === 0 ? colors.success : colors.border,
                height: tick === 0 ? 20 : 15,
                transform: [{ rotate: `${(tick / 50) * 45}deg` }, { translateY: -70 }],
              },
            ]}
          />
        ))}
        <View style={[styles.tuneZone, { backgroundColor: colors.success + '30' }]} />
      </View>

      <Animated.View style={[styles.needleContainer, needleStyle]}>
        <View style={[styles.needle, { backgroundColor: needleColor }]} />
        <View style={[styles.needleBase, { backgroundColor: needleColor }]} />
      </Animated.View>

      <View style={[styles.centerDot, { backgroundColor: colors.surface, borderColor: colors.border }]} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: 280,
    height: 160,
    alignItems: 'center',
    justifyContent: 'flex-end',
    overflow: 'hidden',
    borderRadius: 140,
    borderBottomLeftRadius: 0,
    borderBottomRightRadius: 0,
  },
  gaugeArc: {
    position: 'absolute',
    width: 280,
    height: 140,
    alignItems: 'center',
    justifyContent: 'flex-end',
  },
  tick: {
    position: 'absolute',
    width: 3,
    bottom: 0,
    borderRadius: 1.5,
  },
  tuneZone: {
    position: 'absolute',
    width: 30,
    height: 80,
    bottom: 0,
    borderTopLeftRadius: 15,
    borderTopRightRadius: 15,
  },
  needleContainer: {
    position: 'absolute',
    bottom: 0,
    width: 4,
    height: 100,
    alignItems: 'center',
  },
  needle: {
    width: 4,
    height: 90,
    borderRadius: 2,
  },
  needleBase: {
    width: 16,
    height: 16,
    borderRadius: 8,
    marginTop: -8,
  },
  centerDot: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 3,
    marginBottom: -10,
  },
});
