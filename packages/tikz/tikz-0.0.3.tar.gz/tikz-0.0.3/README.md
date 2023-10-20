# Ti*k*Z Figure Generator

The following is a code example for creating a plot with this library::

```python
import numpy as np
import tikz

K = 1000
x = np.linspace(0, 1.001, K)
y = 3*np.sin(2*np.pi*x) + 0.5*np.random.randn(K)
z = 3*np.cos(2*np.pi*x) + 0.5*np.random.randn(K)
u = np.zeros((2, K))
u[0, :] = np.row_stack((y, z)).min(axis=0) - 2
u[1, :] = np.row_stack((y, z)).max(axis=0) + 2

fig = tikz.Fig('test')
fig.xlabel = 'x axis'
fig.ylabel = 'y axis'
fig.path(x, u, thickness=0, opacity=0.2)
fig.path(x, y, label='first')
fig.path(x, z, label='second')
fig.render()
```

First, a figure object is created with `tikz.Fig()`. This object holds settings
pertaining to the whole figure, like the width, height, and font size. Second,
path objects are created with `fig.path()`, which creates a `Path` object and
appends it to the list of path objects held by the `Fig` object. This object
holds everything pertaining to a particular path, like the `x` and `y` arrays,
the `thickness`, `color`, `opacity`, `dash` style, and `label`. To render the
figure, pass the list of paths to the figure object with the `.render()` method.
Note, the default setting is for the LaTeX file to be generated as a standalone
file with its own document class declaration and preamble. When it is
standalone, this Python library will then try to automatically compile the LaTeX
file with the `pdflatex` command. If `standalone` is set to `False` then only
the TikZ draw commands will be included. This file can then be `input` within
the `tikzpicture` environment of another LaTeX file.
