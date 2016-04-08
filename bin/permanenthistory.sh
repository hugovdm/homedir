#
# "Borrowed" from lvd, thanks! ;)
#
# source this file in your .bashrc to get a permanent record of your shell history.
# e.g.
#   if [ -f ~/bin/permanenthistory.sh  ]; then
#        . ~/bin/permanenthistory.sh
#   fi
#
# see bin/hh for a quick way to grep through your history.
#  tip: make notes to yourself with shell comments ###
#

[ -d ~/history ] || mkdir ~/history

export HOST_SHORT=$(hostname -s)

# add a line to the history log
function hl {
    local ts=$(date +%H:%M:%S)
    echo "${USER}@${HOST_SHORT} $$ ${ts}" "$@" | cut -c1-2000 >> ${HOME}/history/$(date +%Y%m%d).log
}

# add several lines to your history log, useful to record outputs of programs
# eg  ls -l | hc "what the directory looked like"
function hc {
    hl "$@"
    awk '{print "\t"$0}' >> ${HOME}/history/$(date +%Y%m%d).log
}

# tail your history. see also hh
function ht {
    tail "$@" ${HOME}/history/$(date +%Y%m%d).log
}

hl "# new shell $$"

export PROMPT_COMMAND='hl $(history 1)'
export HISTCONTROL=ignoreboth
