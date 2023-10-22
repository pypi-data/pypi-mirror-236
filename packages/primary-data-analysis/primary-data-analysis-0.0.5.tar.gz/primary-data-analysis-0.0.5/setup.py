from setuptools import setup, find_packages


REQUIREMENTS = ['numpy', 'pandas', 'matplotlib', 'six', 'plotly',
                'statsmodels', 'seaborn', 'sklearn', 'setuptools']

# calling the setup function
setup(name='primary-data-analysis',
      version='0.0.5',
      description='Primary data analysis for pandas dataframe',
      long_description='Primary data analysis for pandas dataframe',
      url='https://github.com/anagha-bhople/primary_data_analysis',
      author='Anagha Bhople',
      author_email='bhoplea34@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=REQUIREMENTS,
      keywords='data analysis eda pandas'
      )
