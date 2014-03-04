# The hss function (ssh backwards) is to make accessing ssh helper commands
# able to co-exist in case you already have other commands defined that use
# e.g. ussh or pssh, etc.  If you do, then comment out the aliases
# you don't want above for yourself, and source this file at startup.
function hss () {
    arg1="$1"
    shift
    case $arg1 in
        p*) the_env=production
            ;;
        s*) the_env=staging
            ;;
        *)
            echo "Usage: hss <environment abbreviation> <ssh_helper commands> "
            echo "You haven't entered one of the valid environments. "
            echo "You can use the following: p,s"
            echo  "(for production, staging )"
            return 2
            ;;
    esac
    ssh_helper -e $the_env $*
}
