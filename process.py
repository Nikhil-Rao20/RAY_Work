import numpy as np
import time

def process_image(image: np.ndarray) -> np.ndarray:
    time.sleep(1)
    return 255-image

images = [np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8) for _ in range(8)]

start_time = time.time()
results = [process_image(img) for img in images]
end_time = time.time() 

print(f"[Using Raw Processing] : Processed {len(results)} images in {end_time - start_time:.2f} seconds")