# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarmalator']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch']

setup_kwargs = {
    'name': 'swarmalator',
    'version': '0.0.1',
    'description': 'swarmalator - Pytorch',
    'long_description': "# Swarmalator \n\nSwarmalators are a hybrid swarm oscillator system, combining features of both swarming (particles that align their spatial motion) and oscillators (units that synchronize their phase). This repository provides an implementation of the swarmalator model in a 3D environment using PyTorch.\n\n\n# Install\n\n```bash\n\n\n\n```\n\n## Overview\n\nAt the heart of the model are two main components for each swarmalator: \n1. **Spatial Position (`xi`)**: Represents where the swarmalator is in a 3D space.\n2. **Phase/Orientation (`sigma_i`)**: Defines the state or phase of the swarmalator.\n\nThe dynamics of each swarmalator are driven by interactions with its neighbors. These interactions are based on their relative spatial distances and differences in their phases.\n\n## Dynamics Explained\n\nThe dynamics of the swarmalators are governed by two main equations:\n\n1. For the spatial position (`xi`):\n    - Swarmalators are attracted or repelled based on the difference in their phases.\n    - They also experience a self-propelling force and a damping on high velocities.\n  \n2. For the phase/orientation (`sigma_i`):\n    - The phase changes based on the relative spatial positioning of the swarmalators.\n    - There's also an intrinsic phase precession and a nonlinearity which can cause the phase to wrap around.\n\nUsing the Runge-Kutta 4th order method (RK4), the system numerically integrates these dynamics over time, leading to the emergent behaviors of the swarmalators.\n\n## Visualization\n\nIn the visualization, you will witness:\n- A 3D cube that encapsulates the world of swarmalators.\n- `N` points inside this 3D space, each representing a swarmalator. The movements and dynamics of these swarmalators are based on the aforementioned interactions.\n- A mesmerizing dance of points as they evolve over time, showcasing various patterns, clusters, or scattered behaviors.\n\n## Parameters\n\nThe behavior of swarmalators can be fine-tuned using several parameters:\n- `N`: Number of swarmalators.\n- `J, alpha, beta, gamma, epsilon_a, epsilon_r, R`: Parameters that govern the strength and nature of interactions and dynamics.\n- `D`: Dimensionality of the phase/orientation.\n\n## Usage\n\nTo simulate the swarmalators, adjust the parameters as desired and run the provided script. Post-simulation, the final positions and phases of the swarmalators are printed, and the visualization can be observed.\n\n```python\nN = 100\nJ, alpha, beta, gamma, epsilon_a, epsilon_r, R = [0.1]*7\nD = 3\nxi, sigma_i = simulate_swarmalators(N, J, alpha, beta, gamma, epsilon_a, epsilon_r, R, D)\nprint(xi[-1], sigma_i[-1])\n```\n\n## Conclusion\n\nSwarmalators provide a unique and intriguing insight into systems that exhibit both swarming and synchronization behaviors. By studying and visualizing such models, we can gain a better understanding of complex systems in nature and potentially apply these insights to engineering and technological domains.\n\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/swarmalator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
