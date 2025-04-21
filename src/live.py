"""
MIT License
Created on: 2025-04-21
Author: André Reis <andre.lgr@gmail.com>
"""

import cv2

from halation_engine import HalationEngine

class LiveDemo():

    def run(self):
        halation_engine = HalationEngine()

        # Initialize the webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open webcam.")
            exit()

        # Create a window for the sliders
        cv2.namedWindow('Film Look Halation Effect')

        while True:
            # Capture frame from webcam
            ret, frame = cap.read()
            if not ret:
                break

            # Apply the halation effect
            frame_with_halation, halo, highlight_mask, glow = halation_engine.apply_advanced_halation(frame)

            # Display the resulting frame
            cv2.imshow('Film Look Halation Effect', frame_with_halation)
            cv2.imshow('Halo', halo)
            cv2.imshow('Highlight Mask', highlight_mask)
            cv2.imshow('Glow', glow)

            # Wait for the user to press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = LiveDemo()
    app.run()
