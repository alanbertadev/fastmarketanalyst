#!/bin/bash

#
# Run daily
# Execute the python cron.py in app folder. Fail if Yahoo-ticker-symbol-downloader submodule has not been sync'd

SCRIPT=$(readlink -f "$0")
BASEPATH=$(dirname "$SCRIPT")

LOCKFILE=$(echo $BASEPATH)/.staging-symbols/.LOCK_STAGING_SYMBOLS
if [ -f $LOCKFILE ];
then
    echo ".staging-symbols directory .LOCK_STAGING_SYMBOLS file exists, aborting"
    exit
fi

# Create .staging-symbols directory if not exists
mkdir -p $(echo $BASEPATH)/.staging-symbols
touch $(echo $BASEPATH)/.staging-symbols/.LOCK_STAGING_SYMBOLS

CHECK_YAHOO_SYMBOL_DOWNLOADER=$(echo $BASEPATH)/Yahoo-ticker-symbol-downloader/README.rst
 
if [ -f $CHECK_YAHOO_SYMBOL_DOWNLOADER ];
then

    STAGING_SYMBOLS=$(echo $BASEPATH)/.staging-symbols
    YAHOO_TICKER_OUTPUT=$(echo $BASEPATH)/Yahoo-ticker-symbol-downloader
    
    # Move files from staging into processing folder (Yahoo-ticker-symbol-downloader)
    FILTER=$(find $STAGING_SYMBOLS -type f \( -name "Stock*" \) )
    
    echo ${FILTER}
    #
    # THIS FILTERING SHIT IS NOT WORKING, WE NEED TO FILTER THE FILES AND MOVE THEM ONLY IF THEY EXIST. KTHANKS
    #
    #
    
    if [ -z ${FILTER} ]; then
        mv $(echo $BASEPATH)/.staging-symbols/Stock* $(echo $BASEPATH)/Yahoo-ticker-symbol-downloader/
    fi
    FILTER=$(find $STAGING_SYMBOLS -type f \( -name "downloader*" \) )
    if [ -z ${FILTER} ];
    then
        mv $(echo $BASEPATH)/.staging-symbols/downloader* $(echo $BASEPATH)/Yahoo-ticker-symbol-downloader/
    fi
    #if [ -f $STAGING_SYMBOL_DOWNLOADER ];
    #then
    #    mv $STAGING_SYMBOL_DOWNLOADER $(echo $BASEPATH)/Yahoo-ticker-symbol-downloader/
    #fi

    SCRIPTPATH=$(echo $BASEPATH)/app/cron.py
    python $SCRIPTPATH
    
    # Move stock download files back into .staging-symbols (to adhere to .gitignore)
    FILTER=$(find $YAHOO_TICKER_OUTPUT -type f \( -name "Stock*" \) )
    if [ -z ${FILTER} ];
    then
        mv $(echo $BASEPATH)/Yahoo-ticker-symbol-downloader/Stock* $(echo $BASEPATH)/.staging-symbols/
    fi
    FILTER=$(find $YAHOO_TICKER_OUTPUT -type f \( -name "downloader*" \) )
    if [ -z ${FILTER} ];
    then
        mv $(echo $BASEPATH)/Yahoo-ticker-symbol-downloader/downloader* $(echo $BASEPATH)/.staging-symbols/
    fi
        
else
   echo "Yahoo-ticker-symbol-downloader not initialized!"
fi

rm $(echo $BASEPATH)/.staging-symbols/.LOCK_STAGING_SYMBOLS

