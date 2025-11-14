// Jack Lee
// jacklee@bu.edu
// detail.tsx - displays guitar tabs in String Theory app

import { View, Text, ScrollView, Image } from 'react-native';
import { styles } from '../../assets/styles/my_styles';

const introImage = 'https://cs-people.bu.edu/jacklee/images/blackbird_intro.jpg';
const verseImage = 'https://cs-people.bu.edu/jacklee/images/blackbird_verse.jpg';
const bridgeImage = 'https://cs-people.bu.edu/jacklee/images/blackbird_bridge.jpg';

export default function DetailScreen() {
  return (
    <ScrollView style={styles.scrollSection}>
      <View style={styles.screen}>
        <Text style={styles.title}>Blackbird Practice Notes</Text>

        <Text style={styles.paragraph}>
          This breakdown follows the fingerstyle arrangement I have been
          polishing for the last few weeks. The goal is to keep the alternating
          bass line steady while the melody floats on top.
        </Text>

        <Text style={styles.sectionTitle}>Warm-up</Text>
        <Text style={styles.paragraph}>
          Start with the intro shapes and play them super slow with a metronome
          at 60 bpm. If the bass hits drift off beat, the whole song sounds
          messy, so I mute unused strings with my pinky.
        </Text>
        <Image source={{ uri: introImage }} style={styles.remoteImage} />
        <Text style={styles.imageCaption}>Intro shapes with the steady bass hits.</Text>

        <Text style={styles.sectionTitle}>Verse</Text>
        <Text style={styles.paragraph}>
          For the verse I break the measure into two-note chunks so I can focus
          on landing the hammer-ons cleanly. Rolling my thumb slightly toward
          the fretboard helps the bass stay loud without digging in too hard.
        </Text>
        <Image source={{ uri: verseImage }} style={styles.remoteImage} />
        <Text style={styles.imageCaption}>Verse pattern — keep the top melody relaxed.</Text>

        <Text style={styles.sectionTitle}>Bridge</Text>
        <Text style={styles.paragraph}>
          The bridge stretch from the seventh to the third fret still feels
          awkward, so I plant my index finger first and then reach for the
          higher notes. Practicing that move separately for five minutes keeps
          my hand from locking up later.
        </Text>
        <Image source={{ uri: bridgeImage }} style={styles.remoteImage} />
        <Text style={styles.imageCaption}>Bridge stretch that always trips me up.</Text>

        <Text style={styles.paragraph}>
          After everything clicks, I bump the tempo by 5 bpm and try again.
          Recording a quick voice memo helps me hear where the dynamics flatten
          out, which is usually a cue to lighten my picking hand.
        </Text>
      </View>
    </ScrollView>
  );
}
