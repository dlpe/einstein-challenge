coverage run -m unittest discover
coverage report -m --omit "*test*","*site-packages*"
