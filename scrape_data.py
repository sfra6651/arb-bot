#!!!!RUN ALL SCRIPTS AND DELETE PREVIOUS DATA!!!!
from library import clean_path, get_file_paths, run_js_scripts

paths = get_file_paths('scripts/rugby_union')
clean_path('data/rugby_union')
run_js_scripts(paths)
