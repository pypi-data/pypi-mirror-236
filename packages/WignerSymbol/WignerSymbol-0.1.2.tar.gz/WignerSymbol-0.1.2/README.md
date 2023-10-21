# WignerSymbol-pybind11

Python bindings for [0382/WignerSymbol](https://github.com/0382/WignerSymbol).

## Example

```python
import WignerSymbol as ws
ws.init(20, "Jmax", 3) # init the binomial coefficient table for later calculation
ws.CG(1,1,2,-1,1,0) # 0.7071067811865476
```