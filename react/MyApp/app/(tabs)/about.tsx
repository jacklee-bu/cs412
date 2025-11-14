// Jack Lee
// jacklee@bu.edu
// about.tsx - help page for String Theory app

import { View, Text, ScrollView } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

export default function AboutScreen() {
  return (
    <ScrollView style={styles.scrollSection}>
      <View style={styles.screen}>
        <Text style={styles.title}>About String Theory</Text>

        <Text style={styles.paragraph}>
          I built this project after losing track of screenshots, PDFs, and
          random sticky notes with fingerings. Keeping everything in one place
          makes practice less chaotic and reminds me to slow down.
        </Text>

        <Text style={styles.paragraph}>
          Tabs are perfect for quick reminders, so this page is a mini crash
          course. If you already know the basics, feel free to skip ahead.
        </Text>

        <Text style={styles.sectionTitle}>Tab Lines</Text>
        <Text style={styles.paragraph}>
          Lines in a tab map directly to strings on the guitar. The bottom line
          is the low E string and the top line is the high E.
        </Text>
        <Text style={styles.tabsBlock}>
          {`e |-------
B |-------
G |-------
D |-------
A |-------
E |-------`}
        </Text>

        <Text style={styles.sectionTitle}>Numbers</Text>
        <Text style={styles.paragraph}>
          Numbers tell you which fret to press. A zero is an open string, and
          stacked numbers mean play them together like a chord.
        </Text>
        <Text style={styles.tabsBlock}>
          {`e |---0---   (open string)
B |---1---   (first fret)
G |---2---   (second fret)`}
        </Text>

        <Text style={styles.sectionTitle}>Practice Habit</Text>
        <Text style={styles.paragraph}>
          When something sounds messy I record a 30 second clip on my phone and
          listen back. Hearing it from the outside makes it obvious which
          strings are buzzing or where the timing drifts.
        </Text>
      </View>
    </ScrollView>
  );
}
