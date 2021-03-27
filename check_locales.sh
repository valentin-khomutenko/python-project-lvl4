if [[ `git status task_manager/locale --porcelain` ]]; then
  echo "locales is not up to date, did you run 'make locales && make compiled-locales'?"
  exit 1
fi
