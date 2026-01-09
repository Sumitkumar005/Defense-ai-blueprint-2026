import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';

const screenWidth = Dimensions.get('window').width;

export default function DashboardScreen() {
  const { user } = useAuth();
  const [workouts, setWorkouts] = useState([]);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [workoutsRes, statsRes] = await Promise.all([
        axios.get('http://localhost:3001/api/workouts'),
        axios.get('http://localhost:3001/api/analytics/personal')
      ]);
      setWorkouts(workoutsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Welcome, {user?.username}</Text>
        <Text style={styles.subtitle}>Physical Readiness Dashboard</Text>
      </View>

      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{stats?.workoutsThisWeek || 0}</Text>
          <Text style={styles.statLabel}>Workouts This Week</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statValue}>{stats?.avgFormScore || 0}%</Text>
          <Text style={styles.statLabel}>Avg Form Score</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Recent Workouts</Text>
        {workouts.slice(0, 5).map((workout) => (
          <TouchableOpacity key={workout._id} style={styles.workoutCard}>
            <Text style={styles.workoutDate}>
              {new Date(workout.date).toLocaleDateString()}
            </Text>
            <Text style={styles.workoutType}>{workout.type}</Text>
            {workout.completed && (
              <Text style={styles.completed}>✓ Completed</Text>
            )}
          </TouchableOpacity>
        ))}
      </View>
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
  statsContainer: {
    flexDirection: 'row',
    padding: 20,
    gap: 15,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  statLabel: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  workoutCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
  },
  workoutDate: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  workoutType: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  completed: {
    fontSize: 12,
    color: '#4CAF50',
    marginTop: 5,
  },
});

