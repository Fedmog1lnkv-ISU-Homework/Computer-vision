# Линейный градиент

Написать программу для генерации двухмерного массива значения которого вычисляются как линейный градиент от одного цвета к другому.
Градиент должен быть повернут на 45 градусов, т.е. идти из левого верхнего угла в правый нижний.

В результате должно получится:

![img.png](src/example.png)

Код для генерации градиента сверху вниз:

```python
import numpy as np
import matplotlib.pyplot as plt

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

size = 100
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]

color1 = [255, 128, 0]
color2 = [0, 128, 255]

for i, v in enumerate(np.linspace(0, 1, image.shape[0])):
    r = lerp(color1[0], color2[0], v)
    g = lerp(color1[1], color2[1], v)
    b = lerp(color1[2], color2[2], v)
    image[i, :, :] = [r, g, b]

plt.figure(1)
plt.imshow(image)
plt.show()
```

Результат:
![img.png](src/result.png)null