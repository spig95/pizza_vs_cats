from setuptools import setup, find_packages

setup(
    name='pizza_vs_cats',
    version='0.1',
    python_requires='>=3.8',
    packages=find_packages(
        include=['pizza_vs_cats*']
    ),
    include_package_data=True,
    package_data={'': ['data/decks/*.json']},
    entry_points={
        'console_scripts': [
            'play-pizza-vs-cats = pizza_vs_cats.game.gameplay:play_pizza_vs_cats',
        ]
    }
)
