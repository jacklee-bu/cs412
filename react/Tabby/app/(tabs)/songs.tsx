// Jack Lee
// jacklee@bu.edu
// songs.tsx - browse all songs with tabs

import { View, Text, ScrollView, TextInput, Pressable } from 'react-native';
import { styles } from '../../assets/styles/my_styles';
import { useThemeColors } from '../../config/theme';
import { useState, useEffect } from 'react';
import { router } from 'expo-router';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import { API_BASE } from '../../config/api';

export default function SongsScreen() {
  const colors = useThemeColors();
  const [tabs, setTabs] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [searchFocused, setSearchFocused] = useState(false);

  useEffect(() => {
    loadTabs();
  }, []);

  const loadTabs = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/tabs/`);
      const data = await response.json();
      setTabs(data);
      console.log('loaded', data.length, 'tabs');
    } catch (error) {
      console.log('error loading tabs:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchTabs = async () => {
    if (!searchQuery.trim()) {
      loadTabs();
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/search/?q=${encodeURIComponent(searchQuery)}`);
      const data = await response.json();
      setTabs(data.tabs || []);
      console.log('search results:', data.tabs?.length || 0);
    } catch (error) {
      console.log('search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const goToTab = (tabId) => {
    router.push(`/tab/${tabId}`);
  };

  // filter tabs based on search (client-side for quick filtering)
  const filteredTabs = searchQuery
    ? tabs.filter(tab =>
        tab.song_title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        tab.song_artist?.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : tabs;

  return (
    <ScrollView style={[styles.scrollSection, { backgroundColor: colors.background }]}>
      <View style={[styles.screen, { backgroundColor: colors.background }]}>
        {/* search */}
        <View style={styles.searchContainer}>
          <TextInput
            style={[
              styles.searchInput,
              { backgroundColor: colors.surface, borderColor: colors.border, color: colors.text },
              searchFocused && { borderColor: colors.primary }
            ]}
            placeholder="Search songs or artists..."
            placeholderTextColor={colors.textMuted}
            value={searchQuery}
            onChangeText={setSearchQuery}
            onFocus={() => setSearchFocused(true)}
            onBlur={() => setSearchFocused(false)}
            onSubmitEditing={searchTabs}
            returnKeyType="search"
          />
        </View>

        {/* results count */}
        <Text style={[styles.caption, { color: colors.textMuted }]}>
          {filteredTabs.length} {filteredTabs.length === 1 ? 'tab' : 'tabs'} available
        </Text>

        {/* loading state */}
        {loading ? (
          <View style={styles.emptyState}>
            <Text style={[styles.loadingText, { color: colors.textMuted }]}>Loading tabs...</Text>
          </View>
        ) : filteredTabs.length === 0 ? (
          <View style={styles.emptyState}>
            <FontAwesome name="search" size={48} color={colors.textMuted} />
            <Text style={[styles.emptyStateText, { color: colors.textMuted }]}>
              No tabs found. Try a different search.
            </Text>
          </View>
        ) : (
          /* tabs list */
          filteredTabs.map((tab) => (
            <Pressable
              key={tab.id}
              style={({ pressed }) => [
                styles.card,
                { backgroundColor: colors.surface },
                pressed && { backgroundColor: colors.surfaceAlt }
              ]}
              onPress={() => goToTab(tab.id)}
            >
              <View style={styles.spaceBetween}>
                <View style={styles.listItemContent}>
                  <Text style={[styles.songTitle, { color: colors.text }]}>{tab.song_title}</Text>
                  <Text style={[styles.artistName, { color: colors.textSecondary }]}>{tab.song_artist}</Text>
                </View>
                <FontAwesome name="chevron-right" size={16} color={colors.textMuted} />
              </View>

              {/* metadata badges */}
              <View style={styles.metaRow}>
                {tab.tuning && tab.tuning !== 'standard' && (
                  <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.metaText, { color: colors.textSecondary }]}>{tab.tuning}</Text>
                  </View>
                )}
                {tab.capo > 0 && (
                  <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.metaText, { color: colors.textSecondary }]}>Capo {tab.capo}</Text>
                  </View>
                )}
                {tab.chords_used && (
                  <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.metaText, { color: colors.textSecondary }]}>
                      {tab.chords_used.split(',').length} chords
                    </Text>
                  </View>
                )}
                {tab.quality_score > 0 && (
                  <View style={[styles.metaBadge, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.metaText, { color: colors.textSecondary }]}>
                      {tab.quality_score.toFixed(1)} rating
                    </Text>
                  </View>
                )}
              </View>
            </Pressable>
          ))
        )}
      </View>
    </ScrollView>
  );
}
