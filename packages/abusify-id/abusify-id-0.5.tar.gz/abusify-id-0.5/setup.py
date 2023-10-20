from setuptools import setup, find_packages

setup(
    name='abusify-id',
    version='0.5',
    packages=find_packages(),
    package_data={
        'abusify_id': ['model.pkl', 'tfidf_vectorizer.pkl'],
    },
    install_requires=[
        'scikit-learn',
        'pandas',
        'nltk',
        'pymysql',
    ],
)
