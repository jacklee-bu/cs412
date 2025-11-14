// Jack Lee
// jacklee@bu.edu
// index.tsx - home screen for String Theory app

import { View, Text, Image } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

export default function IndexScreen() {
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>String Theory</Text>

      <Image
        source={require('../../assets/images/guitar.jpg')}
        style={styles.heroImage}
        resizeMode="cover"
      />

      <Text style={styles.paragraph}>
        String Theory is basically my notebook for guitar practice. I use it
        to stash tabs that I reach for over and over again.
      </Text>
      <Text style={styles.paragraph}>
        Every tab has a quick note about why I like it and any tricky finger
        shapes I keep forgetting. Blackbird went in first because that song
        convinced me to learn fingerpicking in the first place.
      </Text>
      <Text style={styles.paragraph}>
        Tap the Tabs page for the full breakdown or the About page for a
        refresher on how to read tabs if it has been a while.
      </Text>
    </View>
  );
}
