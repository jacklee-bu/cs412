// Jack Lee
// jacklee@bu.edu
// chords.tsx - chord library for Tabby app

import { View, Text, ScrollView, Pressable } from 'react-native';
import { styles } from '../../assets/styles/my_styles';
import { useThemeColors } from '../../config/theme';
import { useState, useEffect } from 'react';
import { API_BASE } from '../../config/api';

export default function ChordsScreen() {
  const colors = useThemeColors();
  const [chords, setChords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [expandedChord, setExpandedChord] = useState(null);

  const difficulties = ['all', 'beginner', 'intermediate', 'advanced'];

  useEffect(() => {
    loadChords();
  }, []);

  const loadChords = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/chords/`);
      const data = await response.json();
      setChords(data);
      console.log('loaded', data.length, 'chords');
    } catch (error) {
      console.log('error loading chords:', error);
    } finally {
      setLoading(false);
    }
  };

  // filter by difficulty
  const filteredChords = selectedDifficulty === 'all'
    ? chords
    : chords.filter(c => c.difficulty === selectedDifficulty);

  // group by category
  const groupedChords = filteredChords.reduce((acc, chord) => {
    const cat = chord.category || 'other';
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(chord);
    return acc;
  }, {});

  const getDifficultyStyle = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return styles.difficultyBeginner;
      case 'intermediate': return styles.difficultyIntermediate;
      case 'advanced': return styles.difficultyAdvanced;
      default: return {};
    }
  };

  const toggleChord = (chordId) => {
    setExpandedChord(expandedChord === chordId ? null : chordId);
  };

  if (loading) {
    return (
      <View style={[styles.centered, { backgroundColor: colors.background }]}>
        <Text style={[styles.loadingText, { color: colors.textMuted }]}>Loading chords...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={[styles.scrollSection, { backgroundColor: colors.background }]}>
      <View style={[styles.screen, { backgroundColor: colors.background }]}>
        <Text style={[styles.title, { color: colors.text }]}>Chord Library</Text>
        <Text style={[styles.paragraph, { color: colors.textSecondary }]}>
          Tap a chord to see fingering details. The notation shows fret positions for each string (E A D G B e).
        </Text>

        {/* difficulty filter */}
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={{ marginBottom: 20, marginHorizontal: -20, paddingHorizontal: 20 }}
        >
          {difficulties.map((diff) => (
            <Pressable
              key={diff}
              style={[
                styles.buttonSecondary,
                { marginRight: 8, backgroundColor: colors.surfaceAlt },
                selectedDifficulty === diff && { backgroundColor: colors.primary }
              ]}
              onPress={() => setSelectedDifficulty(diff)}
            >
              <Text style={[
                styles.buttonSecondaryText,
                { color: colors.primary },
                selectedDifficulty === diff && { color: '#fff' }
              ]}>
                {diff.charAt(0).toUpperCase() + diff.slice(1)}
              </Text>
            </Pressable>
          ))}
        </ScrollView>

        {/* chords by category */}
        {Object.entries(groupedChords).map(([category, categoryChords]) => (
          <View key={category}>
            <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>
              {category.replace('_', ' ')}
            </Text>

            {categoryChords.map((chord) => (
              <Pressable
                key={chord.id}
                style={({ pressed }) => [
                  styles.card,
                  { backgroundColor: colors.surface },
                  pressed && { backgroundColor: colors.surfaceAlt }
                ]}
                onPress={() => toggleChord(chord.id)}
              >
                <View style={styles.spaceBetween}>
                  <View style={styles.row}>
                    <Text style={[styles.chordName, { marginRight: 12, color: colors.text }]}>
                      {chord.name}
                    </Text>
                    <Text style={[styles.artistName, { color: colors.textSecondary }]}>{chord.full_name}</Text>
                  </View>
                  <View style={[styles.difficultyBadge, getDifficultyStyle(chord.difficulty)]}>
                    <Text style={[styles.metaText, { color: colors.textSecondary }]}>{chord.difficulty}</Text>
                  </View>
                </View>

                {/* expanded details */}
                {expandedChord === chord.id && (
                  <View style={{ marginTop: 16 }}>
                    <Text style={[styles.label, { color: colors.textSecondary }]}>Fingering</Text>
                    <View style={[styles.tabContainer, { backgroundColor: colors.tabBg }]}>
                      <Text style={[styles.tabContent, { color: colors.tabText }]}>
                        {formatFingering(chord.fingering)}
                      </Text>
                    </View>
                    <Text style={[styles.caption, { color: colors.textMuted }]}>
                      x = dont play, 0 = open string, numbers = fret position
                    </Text>
                  </View>
                )}
              </Pressable>
            ))}
          </View>
        ))}

        {filteredChords.length === 0 && (
          <View style={styles.emptyState}>
            <Text style={[styles.emptyStateText, { color: colors.textMuted }]}>
              No chords found for this difficulty level.
            </Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

// helper to format fingering as a visual representation
function formatFingering(fingering) {
  if (!fingering) return '';

  const strings = ['E', 'A', 'D', 'G', 'B', 'e'];
  const frets = fingering.split('');

  return strings.map((str, i) => {
    const fret = frets[i] || '-';
    return `${str}|---${fret}---`;
  }).join('\n');
}
