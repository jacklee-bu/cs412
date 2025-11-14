// Jack Lee
// jacklee@bu.edu
// my_styles.ts - centralized styles for String Theory app

import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  screen: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  scrollSection: {
    flex: 1,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    marginBottom: 14,
    color: '#1f1f1f',
  },
  paragraph: {
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 12,
    color: '#474747',
  },
  heroImage: {
    width: '100%',
    height: 210,
    borderRadius: 10,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginTop: 18,
    marginBottom: 6,
    color: '#333',
  },
  remoteImage: {
    width: '100%',
    height: 200,
    borderRadius: 8,
    marginTop: 10,
  },
  imageCaption: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
    marginBottom: 8,
  },
  tabsBlock: {
    fontFamily: 'Courier',
    fontSize: 13,
    backgroundColor: '#f3f3f3',
    padding: 10,
    borderRadius: 4,
    marginBottom: 12,
  },
  aboutImage: {
    width: 140,
    height: 140,
    alignSelf: 'center',
    marginBottom: 16,
    borderRadius: 70,
  },
});
