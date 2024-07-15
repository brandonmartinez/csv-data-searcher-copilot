#!/usr/bin/env bash

set -eo pipefail

ERROR=1
WARN=2
INFO=3
DEBUG=4
declare -A log_names=([$ERROR]='ERROR' [$WARN]='WARN' [$INFO]='INFO' [$DEBUG]='DEBUG')
declare -A log_colors=([$ERROR]='31m' [$WARN]='33m' [$INFO]='37m' [$DEBUG]='90m')

LOG_LEVEL=${LOG_LEVEL:-$INFO}
LOG_DIR="$(dirname "$0")/.logs"
LOG_FILE_NAME=${LOG_FILE_NAME:-'logs.txt'}
LOG_FILE="$LOG_DIR/$LOG_FILE_NAME"

mkdir -p $LOG_DIR

function createFile() {
    local file_name=$1
    rm -f $file_name && touch $file_name
}

function log() {
    local log_level_int=$1
    local divider=$2
    local message=${@:3}

    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local log_message="[$timestamp] [${log_names[$log_level_int]:-INFO}] - $message"
    local formatted_log_message="\e[${log_colors[$log_level_int]:-37m}$log_message\e[0m"

    if [[ $log_level_int -gt $LOG_LEVEL ]]; then
        echo $log_message >> $LOG_FILE
    else
        if [[ -n $divider && $divider -eq 1 ]]; then
            echo ''
            echo -e $formatted_log_message
            echo -e "\e[${log_colors[$log_level_int]:-37m}**************************************************\e[0m"
            echo ''
        else
            echo -e $formatted_log_message
        fi
    fi
}

function error() {
    log $ERROR 0 $@
}

function warn() {
    log $WARN 0 $@
}

function info() {
    log $INFO 0 $@
}

function section() {
    log $INFO 1 $@
}

function debug() {
    log $DEBUG 0 $@
}

createFile $LOG_FILE

exec &> >(tee -a $LOG_FILE)
