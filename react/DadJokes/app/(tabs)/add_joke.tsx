// Jack Lee
// jacklee@bu.edu
// add_joke.tsx - form to add a new joke

import { View, Text, TextInput, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { styles } from '../../assets/styles/my_styles';
import { useState } from 'react';

const API_BASE = 'https://cs-webapps.bu.edu/jacklee/cs412/dadjokes';

export default function AddJokeScreen() {
  const [jokeText, setJokeText] = useState('');
  const [contributorName, setContributorName] = useState('');

  const handleSubmit = async () => {
    // make sure fields aren't empty
    if (!jokeText || !contributorName) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/jokes/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: jokeText,
          name: contributorName,
        }),
      });

      if (response.ok) {
        console.log('joke posted successfully');
        Alert.alert('Success', 'Your joke has been submitted!');
        // clear the form
        setJokeText('');
        setContributorName('');
      } else {
        console.log('post failed, status:', response.status);
        Alert.alert('Error', 'Failed to submit joke. Please try again.');
      }
    } catch (error) {
      console.log('error posting joke:', error);
      Alert.alert('Error', 'Failed to submit joke. Please try again.');
    }
  };

  return (
    <ScrollView style={styles.scrollSection}>
      <View style={styles.screen}>
        <Text style={styles.title}>Add a Dad Joke</Text>

        <Text style={styles.label}>Your Joke:</Text>
        <TextInput
          style={styles.textArea}
          multiline
          placeholder="Enter your dad joke here..."
          value={jokeText}
          onChangeText={setJokeText}
        />

        <Text style={styles.label}>Your Name:</Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your name"
          value={contributorName}
          onChangeText={setContributorName}
        />

        <TouchableOpacity style={styles.button} onPress={handleSubmit}>
          <Text style={styles.buttonText}>Submit Joke</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}
