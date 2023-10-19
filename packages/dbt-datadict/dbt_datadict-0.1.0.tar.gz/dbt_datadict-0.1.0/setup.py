# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datadict']

package_data = \
{'': ['*'], 'datadict': ['templates/*']}

install_requires = \
['click>=7.0,<8.1.4', 'ruamel.yaml>=0.17.35,<0.18.0']

entry_points = \
{'console_scripts': ['datadict = datadict:cli']}

setup_kwargs = {
    'name': 'dbt-datadict',
    'version': '0.1.0',
    'description': 'Python CLI for automating the application of consistent field definitions to large multi-layered dbt projects.',
    'long_description': "# dbt datadict\n\ndbt-datadict is a command-line tool that provides helpful tools to improve the process of managing column-level documentation across a large dbt project. It has the following key features:\n\n1. It works alongside dbt-labs/codegen to automate the model documentation creation process. By reviewing the models it can find, it uses codegen to identify the full column list and will merge this with what is already existing ikn the project, adding any missing models to a given file path.\n2. It will analyse your existing dbt project for model yaml files, and for each column summarise the different column description versions, and models that the column appears in. Once set in the dictionary, it will automatically apply descriptions for all columns with the same name (or alias) across the project.\n\n## **Installation**\n\n1. Install dbt data dictionary using\n    \n    ```bash\n    $ python -m pip install dbt-datadict\n    ```\n2. Start using the `datadict` CLI command.\n    ```bash\n    $ datadict --help\n    ```\n\n## Getting Started\n\n[Full user guide](docs/user_guide.md)\n\n### Command: `generate`\n\nThis command generates yaml files using the dbt-codegen package. Where it finds existing model yaml files, it will merge the full column lists. For missing models, it will create a separate model yaml file using the name provided.\n\n> **Warning**\n> This command will only run in a valid dbt project with the dbt-labs/codegen dbt package installed.\n\n#### **Usage:**\n```bash\n$ datadict generate [-D <DIRECTORY>] [-f <NAME>] \n```\n\n#### **Options:**\n\n- **`-D, --directory <DIRECTORY>`**: Directory to apply the dictionary. Default: 'models/'.\n- **`-f, --file <NAME>`**: The file to store any new models in.\n- **`--sort`**: Triggers the generated YAML files to be sorted alphabetically (on by default). \n\n### Command: **`apply`**\n\nThis command applies data dictionary updates to all model YAML files in the specified directory and its subdirectories.\n\n#### **Usage:**\n```bash\n$ datadict apply [-D <DIRECTORY>] [-d <DICTIONARY>] \n```\n\n#### **Options:**\n\n- **`-D, --directory <DIRECTORY>`**: Directory to apply the dictionary. Default: 'models/'.\n- **`-d, --dictionary <DICTIONARY>`**: Location of the dictionary file. Default: 'datadictionary.yml'.\n\n\n\n## **Important Note**\n\nIt is highly recommend to only use this library in a version controlled environment, such as git. Additionally, please ensure that you have backed up your model YAML files and data dictionary before applying any updates. The application modifies files in place and does not create backups automatically.\n\nUse this application responsibly and verify the updates before proceeding.\n\n## Contributing\nWe encourage you to contribute to dbt Data Dictionary! Please check out our [Contributing to dbt Data Dictionary](CONTRIBUTING.md) guide for guidelines about how to proceed.\n\n## License\n\ndbt Data Dictionary is released under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.\n",
    'author': 'tom',
    'author_email': 'tom@tasman.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TasmanAnalytics/dbt-datadictionary',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
