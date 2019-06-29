#!/bin/bash
###
# Created on Jun 24, 2019
#
# @author: unicman
###

set -e

################################################################################
# Constants / variables
################################################################################


KEY_DIR=~/.ssh/key.d
EXTRA_KEY_DIR=
KEY_EXPIRY=
CLEAN_SSH_AGENT=1

if [ "$1" != "" ] ; then
    KEY_EXPIRY=" -t $1 "
fi

if [ "$2" != "" ] ; then
    EXTRA_KEY_DIR=$2
fi

if [ "$3" == "--incremental" ] ; then
    CLEAN_SSH_AGENT=0
elif [ "$3" == "--clean" ] ; then
    CLEAN_SSH_AGENT=1
fi

################################################################################
# Utility functions
################################################################################

fnSshAdd()
{
    INTERNAL_KEY_DIR=$1

    if [ "${INTERNAL_KEY_DIR}" == "" ] ; then
        return
    fi

    ##
    # Add keys with no extension
    ##

    for keyFile in ${INTERNAL_KEY_DIR}/* ; do
        fileName=$(basename "${keyFile}")
        if [ -f "${keyFile}" ] && [[ ! "${fileName}" =~ "." ]] ; then
            ssh-add ${KEY_EXPIRY} "${keyFile}"
        
        # Uncomment only for debugging
        #else
        #    echo "Skipped ${keyFile}"
        fi
    done

    ##
    # Convert windows keys
    ##

    if puttygen --version > /dev/null ; then
        mkdir -p "${INTERNAL_KEY_DIR}/.cache"

        # Create RAM disk to avoid storing passphrase permanently
        pwdFile=$(mktemp /tmp/skXXXXXX)
        echo "${KEY_PWD}" > ${pwdFile}

        for ppkFile in ${INTERNAL_KEY_DIR}/*.ppk ; do
            ppkDir=$(dirname "${ppkFile}")
            fileName=$(basename "${ppkFile}")
            keyFile="${ppkDir}/.cache/${fileName%.*}"

            # Convert if not already converted...
            if [ ! -f "${keyFile}" ] && [ -f "${ppkFile}" ] ; then
                echo "Converting ${ppkFile}..."
                puttygen "${ppkFile}" -O private-openssh -o "${keyFile}" --new-passphrase ${pwdFile}
                chmod 600 "${keyFile}"
            fi

            ssh-add ${KEY_EXPIRY} "${keyFile}"
        done

        rm -f ${pwdFile}
    fi
}

################################################################################
# Main logic
################################################################################

if [ "${CLEAN_SSH_AGENT}" == "1" ] ; then
    ssh-add -D
fi

fnSshAdd "${KEY_DIR}"
fnSshAdd "${EXTRA_KEY_DIR}"
