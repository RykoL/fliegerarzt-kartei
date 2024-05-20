##
# Project Title
#
# @file
# @version 0.1

serve:
	python -m http.server

scrape:
	poetry run python flieger_arzt_kartei/main.py

write:
	poetry run python flieger_arzt_kartei/writer.py
# end
