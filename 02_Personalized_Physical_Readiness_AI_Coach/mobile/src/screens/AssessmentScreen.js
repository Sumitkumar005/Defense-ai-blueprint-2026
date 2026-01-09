import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function AssessmentScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Fitness Assessment</Text>
      <Text style={styles.subtitle}>PT Test and Form Analysis</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginTop: 10,
  },
});

