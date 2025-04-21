"""
MIT License
Created on: 2025-04-21
Author: André Reis <andre.lgr@gmail.com>
"""

import cv2
import numpy as np

class HalationEngine():
    def __init__(self):
        pass

    def normalize_image(self, image):
        img = image.astype(np.float32) / 255.0  # Normalize to [0, 1] range

        # Apply gamma correction to convert from sRGB to linear RGB
        img_lin = np.power(img, 2.2)

        return img_lin

    def apply_advanced_halation(
        self,
        image,
        highlight_threshold=0.97,
        red_boost=8,
        green_boost=1.5,
        blur_passes=[15, 35, 75],
        blend_strength=0.9,
        falloff_power=2.0,
        gamma=2.2
    ):
        img_lin = self.normalize_image(image)

        # Extract red channel for halation effect.
        red_channel = img_lin[:, :, 2]
        highlight_mask = np.clip((red_channel - highlight_threshold) / (1.0 - highlight_threshold), 0, 1)

        # Apply multi-scale Gaussian blur for glow effect.
        glow = np.zeros_like(red_channel)
        for size in blur_passes:
            blurred = cv2.GaussianBlur(highlight_mask, (size, size), 0)
            falloff = np.power(1.0 - blurred, falloff_power)
            glow += blurred * falloff
        glow /= len(blur_passes)

        # Build the red-channel halo (this is where the halation effect happens).
        halo = np.zeros_like(img_lin)

        # Add an orange tint.
        halo[:, :, 2] = glow * red_boost
        halo[:, :, 1] = glow * green_boost

        # Composite the halo with the original image (in linear space).
        final_lin = np.clip(img_lin + halo * blend_strength, 0, 1)

        # Gamma-correct to get sRGB image.
        final_srgb = np.power(final_lin, 1 / gamma)

        # Convert to 16-bit for final output.
        return (final_srgb * 65535).astype(np.uint16), halo, highlight_mask, glow
