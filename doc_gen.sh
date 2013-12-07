#!/bin/bash
epydoc -v --html app.oal -o service/docs
mv service/docs/index.html service/docs/index.html.old
mv service/docs/app.oal.OnlineApplicationLayer-class.html service/docs/index.html