run:
	bundle exec jekyll serve --watch

prepare:
	gem install bundler jekyll
	sudo gem install -n /usr/local/bin jekyll
	bundle install
