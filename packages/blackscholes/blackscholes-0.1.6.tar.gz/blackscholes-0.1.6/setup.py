# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackscholes', 'blackscholes.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'blackscholes',
    'version': '0.1.6',
    'description': 'Black Scholes calculator for Python including all Greeks',
    'long_description': '# blackscholes\n\n![](https://img.shields.io/pypi/dm/blackscholes) | \n![](https://img.shields.io/pypi/pyversions/blackscholes) | \n![](https://img.shields.io/codecov/c/github/carlolepelaars/blackscholes)\n\nA Black-Scholes calculator for Python that includes up to the third-order Greeks.\n\nSupports the Black-Scholes-Merton model, \nBlack-76 model and option structures.\n\n## Installation\n\n`pip install blackscholes`\n\n## Examples\n\n### Input variables\n```python3\nS = 55.0  # Asset price of 55\nK = 50.0  # Strike price of 50\nT = 1.0  # 1 Year to maturity\nr = 0.0025  # 0.25% Risk-free rate\nsigma = 0.15  # 15% Volatility\nq = 0.0 # 0% Annual Dividend Yield\n```\n\n### Call\n\n```python3\nfrom blackscholes import BlackScholesCall\ncall = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma, q=q)\ncall.price()  ## 6.339408\ncall.delta()  ## 0.766407\ncall.spot_delta() ## 0.7683\ncall.charm()  ## 0.083267\n```\n\n### Put\n\n```python3\nfrom blackscholes import BlackScholesPut\nput = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=q)\nput.price()  ## 1.214564\nput.delta()  ## -0.23359\nput.spot_delta() ## -0.23417\nput.charm()  ## 0.083267\n```\n\n### Black-76\n\nThe Black-76 model is often used specifically for options and futures and bonds.\n`blackscholes` also supports this model. To see all available greeks\ncheck out section [4. The Greeks (Black-76)](https://carlolepelaars.github.io/blackscholes/4.the_greeks_black76).\n\n**Call Example**\n```python\nfrom blackscholes import Black76Call\ncall = Black76Call(F=55, K=50, T=1, r=0.0025, sigma=0.15)\ncall.price()  ## 6.2345\ncall.delta()  ## 0.7594\ncall.vomma()  ## 45.1347\n```\n\n**Put Example**\n```python\nfrom blackscholes import Black76Put\nput = Black76Put(F=55, K=50, T=1, r=0.0025, sigma=0.15)\nput.price()  ## 1.2470\nput.delta()  ## -0.2381\nput.vomma()  ## 45.1347\n```\n\n### Structures\n\n`blackscholes` offers the following six option structures:\n- Straddle\n- Strangle\n- Butterfly\n- Iron Condor\n- Spreads\n- Iron Butterfly\n\nAll structures have a long and short version. To learn more\ncheck out section [6. Option Structures](https://carlolepelaars.github.io/blackscholes/6.option_structures).\n\n**Long Straddle Example**\n```python3\nfrom blackscholes import BlackScholesStraddleLong\n\nstraddle = BlackScholesStraddleLong(S=55, K=50, T=1.0,\n                                    r=0.0025, sigma=0.15)\nstraddle.price()  ## 7.5539\nstraddle.delta()  ## 0.5328\n```\n\n## Contributing\n\nWe very much welcome new contributions! Check out the [Github Issues](https://github.com/CarloLepelaars/blackscholes/issues)\nto see what is currently being worked on.\n\nAlso check out [Contributing](https://carlolepelaars.github.io/blackscholes/contributing) in the documentation \nto learn more about \ncontributing to [blackscholes](https://github.com/CarloLepelaars/blackscholes).\n',
    'author': 'CarloLepelaars',
    'author_email': 'info@carlolepelaars.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
