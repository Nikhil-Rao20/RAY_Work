import ray
import numpy as np
import time

ray.init()

total_pixels_processed =0 # Our global counter

@ray.remote
def process_image_and_count(image: np.ndarray) -> np.ndarray:
    global total_pixels_processed
    # Update the global counter
    total_pixels_processed += image.size
    time.sleep(1)
    return 255 - image

images = [np.random.randint(0,255, (10, 10, 3)) for _ in range(4)]
image_size=  images[0].size

ray.get([process_image_and_count.remote(img) for img in images])

print(f"\nExpected total pixels: {image_size * 4}")
print(f"Actual total pixels processed in main script: {total_pixels_processed}")

ray.shutdown()