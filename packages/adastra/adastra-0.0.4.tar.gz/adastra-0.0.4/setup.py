# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astra', 'astra.core', 'astra.core.ops']

package_data = \
{'': ['*']}

install_requires = \
['jax', 'pybind11', 'torch', 'torchvision', 'triton']

entry_points = \
{'console_scripts': ['compile_gelu = build:build']}

setup_kwargs = {
    'name': 'adastra',
    'version': '0.0.4',
    'description': 'Astra - Pytorch',
    'long_description': '# Astra\nAstra is an language/compiler designed to unleash the true power of artificial intelligence blending the best techniques from Jax, Triton, and Mojo to create the most premier experience.\n\nThe evolution of JAX and Triton could lead to a next-generation language for AI development that combines the best features of both, while also introducing new capabilities to meet the evolving needs of the AI community. Let\'s call this hypothetical language "Astra", here would be some features that we would need to move things forward.\n\n# Install\n`pip install adastra`\n\n# Usage\n  \n```python\nfrom astra import astra\nimport torch\nfrom torch import nn\n\ndata = torch.randn(2, 3)    \n\n@astra # 100x+ boost in performance and speed.\ndef forward(x):\n    softmax = nn.Softmax(dim=1)\n    result = softmax(x)\n    return result\n\n\nresult = forward(data)\nprint(result)\n```\n\n## Main Features\n\n1.  🔄\xa0Differentiable Programming:\xa0Support for automatic differentiation and vectorization.\n\n2.  🎮\xa0GPU Programming:\xa0Low-level access to GPU kernels for efficient code execution.\n\n3.  🧩\xa0High-level Abstractions:\xa0Pre-defined layers, loss functions, optimizers, and more for common AI tasks.\n\n4.  🌳\xa0Dynamic Computation Graphs:\xa0Support for models with variable-length inputs or control flow.\n\n5.  🌐\xa0Distributed Computing:\xa0Built-in support for scaling AI models across multiple GPUs or machines.\n\n---\n\n\n## Requirements for Astra:\n\n1.  Differentiable Programming:\xa0Like JAX, Astra should support automatic differentiation and vectorization, which are crucial for gradient-based optimization and parallel computing in AI.\n\n2.  GPU Programming:\xa0Astra should provide low-level access to GPU kernels like Triton, allowing developers to write highly efficient code that can fully utilize the power of modern GPUs.\n\n3.  High-level Abstractions:\xa0Astra should offer high-level abstractions for common AI tasks, making it easier to build and train complex models. This includes pre-defined layers, loss functions, optimizers, and more.\n\n4.  Dynamic Computation Graphs:\xa0Unlike static computation graphs used in TensorFlow, Astra should support dynamic computation graphs like PyTorch, allowing for more flexibility in model design, especially for models with variable-length inputs or control flow.\n\n5.  Distributed Computing:\xa0Astra should have built-in support for distributed computing, enabling developers to scale their AI models across multiple GPUs or machines with minimal code changes.\n\n6.  Interoperability:\xa0Astra should be able to interoperate with popular libraries in the Python ecosystem, such as NumPy, Pandas, and Matplotlib, as well as AI frameworks like TensorFlow and PyTorch.\n\n7.  Debugging and Profiling Tools:\xa0Astra should come with robust tools for debugging and profiling, helping developers identify and fix performance bottlenecks or errors in their code.\n\n8.  Strong Community and Documentation:\xa0Astra should have a strong community of developers and comprehensive documentation, including tutorials, examples, and API references, to help users get started and solve problems.\n\n## How to Build Astra:\n\nBuilding Astra would be a significant undertaking that requires a team of experienced developers and researchers. Here are some steps we can begin with.\n\n1.  Design the Language:\xa0The team should start by designing the language\'s syntax, features, and APIs, taking into account the requirements listed above.\n\n2.  Implement the Core:\xa0The team should then implement the core of the language, including the compiler, runtime, and basic libraries. This would likely involve writing a lot of low-level code in languages like C++ or CUDA.\n\n3.  Build High-Level Libraries:\xa0Once the core is in place, the team can start building high-level libraries for tasks like neural network training, reinforcement learning, and data preprocessing.\n\n4.  Test and Optimize:\xa0The team should thoroughly test Astra to ensure it works correctly and efficiently. This might involve writing benchmarking scripts, optimizing the compiler or runtime, and fixing bugs.\n\n5.  Write Documentation:\xa0The team should write comprehensive documentation to help users learn how to use Astra. This might include API references, tutorials, and example projects.\n\n6.  Build a Community:\xa0Finally, the team should work to build a community around Astra. This might involve hosting workshops or tutorials, contributing to open-source projects, and providing support to users.\n\n# Conclusion\n- If Astra is something you would want to use, an ultra beautiful and simple language to unleash limitless performance for AI models, please star and share with all of your friends and family because if this repository gains support we\'ll build it.\n\n[Join Agora to talk more about Astra and unleashing the true capabilities of AI](https://discord.gg/qUtxnK2NMf)\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/astra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
