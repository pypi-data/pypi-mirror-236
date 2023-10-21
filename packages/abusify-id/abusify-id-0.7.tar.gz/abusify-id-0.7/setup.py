from setuptools import setup, find_packages

setup(
    name='abusify-id',
    version='0.7',
    packages=find_packages(),
    package_data={
        'abusify_id': ['.env', 'model.pkl', 'tfidf_vectorizer.pkl'],
    },
    install_requires=[
        'scikit-learn',
        'pandas',
        'nltk',
        'pymysql',
        'python-decouple',
    ],
)
