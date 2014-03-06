# usercode
CMSSW user code of Jan Veverka.  This is intended as an archive of the original
CVS repository.  More useful packages have been branched out into separate
git repositories

   * FWLite
   * JPsi
   * Vgamma


## History
This collection of random sources was imported from the retired CVS
repository [1] on 5 March 2014.  Originally, it used to live at [2]
and was archived at [3].

It was imported using the HEAD version of cvs2git [4] using these commands:

    MY_GITHUB_USER=`git config --get user.github`
    MY_REMOTE=git@github.com:$MY_GITHUB_USER/usercode.git
    /tmp/veverka/git/cvs2svn/cvs2git --options=cvs2git-usercode.options
    git init usercode
    cd usercode
    git remote add origin $MY_REMOTE
    cat ../git-blob.dat ../git-dump.dat | git fast-import

See also [5].  The file with the cvs2git options is stored at [6].

- [1] /afs/cern.ch/project/cvs/reps/CMSSW/UserCode/JanVeverka
- [2] http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/JanVeverka
- [3] http://cvs.web.cern.ch/cvs/cgi-bin/viewcvs.cgi/UserCode/JanVeverka/
- [4] https://github.com/mhagger/cvs2svn/commit/b0ae0c98b0d5bf4b42425799814a9712d66c0073
   - b0ae0c98b0d5bf4b42425799814a9712d66c0073
   - mhagger@b0ae0c98b0d5bf4b42425799814a9712d66c0073
   - mhagger/cvs2svn@b0ae0c98b0d5bf4b42425799814a9712d66c0073
- [5] http://cms-sw.github.io/cmssw/usercode-faq.html#how_do_i_migrate_to_github
- [6] https://github.com/janveverka/usercode/cvs2git-usercode.options

## Test

16c999e8c71134401a78d4d46435517b2271d6ac
mojombo@16c999e8c71134401a78d4d46435517b2271d6ac
mojombo/github-flavored-markdown@16c999e8c71134401a78d4d46435517b2271d6ac
#1
mojombo#1
mojombo/github-flavored-markdown#1

