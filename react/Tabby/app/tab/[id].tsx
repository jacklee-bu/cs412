// Jack Lee
// jacklee@bu.edu
// [id].tsx - tab detail view with full tablature

import { View, Text, ScrollView, Pressable } from 'react-native';
import { styles } from '../../assets/styles/my_styles';
import { useThemeColors } from '../../config/theme';
import { useState, useEffect } from 'react';
import { useLocalSearchParams, router, Stack } from 'expo-router';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import { API_BASE } from '../../config/api';

export default function TabDetailScreen() {
  const colors = useThemeColors();
  const { id } = useLocalSearchParams();
  const [tab, setTab] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      loadTab();
    }
  }, [id]);

  const loadTab = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/tab/${id}/`);
      const data = await response.json();
      setTab(data);
      console.log('loaded tab:', data.song_title);
    } catch (error) {
      console.log('error loading tab:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={[styles.centered, { backgroundColor: colors.background }]}>
        <Text style={[styles.loadingText, { color: colors.textMuted }]}>Loading tab...</Text>
      </View>
    );
  }

  if (!tab) {
    return (
      <View style={[styles.centered, { backgroundColor: colors.background }]}>
        <Text style={[styles.emptyStateText, { color: colors.textMuted }]}>Tab not found</Text>
        <Pressable style={[styles.button, { marginTop: 20, backgroundColor: colors.primary }]} onPress={() => router.back()}>
          <Text style={styles.buttonText}>Go Back</Text>
        </Pressable>
      </View>
    );
  }

  // parse sections from tab content
  const sections = parseTabSections(tab.content);

  return (
    <>
      <Stack.Screen
        options={{
          title: tab.song_title,
          headerStyle: { backgroundColor: colors.surface },
          headerTintColor: colors.text,
        }}
      />
      <ScrollView style={[styles.scrollSection, { backgroundColor: colors.background }]}>
        <View style={[styles.screen, { backgroundColor: colors.background }]}>
          {/* header */}
          <View style={[styles.headerArea, { borderBottomColor: colors.border }]}>
            <Text style={[styles.title, { color: colors.text }]}>{tab.song_title}</Text>
            <Text style={[styles.artistName, { color: colors.textSecondary }]}>{tab.song_artist}</Text>

            {/* metadata */}
            <View style={styles.metaRow}>
              {tab.tuning && (
                <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                  <Text style={[styles.metaText, { color: colors.textSecondary }]}>
                    {tab.tuning === 'standard' ? 'Standard Tuning' : tab.tuning}
                  </Text>
                </View>
              )}
              {tab.capo > 0 && (
                <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                  <Text style={[styles.metaText, { color: colors.textSecondary }]}>Capo {tab.capo}</Text>
                </View>
              )}
              {tab.tempo && (
                <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                  <Text style={[styles.metaText, { color: colors.textSecondary }]}>{tab.tempo} BPM</Text>
                </View>
              )}
            </View>
          </View>

          {/* song info */}
          {tab.chords_used && (
            <View style={[styles.card, { backgroundColor: colors.surface }]}>
              <Text style={[styles.label, { color: colors.textSecondary }]}>Chords Used</Text>
              <Text style={[styles.paragraph, { color: colors.textSecondary }]}>{tab.chords_used}</Text>

              {tab.strumming_pattern && (
                <>
                  <Text style={[styles.label, { marginTop: 12, color: colors.textSecondary }]}>Pattern</Text>
                  <Text style={[styles.paragraph, { color: colors.textSecondary }]}>{tab.strumming_pattern}</Text>
                </>
              )}
            </View>
          )}

          {/* tab content */}
          <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>Tablature</Text>

          {sections.length > 0 ? (
            sections.map((section, index) => (
              <View key={index} style={styles.tabSection}>
                {section.header && (
                  <Text style={[styles.tabSectionHeader, { color: colors.primary }]}>{section.header}</Text>
                )}
                <ScrollView horizontal showsHorizontalScrollIndicator={true}>
                  <View style={[styles.tabContainer, { backgroundColor: colors.tabBg }]}>
                    <Text style={[styles.tabContent, { color: colors.tabText }]}>{section.content}</Text>
                  </View>
                </ScrollView>
              </View>
            ))
          ) : (
            <ScrollView horizontal showsHorizontalScrollIndicator={true}>
              <View style={[styles.tabContainer, { backgroundColor: colors.tabBg }]}>
                <Text style={[styles.tabContent, { color: colors.tabText }]}>{tab.content}</Text>
              </View>
            </ScrollView>
          )}

          {/* source info */}
          {tab.source_site && (
            <View style={{ marginTop: 20, marginBottom: 40 }}>
              <Text style={[styles.caption, { color: colors.textMuted }]}>
                Source: {tab.source_site}
              </Text>
              {tab.quality_score > 0 && (
                <Text style={[styles.caption, { color: colors.textMuted }]}>
                  Rating: {tab.quality_score.toFixed(1)}/5 ({tab.rating_count} votes)
                </Text>
              )}
            </View>
          )}
        </View>
      </ScrollView>
    </>
  );
}

// helper to parse tab content into sections
function parseTabSections(content) {
  if (!content) return [];

  const sections = [];
  const lines = content.split('\n');

  let currentSection = { header: null, content: '' };

  for (const line of lines) {
    // check if this line is a section header like [Verse] or [Chorus]
    const headerMatch = line.match(/^\s*\[([^\]]+)\]\s*$/);

    if (headerMatch) {
      // save previous section if it has content
      if (currentSection.content.trim()) {
        sections.push(currentSection);
      }
      // start new section
      currentSection = { header: headerMatch[1], content: '' };
    } else {
      currentSection.content += line + '\n';
    }
  }

  // dont forget the last section
  if (currentSection.content.trim()) {
    sections.push(currentSection);
  }

  return sections;
}
