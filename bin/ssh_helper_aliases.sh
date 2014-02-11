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
        ua*) the_env=uat
            ;;
        u*) the_env=utility
            ;;
        a*) the_env=analytics
            ;;
        tpp*) the_env=testprep-production
            ;;
        tps*) the_env=testprep-staging
            ;;
        rs*) the_env=readiness-staging
            ;;
        rp*) the_env=readiness-production
            ;;
        *)
            echo "Usage: hss <environment abbreviation> <ssh_helper commands> "
            echo "You haven't entered one of the valid environments. "
            echo "You can use the following: p,s, ua, u, a, tpp, tps, rp, rs"
            echo  "(for production, staging, uat, utilty, analytics, testprep-prod/staging, or readiness-prod/staging )"
            return 2
            ;;
    esac
    ssh_helper -e $the_env $*
}
