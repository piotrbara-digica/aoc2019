import sys
from functools import partial, reduce
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

debug = partial(print, file=sys.stderr)
# find the layer that contains the fewest 0 digits.
# On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
image = np.array([int(d) for d in Path('input8.txt').read_text().strip()]).reshape((100, 25 * 6))
fewest_zeros_layer = np.argmin(np.sum(image == 0, axis=1))
layer = image[fewest_zeros_layer]
print((layer == 1).sum() * (layer == 2).sum())

BLACK, WHITE, TRANSPARENT = 0, 1, 2
decoded = reduce(lambda a, b: np.where(a < 2, a, b), image)
plt.imshow(decoded.reshape(6, 25))
plt.show()