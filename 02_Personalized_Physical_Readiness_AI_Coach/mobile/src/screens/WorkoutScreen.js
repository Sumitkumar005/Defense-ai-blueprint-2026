import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert } from 'react-native';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

export default function WorkoutScreen() {
  const { user } = useAuth();
  const [todayWorkout, setTodayWorkout] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTodayWorkout();
  }, []);

  const loadTodayWorkout = async () => {
    try {
      const response = await axios.post('http://localhost:3001/api/workouts/generate', {
        date: new Date().toISOString(),
        type: 'mixed'
      });
      setTodayWorkout(response.data);
    } catch (error) {
      console.error('Error loading workout:', error);
    }
  };

  const generateWorkout = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:3001/api/workouts/generate', {
        date: new Date().toISOString(),
        type: 'mixed'
      });
      setTodayWorkout(response.data);
    } catch (error) {
      Alert.alert('Error', 'Failed to generate workout');
    } finally {
      setLoading(false);
    }
  };

  const completeWorkout = async () => {
    try {
      await axios.patch(`http://localhost:3001/api/workouts/${todayWorkout._id}/complete`, {
        performance: {
          exercisesCompleted: todayWorkout.exercises.length,
          effortRating: 8
        }
      });
      Alert.alert('Success', 'Workout completed!');
      loadTodayWorkout();
    } catch (error) {
      Alert.alert('Error', 'Failed to complete workout');
    }
  };

  if (!todayWorkout) {
    return (
      <View style={styles.container}>
        <TouchableOpacity style={styles.button} onPress={generateWorkout}>
          <Text style={styles.buttonText}>Generate Today's Workout</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Today's Workout</Text>
        <Text style={styles.subtitle}>{todayWorkout.type}</Text>
      </View>

      <View style={styles.exercisesContainer}>
        {todayWorkout.exercises.map((exercise, index) => (
          <View key={index} style={styles.exerciseCard}>
            <Text style={styles.exerciseName}>{exercise.name}</Text>
            {exercise.sets && (
              <Text style={styles.exerciseDetail}>
                {exercise.sets} sets × {exercise.reps} reps
              </Text>
            )}
            {exercise.duration && (
              <Text style={styles.exerciseDetail}>
                Duration: {Math.floor(exercise.duration / 60)} minutes
              </Text>
            )}
          </View>
        ))}
      </View>

      <TouchableOpacity 
        style={[styles.button, styles.completeButton]} 
        onPress={completeWorkout}
      >
        <Text style={styles.buttonText}>Complete Workout</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginTop: 5,
  },
  exercisesContainer: {
    padding: 20,
  },
  exerciseCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
  },
  exerciseName: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  exerciseDetail: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 10,
    margin: 20,
    alignItems: 'center',
  },
  completeButton: {
    backgroundColor: '#4CAF50',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

