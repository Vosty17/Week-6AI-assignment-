
![IoT Crop Recommendation System log](https://github.com/Vosty17/Logo.png/blob/main/IMG-20250702-WA0016.jpg)
*# IoT Crop Recommendation System with Continuous Learning*

## Overview

This project predicts crop yield using a combination of batch and online machine learning. It leverages sensor data (rainfall, fertilizer, temperature, N, P, K) to help farmers and agronomists make data-driven decisions for better harvests. The system supports continuous learning, updating itself as new data arrives.

## Features

1. Batch training with Gradient Boosting for initial yield prediction.
2. Online learning using River for real-time model updates.
3. Visualizes actual vs. predicted yields.
4. Predicts yield from sensor data via a simple function.
5. Saves and updates models for continuous improvement.

## Dataset

- Input: `crop_yield_data.csv` with features like rainfall, fertilizer, temperature, and soil nutrients.
- Output: Yield in Q/acre.
- Data is cleaned to remove missing yield values.

## Results

- Evaluates model using R² Score and MAE.
- Plots actual vs. predicted yields.
- Online MAE is updated as new data streams in.

## Example Usage

```
good_conditions = {
    'Rain Fall (mm)': 1250,
    'Fertilizer': 80,
    'Temperatue': 28,
    'Nitrogen (N)': 80,
    'Phosphorus (P)': 24,
    'Potassium (K)': 20
}
yield_pred = predict_yield(good_conditions)
print(f"Predicted yield: {yield_pred:.2f} Q/acre")
```
## Development flowchart 
![AIoT System Flowchart]()

## Future Work

- Integrate more IoT sensor types.
- Add web or mobile interface.
- Expand to crop recommendation, not just yield.

## License

MIT License.
