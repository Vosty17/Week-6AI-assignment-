# Week-6AI-assignment-
*# IoT Crop Recommendation System with Continuous Learning*

## Overview
This project is a smart crop recommendation system that uses machine learning to suggest the best crop for a farm based on soil and weather sensor data. It supports continuous learning, allowing the model to improve over time with new data and farmer feedback.

## Features
1. **Initial Model Training:**  
   - Loads and preprocesses the `Crop_recommendation.csv` dataset (N, P, K, temperature, humidity, pH, rainfall, crop label).
   - Trains a Random Forest model for initial crop prediction.
   - Saves preprocessing objects and the trained model for reuse.

2. **Continuous Learning:**  
   - Uses an online learning model (Hoeffding Tree) for real-time updates.
   - Continuously retrains with new sensor data and farmer feedback.
   - Stores historical data for periodic full retraining.

3. **IoT Device Simulation:**  
   - Simulates daily sensor readings.
   - Provides crop recommendations.
   - Accepts simulated farmer feedback to update the model.

## How It Works
- **Data Preprocessing:** Encodes crop labels, scales features, and splits data for training/testing.
- **Model Training:** Trains a Random Forest classifier and evaluates accuracy.
- **Continuous Learning:** Initializes an online model with historical data, updates with new inputs, and periodically retrains.
- **IoT Simulation:** Mimics sensor readings and farmer actions over multiple days.

## Usage
1. Place `Crop_recommendation.csv` in your working directory.
2. Run the main script to train the model and start the simulation.
3. The system will simulate daily readings, recommend crops, and update itself with feedback.

## Requirements
- Python 3.x
- pandas, numpy, scikit-learn, joblib, river
