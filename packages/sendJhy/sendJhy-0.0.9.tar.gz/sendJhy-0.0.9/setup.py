from setuptools import setup, find_packages

setup(
    name                = 'sendJhy',
    version             = '0.0.9',
    description         = '로컬 api sqlite db 사용, 교수 회원가입 및 기본 inNout 데이터 삽입, tree 변경',
    author              = 'lucete28',
    author_email        = '2580jhy@naver.com',
    # url                 = 'https://github.com/jeakwon/ccpy',
    # download_url        = 'https://github.com/jeakwon/ccpy/archive/0.0.tar.gz',
    install_requires    =  [        ],
    packages            = find_packages('src'),
    package_dir={'': 'src'},  # 패키지 디렉토리를 명시적으로 지정
    keywords            = ['Code','Lucete','lucete','lucete28','Lucete28','jhy'],
    python_requires     = '>=3',
    package_data        = {},
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)