@ECHO OFF
CD /D "%~DP0"
VER | FIND /I "XP"
IF %ERRORLEVEL%==0 (SET GAMEARCHIVES="C:\Documents and Settings\%USERNAME%\Application Data\Macromedia\Flash Player") ELSE (SET GAMEARCHIVES="C:\Users\%USERNAME%\AppData\Roaming\Macromedia\Flash Player")
ECHO %GAMEARCHIVES%
START "" %GAMEARCHIVES%
PAUSE
EXIT /B