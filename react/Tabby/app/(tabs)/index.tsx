// Jack Lee
// jacklee@bu.edu
// index.tsx - home screen for Tabby app

import { View, Text, ScrollView, Pressable } from 'react-native';
import { styles } from '../../assets/styles/my_styles';
import { useThemeColors } from '../../config/theme';
import { useState, useEffect } from 'react';
import { router } from 'expo-router';
import { API_BASE } from '../../config/api';

export default function HomeScreen() {
  const colors = useThemeColors();
  const [featured, setFeatured] = useState(null);
  const [chords, setChords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHomeData();
  }, []);

  const loadHomeData = async () => {
    try {
      // fetch featured tab and some chords
      const [featuredRes, chordsRes] = await Promise.all([
        fetch(`${API_BASE}/api/featured/`),
        fetch(`${API_BASE}/api/chords/`)
      ]);

      const featuredData = await featuredRes.json();
      const chordsData = await chordsRes.json();

      setFeatured(featuredData);
      setChords(chordsData.slice(0, 4)); // just show first 4
      console.log('loaded home data');
    } catch (error) {
      console.log('error loading home data:', error);
    } finally {
      setLoading(false);
    }
  };

  const goToTab = (tabId) => {
    router.push(`/tab/${tabId}`);
  };

  if (loading) {
    return (
      <View style={[styles.centered, { backgroundColor: colors.background }]}>
        <Text style={[styles.loadingText, { color: colors.textMuted }]}>Loading...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={[styles.scrollSection, { backgroundColor: colors.background }]}>
      <View style={[styles.screen, { backgroundColor: colors.background }]}>
        {/* header */}
        <Text style={[styles.title, { color: colors.text }]}>Tabby</Text>
        <Text style={[styles.paragraph, { color: colors.textSecondary }]}>
          Your personal guitar tab companion. Learn songs, master chords, track your progress.
        </Text>

        {/* featured tab */}
        {featured && (
          <>
            <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>Featured Tab</Text>
            <Pressable
              style={[styles.featuredCard, { backgroundColor: colors.surface, borderLeftColor: colors.primary }]}
              onPress={() => goToTab(featured.id)}
            >
              <Text style={[styles.songTitle, { color: colors.text }]}>{featured.song_title}</Text>
              <Text style={[styles.artistName, { color: colors.textSecondary }]}>{featured.song_artist}</Text>
              <View style={styles.metaRow}>
                {featured.tuning && (
                  <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.metaText, { color: colors.textSecondary }]}>
                      {featured.tuning === 'standard' ? 'Standard' : featured.tuning}
                    </Text>
                  </View>
                )}
                {featured.capo > 0 && (
                  <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.metaText, { color: colors.textSecondary }]}>Capo {featured.capo}</Text>
                  </View>
                )}
                {featured.tempo && (
                  <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.metaText, { color: colors.textSecondary }]}>{featured.tempo} BPM</Text>
                  </View>
                )}
              </View>
              <Text style={[styles.caption, { marginTop: 12, color: colors.textMuted }]}>
                Tap to view full tab
              </Text>
            </Pressable>
          </>
        )}

        {/* quick chords */}
        {chords.length > 0 && (
          <>
            <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>Quick Chords</Text>
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              style={styles.horizontalScroll}
            >
              {chords.map((chord) => (
                <View key={chord.id} style={[styles.chordCard, { backgroundColor: colors.surface }]}>
                  <Text style={[styles.chordName, { color: colors.text }]}>{chord.name}</Text>
                  <Text style={[styles.chordFullName, { color: colors.textMuted }]}>{chord.full_name}</Text>
                  <Text style={[styles.chordFingering, { color: colors.textSecondary, backgroundColor: colors.surfaceAlt }]}>{chord.fingering}</Text>
                </View>
              ))}
            </ScrollView>
          </>
        )}

        {/* getting started */}
        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>Getting Started</Text>
        <View style={[styles.card, { backgroundColor: colors.surface }]}>
          <Text style={[styles.subtitle, { color: colors.text }]}>How to Read Tabs</Text>
          <Text style={[styles.paragraph, { color: colors.textSecondary }]}>
            Guitar tablature shows six lines representing the strings (low E at bottom, high e at top).
            Numbers indicate which fret to press. 0 means open string, x means don't play that string.
          </Text>
          <View style={[styles.tabContainer, { backgroundColor: colors.tabBg }]}>
            <Text style={[styles.tabContent, { color: colors.tabText }]}>
              e|---0---1---3---{'\n'}
              B|---1---1---0---{'\n'}
              G|---0---2---0---{'\n'}
              D|---2---3---0---{'\n'}
              A|---3---3---2---{'\n'}
              E|---x---1---3---
            </Text>
          </View>
          <Text style={[styles.caption, { color: colors.textMuted }]}>
            Example: C, F, and G chords
          </Text>
        </View>
      </View>
    </ScrollView>
  );
}
