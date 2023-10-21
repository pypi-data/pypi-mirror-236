# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['igem_lite',
 'igem_lite.epc',
 'igem_lite.epc.clarite',
 'igem_lite.epc.clarite.analyze',
 'igem_lite.epc.clarite.describe',
 'igem_lite.epc.clarite.load',
 'igem_lite.epc.clarite.modify',
 'igem_lite.epc.clarite.plot',
 'igem_lite.epc.clarite.survey',
 'igem_lite.epc.tests',
 'igem_lite.epc.tests.test_analyze',
 'igem_lite.epc.tests.test_describe',
 'igem_lite.epc.tests.test_load',
 'igem_lite.epc.tests.test_modify',
 'igem_lite.epc.tests.test_plot',
 'igem_lite.ge',
 'igem_lite.ge.db',
 'igem_lite.ge.filter',
 'igem_lite.ge.forms',
 'igem_lite.ge.management',
 'igem_lite.ge.management.commands',
 'igem_lite.ge.management.commands.olds',
 'igem_lite.ge.migrations',
 'igem_lite.ge.tests',
 'igem_lite.ge.utils',
 'igem_lite.ge.views',
 'igem_lite.load',
 'igem_lite.load.plink',
 'igem_lite.load.test',
 'igem_lite.omics',
 'igem_lite.omics.migrations',
 'igem_lite.src']

package_data = \
{'': ['*'],
 'igem_lite.epc.tests': ['py_test_output/.gitignore',
                         'py_test_output/.gitignore',
                         'py_test_output/.gitignore',
                         'py_test_output/.gitignore',
                         'py_test_output/top_results_nhanesreal.png',
                         'py_test_output/top_results_nhanesreal.png',
                         'py_test_output/top_results_nhanesreal.png',
                         'py_test_output/top_results_nhanesreal.png',
                         'py_test_output/top_results_nhanesreal_no_cutoff.png',
                         'py_test_output/top_results_nhanesreal_no_cutoff.png',
                         'py_test_output/top_results_nhanesreal_no_cutoff.png',
                         'py_test_output/top_results_nhanesreal_no_cutoff.png',
                         'py_test_output/top_results_nhanessmall.png',
                         'py_test_output/top_results_nhanessmall.png',
                         'py_test_output/top_results_nhanessmall.png',
                         'py_test_output/top_results_nhanessmall.png'],
 'igem_lite.ge': ['templates/ge/pages/*', 'templates/ge/partials/*']}

install_requires = \
['clarite==2.3.5',
 'dask>=2023.7.1,<2024.0.0',
 'django-thread>=0.0.1,<0.0.2',
 'django>=4.1.5,<5.0.0',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.66.1,<5.0.0',
 'xarray>=2023.10.1,<2024.0.0']

setup_kwargs = {
    'name': 'igem-lite',
    'version': '0.1.5',
    'description': '',
    'long_description': "\nIGEM - Integrative Genome-Exposome Method\n=========================================\n\nAn Architecture for Efficient Bioinformatics Analysis\n-----------------------------------------------------\n\n\nAbstract:\nIGEM software is a robust and scalable architecture designed for bioinformatics analysis. IGEM incorporates various modules that seamlessly work together to enable efficient data processing, analysis, and visualization. This paper explores the architecture of IGEM, including its core components, the two versions available (Server and Client), the ETL (Extraction, Transformation, and Loading) process, term replacement techniques, and the utilization of master data. Additionally, it highlights the powerful analysis functions offered by IGEM, such as dataset loading, quality control functionalities, and association and interaction analyses. The flexibility and capabilities of IGEM make it a valuable tool for researchers and practitioners in the field of omics research.\n\n1. Introduction\nThe IGEM software provides a comprehensive suite of tools for bioinformatics analysis. Its architecture is built upon a scalable and efficient framework that supports the integration and analysis of diverse omics datasets. In this paper, we delve into the various aspects of the IGEM architecture, highlighting its key components, functionalities, and advantages.\n\n2. IGEM Architecture\nThe architecture of IGEM revolves around its core modules, which enable seamless data processing, analysis, and visualization. At the heart of IGEM lies the GE-db, a multi-database that serves as the foundation of the knowledge base. This knowledge base is vital for conducting meaningful analyses and extracting valuable insights from external sources.\n\n3. IGEM Versions: Server and Client\nTo cater to different user needs, IGEM is available in two distinct versions: the IGEM Server and the IGEM Client. The IGEM Server version provides a comprehensive suite of tools for handling large-scale omics data and performing advanced analytics. On the other hand, the IGEM Client version offers a streamlined and lightweight experience, suitable for individual researchers or smaller teams focusing on specific analyses.\n\n4. ETL Process: Collect, Prepare, Map, Reduce\nThe ETL (Extraction, Transformation, and Loading) process is a crucial component of IGEM, ensuring the acquisition and preparation of data for analysis. The ETL process consists of four steps: collect, prepare, map, and reduce. In the collect step, active datasets are selected and the latest data is extracted and stored. The prepare step transforms the data into a well-structured format, while the map step establishes relationships between terms. Finally, the reduce step identifies and records terms per line, ensuring accurate and up-to-date information is stored.\n\n5. Replacing Terms: Pre-computed Mapping and IGEM Search Engine\nTo ensure consistency and accuracy in the data, IGEM employs a pre-computed term mapping approach combined with a powerful search engine. Prior to the ETL process, a mapping table is created, associating different variations and synonyms of terms with their standardized counterparts. During the term replacement step, IGEM's search engine matches terms in the data with their standardized form, ensuring coherence and alignment within the dataset.\n\n6. IGEM Master Data\nIGEM utilizes master data entries to effectively configure and manage the integration of external datasets. These entries provide essential information about each dataset, including unique identifiers, database details, field-level parameters, and hierarchical relationships among terms. Configuring field-level parameters ensures accurate interpretation of data, while establishing term hierarchies enhances organization and accessibility.\n\n7. Analysis Functions: Server and Client Versions\nBoth the IGEM Server and Client versions offer a range of analysis functions to enhance the software's capabilities. Users can load datasets, apply quality control processes, and perform association and interaction analyses. Association analysis allows users to explore relationships between variables, while interaction analysis focuses on ExE and GxE interactions. Pairwise analysis further refines the investigation of specific pairs exhibiting\nsignificant interactions.\n\n8. Conclusion\nThe IGEM software provides a robust and scalable architecture for efficient bioinformatics analysis. Its modular design, flexible functionality, and powerful analysis capabilities make it a valuable tool for researchers and practitioners in the field. By leveraging the IGEM architecture, users can seamlessly integrate omics datasets, perform comprehensive analyses, and gain valuable insights into biological systems. Further advancements and enhancements to the IGEM software will continue to propel bioinformatics research forward, driving discoveries and breakthroughs in the field of omics research.\n\n\nQuestions\n---------\n\nfeel free to open an `Issue <https://github.com/HallLab/igem/issues>`_.\n\nCiting IGEM\n--------------\n\n\nhttps://igem.readthedocs.io/en/latest/",
    'author': 'Andre Rico',
    'author_email': '97684721+AndreRicoPSU@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<3.11.0',
}


setup(**setup_kwargs)
