#!/usr/bin/env python3
"""
Script para ejecutar tests de ejercicios con imágenes de test
"""

import sys
import os
from pathlib import Path
from test_exercises import TestExercises

def main():
    print("=== Fugl-Meyer Exercise Test Suite ===\n")
    
    # Check if test images directory exists
    test_images_dir = Path(__file__).parent / "test_images"
    if not test_images_dir.exists():
        print("❌ Error: 'test_images' directory not found")
        return 1
    
    # Count available images
    image_files = list(test_images_dir.glob("*.png"))
    print(f"📁 Found {len(image_files)} test images")
    
    # Initialize detector
    print("\n🔧 Initializing pose detector...")
    try:
        # Create test instance and initialize
        test_instance = TestExercises()
        test_instance.setUpClass()
    except Exception as e:
        print(f"❌ Error initializing detector: {e}")
        return 1
    
    print("✅ Detector initialized successfully")
    
    # Run tests
    print("\n🧪 Running tests...\n")
    
    results = {
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'errors': []
    }
    
    for image_file in image_files:
        image_name = image_file.name
        
        # Check mapping
        if image_name not in test_instance.image_to_exercise:
            print(f"⚠️  {image_name}: No exercise mapping")
            results['skipped'] += 1
            continue
        
        # Check if expected metrics are defined
        if image_name not in test_instance.expected_metrics:
            print(f"⚠️  {image_name}: No expected metrics defined")
            results['skipped'] += 1
            continue
        
        exercise_id = test_instance.image_to_exercise[image_name]
        
        try:
            # Process image
            score, metrics = test_instance.process_image_and_evaluate(
                image_file, exercise_id
            )
            
            if score is None:
                print(f"❌ {image_name}: No landmarks detected")
                results['failed'] += 1
                results['errors'].append(f"{image_name}: No landmarks detected")
            else:
                # Check specific metrics if defined
                metrics_ok, metric_errors = test_instance.check_metrics(image_name, metrics)
                
                if metrics_ok:
                    print(f"✅ {image_name}: {exercise_id}")
                    results['passed'] += 1
                else:
                    print(f"❌ {image_name}: {exercise_id}")
                    print(f"   📊 Metrics: {metrics}")
                    print(f"   ⚠️  Metric errors: {metric_errors}")
                    results['failed'] += 1
                    error_msg = f"{image_name}: Score {score} | Metrics: {metrics} | Errors: {metric_errors}"
                    results['errors'].append(error_msg)
                
        except Exception as e:
            print(f"💥 {image_name}: Error - {str(e)}")
            results['failed'] += 1
            results['errors'].append(f"{image_name}: {str(e)}")
    
    # Final summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print(f"{'='*50}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"⚠️  Skipped: {results['skipped']}")
    print(f"📈 Total: {results['passed'] + results['failed'] + results['skipped']}")
    
    if results['errors']:
        print(f"\n🔍 Detailed errors:")
        for error in results['errors']:
            print(f"   • {error}")
        
        print(f"\n📋 Exercise metrics summary:")
        # Group errors by exercise type
        exercise_errors = {}
        for error in results['errors']:
            # Extract exercise name from error
            if " - " in error:
                exercise_part = error.split(" - ")[1].split(" |")[0]
                if exercise_part not in exercise_errors:
                    exercise_errors[exercise_part] = []
                exercise_errors[exercise_part].append(error)
        
        for exercise, errors in exercise_errors.items():
            print(f"\n   {exercise}:")
            for error in errors:
                print(f"     {error}")
    
    success_rate = (results['passed'] / (results['passed'] + results['failed'])) * 100 if (results['passed'] + results['failed']) > 0 else 0
    print(f"\n🎯 Success rate: {success_rate:.1f}%")
    
    return 0 if results['failed'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main()) 