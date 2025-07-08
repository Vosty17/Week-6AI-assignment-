#!/usr/bin/env python3
"""
Colab Setup Script for Edge AI Waste Classification
==================================================

This script sets up the environment and runs the complete Edge AI 
waste classification pipeline in Google Colab.

Run this in a Colab cell to get started quickly!
"""

import os
import sys
import subprocess
import urllib.request
import tarfile

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    packages = [
        'tensorflow>=2.10.0',
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0',
        'scikit-learn>=1.0.0',
        'Pillow>=8.3.0',
        'opencv-python>=4.5.0',
        'tensorflow-hub>=0.12.0',
        'tensorflow-datasets>=4.5.0'
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    
    print("All packages installed successfully!")

def download_dataset():
    """Download sample dataset"""
    print("Downloading sample dataset...")
    
    dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
    dataset_file = "flower_photos.tgz"
    
    if not os.path.exists("flower_photos"):
        print(f"Downloading dataset from {dataset_url}...")
        urllib.request.urlretrieve(dataset_url, dataset_file)
        
        print("Extracting dataset...")
        with tarfile.open(dataset_file, 'r:gz') as tar:
            tar.extractall()
        
        # Clean up
        os.remove(dataset_file)
        print("Dataset downloaded and extracted successfully!")
    else:
        print("Dataset already exists!")

def run_edge_ai_pipeline():
    """Run the complete Edge AI pipeline"""
    print("Running Edge AI waste classification pipeline...")
    
    # Import the main classifier
    from edge_ai_waste_classification import EdgeAIWasteClassifier
    
    # Initialize classifier
    classifier = EdgeAIWasteClassifier(img_size=224, batch_size=32)
    
    # Setup data generators
    classifier.setup_data_generators('flower_photos')
    
    # Create and train model
    classifier.create_model()
    classifier.train_model(epochs=10)  # Reduced epochs for Colab demo
    
    # Plot training history
    classifier.plot_training_history()
    
    # Evaluate model
    accuracy, predictions, true_labels, predicted_labels = classifier.evaluate_model()
    
    # Convert to TFLite
    tflite_model_path, tflite_model = classifier.convert_to_tflite()
    
    # Test TFLite model
    classifier.validation_generator.reset()
    test_batch = next(classifier.validation_generator)
    test_images = test_batch[0][:10]
    test_labels = np.argmax(test_batch[1][:10], axis=1)
    
    tflite_accuracy, avg_inference_time = classifier.test_tflite_model(
        tflite_model_path, test_images, test_labels
    )
    
    # Compare performance
    classifier.compare_performance(tflite_model_path, test_images)
    
    # Generate deployment report
    report = classifier.generate_deployment_report(
        tflite_model_path, tflite_accuracy, avg_inference_time
    )
    
    # Save report
    with open('edge_ai_deployment_report.md', 'w') as f:
        f.write(report)
    
    print("\n" + "=" * 60)
    print("EDGE AI PROTOTYPE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("Generated files:")
    print("• waste_classification_model.tflite - TensorFlow Lite model")
    print("• edge_ai_deployment_report.md - Deployment report")
    print("• confusion_matrix.png - Model evaluation")
    print("• training_history.png - Training progress")
    print("\nThe model is ready for deployment on edge devices!")

def main():
    """Main setup function"""
    print("=" * 60)
    print("Edge AI Waste Classification - Colab Setup")
    print("=" * 60)
    
    try:
        # Install requirements
        install_requirements()
        
        # Download dataset
        download_dataset()
        
        # Run the pipeline
        run_edge_ai_pipeline()
        
    except Exception as e:
        print(f"Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 