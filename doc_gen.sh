#!/bin/bash
rm service/docs/*
epydoc -v --html app.oal -o service/docs
mv service/docs/index.html service/docs/index.html.old
mv service/docs/app.oal.OnlineApplicationLayer-class.html service/docs/index.html

python app/docs/doc_gen_utils.py service/docs/index.html