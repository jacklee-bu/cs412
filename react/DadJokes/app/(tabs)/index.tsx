// Jack Lee
// jacklee@bu.edu
// index.tsx - home screen for DadJokes app

import { View, Text, Image, ScrollView } from 'react-native';
import { styles } from '../../assets/styles/my_styles';
import { useState, useEffect } from 'react';

const API_BASE = 'https://cs-webapps.bu.edu/jacklee/cs412/dadjokes';

export default function IndexScreen() {
  const [joke, setJoke] = useState(null);
  const [picture, setPicture] = useState(null);

  useEffect(() => {
    // grab data when screen loads
    fetchRandomJoke();
    fetchRandomPicture();
  }, []);

  const fetchRandomJoke = async () => {
    const response = await fetch(`${API_BASE}/api/random/`);
    const data = await response.json();
    console.log('got joke:', data);
    setJoke(data);
  };

  const fetchRandomPicture = async () => {
    const response = await fetch(`${API_BASE}/api/random_picture/`);
    const data = await response.json();
    console.log('got picture:', data);
    setPicture(data);
  };

  return (
    <ScrollView style={styles.scrollSection}>
      <View style={styles.screen}>
        <Text style={styles.title}>Dad Joke of the Day</Text>

        {joke ? (
          <View style={styles.jokeCard}>
            <Text style={styles.jokeText}>{joke.text}</Text>
            <Text style={styles.contributor}>- {joke.name}</Text>
          </View>
        ) : (
          <Text style={styles.paragraph}>Loading joke...</Text>
        )}

        {picture ? (
          <View>
            <Text style={styles.title}>Random Silly Picture</Text>
            <Image
              source={{ uri: picture.image_url }}
              style={styles.image}
              resizeMode="cover"
            />
            <Text style={styles.contributor}>Contributed by: {picture.name}</Text>
          </View>
        ) : (
          <Text style={styles.paragraph}>Loading picture...</Text>
        )}
      </View>
    </ScrollView>
  );
}
