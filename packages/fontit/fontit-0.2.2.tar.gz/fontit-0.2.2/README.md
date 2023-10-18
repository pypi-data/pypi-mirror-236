# Install

```shell
pip install fontit
```

# Usage
```python
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontit import default_font

font = ImageFont.truetype(default_font, 32, )

canvas = np.zeros((640, 640, 3), dtype=np.uint8)
canvas = Image.fromarray(canvas)
draw = ImageDraw.Draw(canvas)

draw.text((40, 40), "你好，世界！", font=font, fill=(255, 255, 255))
draw.text((40, 80), "Hello World!", font=font, fill=(255, 255, 255))

canvas.show()
```