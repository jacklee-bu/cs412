// Jack Lee
// jacklee@bu.edu
// jokes_list.tsx - shows all the jokes

import { View, Text, ScrollView } from 'react-native';
import { styles } from '../../assets/styles/my_styles';
import { useState, useEffect } from 'react';

export default function JokeListScreen() {
  const [jokes, setJokes] = useState([]);

  useEffect(() => {
    fetchJokes();
  }, []);

  const fetchJokes = async () => {
    try {
      const response = await fetch('https://cs-webapps.bu.edu/jacklee/cs412/dadjokes/api/jokes/');
      const data = await response.json();
      setJokes(data);
      console.log('loaded', data.length, 'jokes');
    } catch (error) {
      console.log('error loading jokes:', error);
    }
  };

  return (
    <ScrollView style={styles.scrollSection}>
      <View style={styles.screen}>
        <Text style={styles.title}>All Dad Jokes</Text>

        {jokes.length > 0 ? (
          jokes.map((joke) => (
            <View key={joke.id} style={styles.jokeCard}>
              <Text style={styles.jokeText}>{joke.text}</Text>
              <Text style={styles.contributor}>- {joke.name}</Text>
            </View>
          ))
        ) : (
          <Text style={styles.paragraph}>Loading jokes...</Text>
        )}
      </View>
    </ScrollView>
  );
}
