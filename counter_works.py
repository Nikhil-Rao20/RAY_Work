import ray
import numpy as np
import time

ray.init()

@ray.remote
class PixelCounter():
    def __init__(self):
        # This is the actor's private, internal state
        self.total_pixels = 0
    
    def add(self, num_pixels: int):
        # This method will update the actor's state
        self.total_pixels += num_pixels

    def get_total(self) -> int:
        return self.total_pixels
    

@ray.remote
def process_image_with_actor(image: np.ndarray, counter) -> np.ndarray:
    
    counter.add.remote(image.size)
    time.sleep(1)

# Main Script

images = [np.random.randint(0, 255, (10, 10, 3)) for _ in range(8)]
image_size = images[0].size

# This creates the actor and returns a handle to it. A remote counter for the service running in the cluster.  
counter = PixelCounter.remote()

tasks_refs = [process_image_with_actor.remote(img, counter) for img in images]

ray.get(tasks_refs)

expected_total = len(images) * image_size
final_total_ref = counter.get_total.remote()
final_total = ray.get(final_total_ref)

print(f"Expected total pixels: {expected_total}")
print(f"Actual total from actor: {final_total}")
assert final_total == expected_total, "The total pixel count does not match the expected value!"

ray.shutdown()