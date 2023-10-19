from setuptools import setup, find_packages

#with open('README.md', encoding='utf-8') as f: # README.md 내용 읽어오기
#	long_description = f.read()

setup(
	name='dooray',						                # module 이름
	version='0.0.1', 					                # 버전 등록
	#long_description = long_description,			    # readme.md 등록
	#long_description_content_type = 'text/markdown',    # readme.md 포맷
	description='dooray api',                           # 패키지 설명
	author='minsoo.kim',                                # 참여자 등록
	author_email='ms.kim8717@gmail.com',                # 이메일 등록
	url='https://github.com/mskim8717/dooray',          # url 등록
	license='MIT',                                      # 라이센스 등록
	python_requires='>=3.6',                            #파이썬 버전 등록
	install_requires=['requests'],                      # module 필요한 다른 module 등록
	packages=find_packages(exclude=[]),                 # 업로드할 module이 있는 폴더 입력
    keywords=['dooray', 'pydooray', 'python tutorial', 'pypi'],
	zip_safe=False,
	classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)