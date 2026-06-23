import cv2
import time
from src.pipeline.capture import WebcamCapture
from src.pipeline.preprocessor import FramePreprocessor

def main():
    # 1. Initialize Pipeline
    print("Initializing pipeline...")
    # cap = WebcamCapture(fps=15, resolution=(640, 480))
    # Instead of cap = WebcamCapture(src=0)
    # Use a source that definitely doesn't exist
    # Change this:
    # cap = WebcamCapture(src=999)

# To this (0 is your default built-in webcam):
    cap = WebcamCapture(src=0)
    cap.start()
    
    prep = FramePreprocessor(target_size=(640, 480))
    
    print("Pipeline started. Capturing frames... (Press Ctrl+C to stop)")
    
    try:
        while True:
            # 2. Capture and Process
            raw_frame, timestamp = cap.read()
            
            if raw_frame is not None:
                processed_frame = prep.process(raw_frame)
                
                # 3. Print status to verify it's working
                print(f"[{timestamp}] Frame processed. Output shape: {processed_frame.shape}")
            
            # Control the loop frequency to match FPS
            time.sleep(1/15)
            
    except KeyboardInterrupt:
        print("\nStopping pipeline...")
    finally:
        cap.stop()
        print("Pipeline stopped successfully.")

if __name__ == "__main__":
    main()