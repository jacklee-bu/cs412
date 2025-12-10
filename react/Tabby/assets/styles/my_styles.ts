// Jack Lee
// jacklee@bu.edu
// my_styles.ts - styles for Tabby guitar tabs app

import { StyleSheet, Platform } from 'react-native';

// platform-specific monospace font
const monoFont = Platform.select({
  ios: 'Menlo',
  android: 'monospace',
  default: 'monospace',
});

// color palettes - warm guitar-inspired tones
export const lightColors = {
  primary: '#d97706',      // amber
  primaryLight: '#fbbf24', // light amber
  primaryDark: '#b45309',  // dark amber
  background: '#fffbeb',   // cream
  surface: '#ffffff',
  surfaceAlt: '#fef3c7',   // light amber tint
  text: '#1c1917',         // stone-900
  textSecondary: '#57534e', // stone-600
  textMuted: '#a8a29e',    // stone-400
  border: '#e7e5e4',       // stone-200
  success: '#16a34a',
  error: '#dc2626',
  tabBg: '#1e1e1e',
  tabText: '#e5e5e5',
};

export const darkColors = {
  primary: '#f59e0b',      // brighter amber for dark mode
  primaryLight: '#fbbf24',
  primaryDark: '#d97706',
  background: '#0c0a09',   // stone-950
  surface: '#1c1917',      // stone-900
  surfaceAlt: '#292524',   // stone-800
  text: '#fafaf9',         // stone-50
  textSecondary: '#d6d3d1', // stone-300
  textMuted: '#78716c',    // stone-500
  border: '#44403c',       // stone-700
  success: '#22c55e',
  error: '#ef4444',
  tabBg: '#0c0a09',
  tabText: '#e5e5e5',
};

// default export for backward compatibility
export const colors = lightColors;

export const styles = StyleSheet.create({
  // layout
  screen: {
    flex: 1,
    padding: 20,
    backgroundColor: colors.background,
  },
  scrollSection: {
    flex: 1,
    backgroundColor: colors.background,
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.background,
  },

  // typography
  title: {
    fontSize: 28,
    fontWeight: '700',
    marginBottom: 8,
    color: colors.text,
  },
  subtitle: {
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 6,
    color: colors.text,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
    marginTop: 20,
    color: colors.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  paragraph: {
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 12,
    color: colors.textSecondary,
  },
  caption: {
    fontSize: 14,
    color: colors.textMuted,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 4,
    color: colors.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },

  // cards
  card: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  cardPressed: {
    backgroundColor: colors.surfaceAlt,
  },
  featuredCard: {
    backgroundColor: colors.surface,
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    borderLeftWidth: 4,
    borderLeftColor: colors.primary,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 5,
  },

  // song/tab specific
  songTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 4,
  },
  artistName: {
    fontSize: 15,
    color: colors.textSecondary,
    marginBottom: 8,
  },
  metaRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginTop: 8,
  },
  metaBadge: {
    backgroundColor: colors.surfaceAlt,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  metaText: {
    fontSize: 12,
    color: colors.textSecondary,
    fontWeight: '500',
  },

  // tab content display
  tabContainer: {
    backgroundColor: '#1e1e1e',
    borderRadius: 8,
    padding: 16,
    marginVertical: 12,
  },
  tabContent: {
    fontFamily: monoFont,
    fontSize: 11,
    lineHeight: 14,
    color: '#e5e5e5',
  },
  tabSection: {
    marginBottom: 16,
  },
  tabSectionHeader: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.primary,
    marginBottom: 8,
    fontFamily: monoFont,
  },

  // chord display
  chordCard: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: 16,
    marginRight: 12,
    width: 120,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 6,
    elevation: 2,
  },
  chordName: {
    fontSize: 24,
    fontWeight: '700',
    color: colors.text,
    marginBottom: 4,
  },
  chordFullName: {
    fontSize: 12,
    color: colors.textMuted,
    marginBottom: 8,
  },
  chordFingering: {
    fontSize: 14,
    fontFamily: monoFont,
    color: colors.textSecondary,
    backgroundColor: colors.surfaceAlt,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  difficultyBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
    marginTop: 8,
  },
  difficultyBeginner: {
    backgroundColor: '#dcfce7',
  },
  difficultyIntermediate: {
    backgroundColor: '#fef3c7',
  },
  difficultyAdvanced: {
    backgroundColor: '#fee2e2',
  },

  // search
  searchContainer: {
    marginBottom: 16,
  },
  searchInput: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding: 14,
    fontSize: 16,
    borderWidth: 1,
    borderColor: colors.border,
  },
  searchInputFocused: {
    borderColor: colors.primary,
  },

  // buttons
  button: {
    backgroundColor: colors.primary,
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  buttonSecondary: {
    backgroundColor: colors.surfaceAlt,
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonSecondaryText: {
    color: colors.primary,
    fontSize: 15,
    fontWeight: '600',
  },

  // list
  listItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  listItemContent: {
    flex: 1,
  },

  // empty states
  emptyState: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyStateText: {
    fontSize: 16,
    color: colors.textMuted,
    textAlign: 'center',
    marginTop: 12,
  },

  // loading
  loadingText: {
    fontSize: 16,
    color: colors.textMuted,
  },

  // info row
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  infoLabel: {
    fontSize: 14,
    color: colors.textMuted,
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '500',
    color: colors.text,
  },

  // header area
  headerArea: {
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    marginBottom: 16,
  },

  // horizontal scroll
  horizontalScroll: {
    marginHorizontal: -20,
    paddingHorizontal: 20,
  },

  // row layouts
  row: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  spaceBetween: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
});
