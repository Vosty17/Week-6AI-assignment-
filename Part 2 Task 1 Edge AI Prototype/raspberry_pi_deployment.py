#!/usr/bin/env python3
"""
Raspberry Pi Deployment Script for Edge AI Waste Classification
=============================================================

This script demonstrates how to deploy the trained TensorFlow Lite model
on a Raspberry Pi for real-time waste classification.

Requirements:
- Raspberry Pi 4 (recommended)
- Camera module (Pi Camera v2 or USB camera)
- TensorFlow Lite runtime
- OpenCV for camera access

Installation:
pip install tflite-runtime opencv-python numpy pillow
"""

import cv2
import numpy as np
import tensorflow as tf
import time
import os
from PIL import Image
import argparse

class RaspberryPiWasteClassifier:
    """Real-time waste classification on Raspberry Pi"""
    
    def __init__(self, model_path, class_names, img_size=224):
        self.model_path = model_path
        self.class_names = class_names
        self.img_size = img_size
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        
        # Initialize TensorFlow Lite interpreter
        self.setup_interpreter()
        
    def setup_interpreter(self):
        """Setup TensorFlow Lite interpreter"""
        print(f"Loading model from: {self.model_path}")
        
        # Load TFLite model
        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        
        # Get input and output details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        print(f"Input shape: {self.input_details[0]['shape']}")
        print(f"Output shape: {self.output_details[0]['shape']}")
        print(f"Model loaded successfully!")
        
    def preprocess_image(self, image):
        """Preprocess image for inference"""
        # Resize image
        image = cv2.resize(image, (self.img_size, self.img_size))
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values
        image = image.astype(np.float32) / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
        
    def predict(self, image):
        """Run inference on preprocessed image"""
        # Set input tensor
        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        
        # Run inference
        start_time = time.time()
        self.interpreter.invoke()
        inference_time = time.time() - start_time
        
        # Get output
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        # Get prediction
        predicted_class = np.argmax(output[0])
        confidence = np.max(output[0])
        
        return predicted_class, confidence, inference_time
        
    def run_camera_inference(self, camera_index=0, display=True):
        """Run real-time inference using camera"""
        print(f"Starting camera inference (camera index: {camera_index})...")
        print("Press 'q' to quit, 's' to save image")
        
        # Initialize camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return
            
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        frame_count = 0
        total_inference_time = 0
        
        try:
            while True:
                # Capture frame
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break
                    
                # Preprocess frame
                processed_image = self.preprocess_image(frame)
                
                # Run inference
                predicted_class, confidence, inference_time = self.predict(processed_image)
                
                # Update statistics
                frame_count += 1
                total_inference_time += inference_time
                
                # Get class name
                class_name = self.class_names[predicted_class]
                
                # Display results on frame
                if display:
                    # Add text overlay
                    text = f"{class_name}: {confidence:.2f}"
                    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                               1, (0, 255, 0), 2)
                    
                    # Add inference time
                    fps_text = f"FPS: {1/inference_time:.1f}"
                    cv2.putText(frame, fps_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
                               1, (0, 255, 0), 2)
                    
                    # Add frame count
                    frame_text = f"Frame: {frame_count}"
                    cv2.putText(frame, frame_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 
                               1, (0, 255, 0), 2)
                    
                    # Display frame
                    cv2.imshow('Edge AI Waste Classification', frame)
                    
                # Print results to console
                print(f"Frame {frame_count}: {class_name} ({confidence:.3f}) - {inference_time*1000:.1f}ms")
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save current frame
                    timestamp = int(time.time())
                    filename = f"waste_classification_{timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    print(f"Saved frame as: {filename}")
                    
        except KeyboardInterrupt:
            print("\nStopping camera inference...")
            
        finally:
            # Clean up
            cap.release()
            cv2.destroyAllWindows()
            
            # Print statistics
            if frame_count > 0:
                avg_inference_time = total_inference_time / frame_count
                avg_fps = 1 / avg_inference_time
                print(f"\nStatistics:")
                print(f"Total frames processed: {frame_count}")
                print(f"Average inference time: {avg_inference_time*1000:.2f} ms")
                print(f"Average FPS: {avg_fps:.1f}")
                
    def test_single_image(self, image_path):
        """Test inference on a single image"""
        print(f"Testing inference on: {image_path}")
        
        # Load and preprocess image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image {image_path}")
            return
            
        processed_image = self.preprocess_image(image)
        
        # Run inference
        predicted_class, confidence, inference_time = self.predict(processed_image)
        
        # Get class name
        class_name = self.class_names[predicted_class]
        
        # Display results
        print(f"Prediction: {class_name}")
        print(f"Confidence: {confidence:.3f}")
        print(f"Inference time: {inference_time*1000:.2f} ms")
        
        # Display image with prediction
        cv2.putText(image, f"{class_name}: {confidence:.2f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Prediction Result', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    """Main function for Raspberry Pi deployment"""
    parser = argparse.ArgumentParser(description='Raspberry Pi Edge AI Waste Classification')
    parser.add_argument('--model', type=str, default='waste_classification_model.tflite',
                        help='Path to TensorFlow Lite model')
    parser.add_argument('--camera', type=int, default=0,
                        help='Camera index (0 for Pi Camera, 1 for USB camera)')
    parser.add_argument('--image', type=str, default=None,
                        help='Path to test image (optional)')
    parser.add_argument('--no-display', action='store_true',
                        help='Disable display (for headless operation)')
    
    args = parser.parse_args()
    
    # Check if model exists
    if not os.path.exists(args.model):
        print(f"Error: Model file '{args.model}' not found!")
        print("Please ensure you have the trained TensorFlow Lite model.")
        return
    
    # Define class names (update these based on your training)
    class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
    
    print("=" * 60)
    print("Raspberry Pi Edge AI Waste Classification")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Classes: {class_names}")
    print("=" * 60)
    
    try:
        # Initialize classifier
        classifier = RaspberryPiWasteClassifier(args.model, class_names)
        
        if args.image:
            # Test single image
            classifier.test_single_image(args.image)
        else:
            # Run camera inference
            classifier.run_camera_inference(
                camera_index=args.camera,
                display=not args.no_display
            )
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 