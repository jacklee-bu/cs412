// Jack Lee
// jacklee@bu.edu
// tuner.tsx - guitar tuner screen

import React from 'react';
import { View, Text, Pressable, StyleSheet, ScrollView } from 'react-native';
import { useThemeColors } from '../../config/theme';
import { useTuner } from '../../hooks/useTuner';
import { GUITAR_STRINGS } from '../../utils/tuner';
import { TunerGauge } from '../../components/tuner/TunerGauge';
import { styles as appStyles } from '../../assets/styles/my_styles';

export default function TunerScreen() {
  const colors = useThemeColors();
  const tuner = useTuner();

  const centsText = tuner.cents > 0 ? `+${tuner.cents}` : `${tuner.cents}`;
  const noteColor = !tuner.isActive ? colors.textMuted : tuner.isInTune ? colors.success : colors.text;
  const centsColor = !tuner.isActive ? colors.textMuted : tuner.isInTune ? colors.success : Math.abs(tuner.cents) > 20 ? colors.error : colors.textSecondary;

  const getStatusText = () => {
    if (tuner.error) return tuner.error;
    if (tuner.state === 'idle') return 'Tap Start to begin tuning';
    if (!tuner.isActive) return 'Play a string...';
    return 'Listening...';
  };

  return (
    <ScrollView style={[appStyles.scrollSection, { backgroundColor: colors.background }]} contentContainerStyle={styles.content}>
      <View style={styles.container}>
        <Text style={[appStyles.title, { color: colors.text, textAlign: 'center' }]}>Guitar Tuner</Text>
        <Text style={[appStyles.caption, { color: colors.textMuted, textAlign: 'center', marginBottom: 24 }]}>
          Standard Tuning (E A D G B e)
        </Text>

        {/* gauge */}
        <View style={styles.gaugeContainer}>
          <TunerGauge cents={tuner.cents} isActive={tuner.isActive} isInTune={tuner.isInTune} colors={colors} />
        </View>

        {/* note display */}
        <View style={styles.noteContainer}>
          <View style={styles.noteRow}>
            <Text style={[styles.note, { color: noteColor }]}>{tuner.note ?? '-'}</Text>
            {tuner.octave !== null && <Text style={[styles.octave, { color: colors.textMuted }]}>{tuner.octave}</Text>}
          </View>
          <Text style={[styles.frequency, { color: colors.textSecondary }]}>
            {tuner.frequency ? `${tuner.frequency.toFixed(1)} Hz` : '-- Hz'}
          </Text>
          <View style={styles.centsRow}>
            <Text style={[styles.centsLabel, { color: colors.textMuted }]}>
              {!tuner.isActive ? '' : Math.abs(tuner.cents) <= 5 ? 'IN TUNE' : tuner.cents < 0 ? 'FLAT' : 'SHARP'}
            </Text>
            <Text style={[styles.cents, { color: centsColor }]}>{tuner.isActive ? centsText : '--'} ¢</Text>
          </View>
        </View>

        {/* volume + status */}
        <View style={styles.statusContainer}>
          {tuner.state === 'listening' && (
            <View style={styles.volumeMeter}>
              <View style={[styles.volumeTrack, { backgroundColor: colors.surfaceAlt }]}>
                <View style={[styles.volumeFill, { backgroundColor: tuner.isActive ? colors.primary : colors.textMuted, width: `${Math.min(100, tuner.volume * 100)}%` }]} />
              </View>
              <Text style={[styles.volumeLabel, { color: colors.textMuted }]}>INPUT</Text>
            </View>
          )}
          <Text style={[styles.status, { color: tuner.error ? colors.error : tuner.isActive ? colors.success : colors.textMuted }]}>
            {getStatusText()}
          </Text>
        </View>

        {/* start/stop */}
        <View style={styles.buttonContainer}>
          <Pressable
            style={[styles.mainButton, { backgroundColor: tuner.state === 'listening' ? colors.error : colors.primary }]}
            onPress={tuner.state === 'listening' ? tuner.stop : tuner.start}
          >
            <Text style={styles.mainButtonText}>{tuner.state === 'listening' ? 'Stop' : 'Start'}</Text>
          </Pressable>
        </View>

        {/* string selector */}
        <View style={styles.stringsContainer}>
          <Text style={[styles.stringsLabel, { color: colors.textMuted }]}>TARGET STRING (optional)</Text>
          <View style={styles.stringsRow}>
            {GUITAR_STRINGS.map((string) => {
              const isSelected = tuner.targetString?.note === string.note;
              const isDetected = tuner.closestString?.note === string.note && !tuner.targetString;
              return (
                <Pressable
                  key={string.note}
                  style={[styles.stringButton, { backgroundColor: isSelected ? colors.primary : isDetected ? colors.surfaceAlt : colors.surface, borderColor: isDetected ? colors.primary : colors.border }]}
                  onPress={() => tuner.setTargetString(isSelected ? null : string)}
                >
                  <Text style={[styles.stringNote, { color: isSelected ? '#fff' : isDetected ? colors.primary : colors.text }]}>
                    {string.note.replace(/\d/, '')}
                  </Text>
                  <Text style={[styles.stringNumber, { color: isSelected ? 'rgba(255,255,255,0.7)' : colors.textMuted }]}>
                    {string.stringNumber}
                  </Text>
                </Pressable>
              );
            })}
          </View>
          <Pressable
            style={[styles.autoButton, { backgroundColor: !tuner.targetString ? colors.primary : colors.surface, borderColor: colors.border }]}
            onPress={() => tuner.setTargetString(null)}
          >
            <Text style={[styles.autoText, { color: !tuner.targetString ? '#fff' : colors.textSecondary }]}>Auto-detect</Text>
          </Pressable>
        </View>

        {/* tips */}
        <View style={[appStyles.card, { backgroundColor: colors.surface, marginTop: 24 }]}>
          <Text style={[appStyles.subtitle, { color: colors.text }]}>Tips</Text>
          <Text style={[appStyles.paragraph, { color: colors.textSecondary, marginBottom: 0 }]}>
            • Play one string at a time for best accuracy{'\n'}
            • Let the note ring out clearly{'\n'}
            • Green zone = in tune (±5 cents){'\n'}
            • Tune in a quiet environment
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: { flexGrow: 1, paddingBottom: 40 },
  container: { flex: 1, padding: 20 },
  gaugeContainer: { alignItems: 'center', marginVertical: 20 },
  noteContainer: { alignItems: 'center', paddingVertical: 20 },
  noteRow: { flexDirection: 'row', alignItems: 'flex-end' },
  note: { fontSize: 72, fontWeight: '700' },
  octave: { fontSize: 32, fontWeight: '500', marginBottom: 8, marginLeft: 4 },
  frequency: { fontSize: 18, marginTop: 4 },
  centsRow: { flexDirection: 'row', alignItems: 'center', marginTop: 12, gap: 8 },
  centsLabel: { fontSize: 12, fontWeight: '600', letterSpacing: 1 },
  cents: { fontSize: 24, fontWeight: '600' },
  statusContainer: { alignItems: 'center', paddingVertical: 16, gap: 12 },
  volumeMeter: { alignItems: 'center', gap: 4 },
  volumeTrack: { width: 200, height: 6, borderRadius: 3, overflow: 'hidden' },
  volumeFill: { height: '100%', borderRadius: 3 },
  volumeLabel: { fontSize: 10, fontWeight: '600', letterSpacing: 1 },
  status: { fontSize: 14, fontWeight: '500' },
  buttonContainer: { alignItems: 'center', marginVertical: 16 },
  mainButton: { paddingHorizontal: 48, paddingVertical: 16, borderRadius: 30, minWidth: 160, alignItems: 'center' },
  mainButtonText: { color: '#fff', fontSize: 18, fontWeight: '700' },
  stringsContainer: { alignItems: 'center', paddingVertical: 16 },
  stringsLabel: { fontSize: 12, fontWeight: '600', letterSpacing: 1, marginBottom: 12 },
  stringsRow: { flexDirection: 'row', gap: 8 },
  stringButton: { width: 48, height: 56, borderRadius: 12, borderWidth: 2, alignItems: 'center', justifyContent: 'center' },
  stringNote: { fontSize: 18, fontWeight: '700' },
  stringNumber: { fontSize: 11, fontWeight: '500' },
  autoButton: { marginTop: 12, paddingHorizontal: 20, paddingVertical: 10, borderRadius: 20, borderWidth: 1 },
  autoText: { fontSize: 14, fontWeight: '600' },
});
