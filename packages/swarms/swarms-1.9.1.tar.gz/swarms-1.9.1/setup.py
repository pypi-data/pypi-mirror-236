# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarms',
 'swarms.agents',
 'swarms.apps',
 'swarms.artifacts',
 'swarms.boss',
 'swarms.chunkers',
 'swarms.embeddings',
 'swarms.hivemind',
 'swarms.memory',
 'swarms.memory.vector_stores',
 'swarms.models',
 'swarms.prompts',
 'swarms.structs',
 'swarms.swarms',
 'swarms.tools',
 'swarms.utils',
 'swarms.workers']

package_data = \
{'': ['*']}

install_requires = \
['EdgeGPT',
 'Pillow',
 'agent-protocol',
 'asyncio',
 'beautifulsoup4',
 'black',
 'chromadb',
 'dalle3',
 'diffusers',
 'duckduckgo-search',
 'einops',
 'faiss-cpu',
 'ggl',
 'google-generativeai',
 'griptape',
 'httpx',
 'langchain',
 'langchain-experimental',
 'nest_asyncio',
 'open-interpreter',
 'openai',
 'pegasusx',
 'playwright',
 'pydantic',
 'redis',
 'rich',
 'tabulate',
 'tenacity',
 'termcolor',
 'torch',
 'torchvision',
 'transformers',
 'wget']

setup_kwargs = {
    'name': 'swarms',
    'version': '1.9.1',
    'description': 'Swarms - Pytorch',
    'long_description': '![Swarming banner icon](images/swarmsbanner.png)\n\n<div align="center">\n\nSwarms is a modular framework that enables reliable and useful multi-agent collaboration at scale to automate real-world tasks.\n\n\n[![GitHub issues](https://img.shields.io/github/issues/kyegomez/swarms)](https://github.com/kyegomez/swarms/issues) [![GitHub forks](https://img.shields.io/github/forks/kyegomez/swarms)](https://github.com/kyegomez/swarms/network) [![GitHub stars](https://img.shields.io/github/stars/kyegomez/swarms)](https://github.com/kyegomez/swarms/stargazers) [![GitHub license](https://img.shields.io/github/license/kyegomez/swarms)](https://github.com/kyegomez/swarms/blob/main/LICENSE)[![GitHub star chart](https://img.shields.io/github/stars/kyegomez/swarms?style=social)](https://star-history.com/#kyegomez/swarms)[![Dependency Status](https://img.shields.io/librariesio/github/kyegomez/swarms)](https://libraries.io/github/kyegomez/swarms) [![Downloads](https://static.pepy.tech/badge/swarms/month)](https://pepy.tech/project/swarms)\n\n\n### Share on Social Media\n\n[![Join the Agora discord](https://img.shields.io/discord/1110910277110743103?label=Discord&logo=discord&logoColor=white&style=plastic&color=d7b023)![Share on Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Share%20%40kyegomez/swarms)](https://twitter.com/intent/tweet?text=Check%20out%20this%20amazing%20AI%20project:%20&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms) [![Share on Facebook](https://img.shields.io/badge/Share-%20facebook-blue)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms) [![Share on LinkedIn](https://img.shields.io/badge/Share-%20linkedin-blue)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&title=&summary=&source=)\n\n[![Share on Reddit](https://img.shields.io/badge/-Share%20on%20Reddit-orange)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&title=Swarms%20-%20the%20future%20of%20AI) [![Share on Hacker News](https://img.shields.io/badge/-Share%20on%20Hacker%20News-orange)](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&t=Swarms%20-%20the%20future%20of%20AI) [![Share on Pinterest](https://img.shields.io/badge/-Share%20on%20Pinterest-red)](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&media=https%3A%2F%2Fexample.com%2Fimage.jpg&description=Swarms%20-%20the%20future%20of%20AI) [![Share on WhatsApp](https://img.shields.io/badge/-Share%20on%20WhatsApp-green)](https://api.whatsapp.com/send?text=Check%20out%20Swarms%20-%20the%20future%20of%20AI%20%23swarms%20%23AI%0A%0Ahttps%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms)\n\n</div>\n\n\n## Purpose\nAt Swarms, we\'re transforming the landscape of AI from siloed AI agents to a unified \'swarm\' of intelligence. Through relentless iteration and the power of collective insight from our 1500+ Agora researchers, we\'re developing a groundbreaking framework for AI collaboration. Our mission is to catalyze a paradigm shift, advancing Humanity with the power of unified autonomous AI agent swarms.\n\n-----\n\n# 🤝 Schedule a 1-on-1 Session\nBook a [1-on-1 Session with Kye](https://calendly.com/apacai/agora), the Creator, to discuss any issues, provide feedback, or explore how we can improve Swarms for you.\n\n\n----------\n\n## Installation\n* `pip3 install swarms`\n\n---\n\n## Usage\nWe have a small gallery of examples to run here, [for more check out the docs to build your own agent and or swarms!](https://docs.apac.ai)\n\n### `MultiAgentDebate`\n\n- `MultiAgentDebate` is a simple class that enables multi agent collaboration.\n\n```python\nfrom swarms.workers import Worker\nfrom swarms.swarms import MultiAgentDebate, select_speaker\nfrom swarms.models import OpenAIChat\n\n\napi_key = "sk-"\n\nllm = OpenAIChat(\n    model_name=\'gpt-4\', \n    openai_api_key=api_key, \n    temperature=0.5\n)\n\nnode = Worker(\n    llm=llm,\n    openai_api_key=api_key,\n    ai_name="Optimus Prime",\n    ai_role="Worker in a swarm",\n    external_tools = None,\n    human_in_the_loop = False,\n    temperature = 0.5,\n)\n\nnode2 = Worker(\n    llm=llm,\n    openai_api_key=api_key,\n    ai_name="Bumble Bee",\n    ai_role="Worker in a swarm",\n    external_tools = None,\n    human_in_the_loop = False,\n    temperature = 0.5,\n)\n\nnode3 = Worker(\n    llm=llm,\n    openai_api_key=api_key,\n    ai_name="Bumble Bee",\n    ai_role="Worker in a swarm",\n    external_tools = None,\n    human_in_the_loop = False,\n    temperature = 0.5,\n)\n\nagents = [\n    node,\n    node2,\n    node3\n]\n\n# Initialize multi-agent debate with the selection function\ndebate = MultiAgentDebate(agents, select_speaker)\n\n# Run task\ntask = "What were the winning boston marathon times for the past 5 years (ending in 2022)? Generate a table of the year, name, country of origin, and times."\nresults = debate.run(task, max_iters=4)\n\n# Print results\nfor result in results:\n    print(f"Agent {result[\'agent\']} responded: {result[\'response\']}")\n```\n\n----\n\n### `Worker`\n- The `Worker` is an fully feature complete agent with an llm, tools, and a vectorstore for long term memory!\n- Place your api key as parameters in the llm if you choose!\n- And, then place the openai api key in the Worker for the openai embedding model\n\n```python\nfrom swarms.models import OpenAIChat\nfrom swarms import Worker\n\napi_key = ""\n\nllm = OpenAIChat(\n    openai_api_key=api_key,\n    temperature=0.5,\n)\n\nnode = Worker(\n    llm=llm,\n    ai_name="Optimus Prime",\n    openai_api_key=api_key,\n    ai_role="Worker in a swarm",\n    external_tools=None,\n    human_in_the_loop=False,\n    temperature=0.5,\n)\n\ntask = "What were the winning boston marathon times for the past 5 years (ending in 2022)? Generate a table of the year, name, country of origin, and times."\nresponse = node.run(task)\nprint(response)\n\n\n```\n\n------\n\n### `OmniModalAgent`\n- OmniModal Agent is an LLM that access to 10+ multi-modal encoders and diffusers! It can generate images, videos, speech, music and so much more, get started with:\n\n```python\nfrom swarms.models import OpenAIChat\nfrom swarms.agents import OmniModalAgent\n\napi_key = "SK-"\n\nllm = OpenAIChat(model_name="gpt-4", openai_api_key=api_key)\n\nagent = OmniModalAgent(llm)\n\nagent.run("Create a video of a swarm of fish")\n\n```\n\n- OmniModal Agent has a ui in the root called `python3 omni_ui.py`\n\n---\n\n# Documentation\nFor documentation, go here, [swarms.apac.ai](https://swarms.apac.ai)\n\n-----\n\n# ✨ Features\n* Easy to use Base LLMs, `OpenAI` `Palm` `Anthropic` `HuggingFace`\n* Enterprise Grade, Production Ready with robust Error Handling\n* Multi-Modality Native with Multi-Modal LLMs as tools\n* Infinite Memory Processing: Store infinite sequences of infinite Multi-Modal data, text, images, videos, audio\n* Usability: Extreme emphasis on useability, code is at it\'s theortical minimum simplicity factor to use\n* Reliability: Outputs that accomplish tasks and activities you wish to execute.\n* Fluidity: A seamless all-around experience to build production grade workflows\n* Speed: Lower the time to automate tasks by 90%. \n* Simplicity: Swarms is extremely simple to use, if not thee simplest agent framework of all time\n* Powerful: Swarms is capable of building entire software apps, to large scale data analysis, and handling chaotic situations\n\n\n-----\n\n## Contribute\nWe\'re always looking for contributors to help us improve and expand this project. If you\'re interested, please check out our [Contributing Guidelines](C0NTRIBUTING.md).\n\n\n\n### Optimization Priorities\n\n1. **Reliability**: Increase the reliability of the swarm - obtaining the desired output with a basic and un-detailed input.\n\n2. **Speed**: Reduce the time it takes for the swarm to accomplish tasks by improving the communication layer, critiquing, and self-alignment with meta prompting.\n\n3. **Scalability**: Ensure that the system is asynchronous, concurrent, and self-healing to support scalability.\n\nOur goal is to continuously improve Swarms by following this roadmap, while also being adaptable to new needs and opportunities as they arise.\n\n---\n\n# Demos\n\n![Swarms Demo](images/Screenshot_48.png)\n\n## Swarm Video Demo {Click for more}\n\n[![Watch the swarm video](https://img.youtube.com/vi/Br62cDMYXgc/maxresdefault.jpg)](https://youtu.be/Br62cDMYXgc)\n\n---\n\n# Contact \nFor enterprise and production ready deployments, allow us to discover more about you and your story, [book a call with us here](https://www.apac.ai/Setup-Call)',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/swarms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
