@REM cd  "%USERPROFILE%\Dropbox\Etudes\2021\_Website\sebast759.github.io"
cd /d "%~dp0"
echo %git_command%
git add --all
git commit -m "seb_benq_commit"
git pull
git push


ECHO waiting 5 seconds...
CHOICE /C:AB /D A /T 8 > NUL