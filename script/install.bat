@echo off
rem This is the logistics product component.
rem All copyright belongs to logistics.  
rem     https://www.yourdomain.com/xtool/download
rem     Author:siqishangshu@foxmail.com
rem Through the above link, you can get the latest software version and technical support.
rem If you have any questions in use, please consult yourdomain.com.

rem ---------------------------------------------------------------------------
rem Install script for the xtool Server
rem ---------------------------------------------------------------------------

echo Start install new xtool in your computer

cd /d %~dp0
echo "At %CD%"

set DIR="C:\xtool"
set PRO=xtool.exe
set LINK="C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\xtool"
set TEMP=\xtool
set PWD=%CD%

tasklist.exe -v | findstr %PRO% >NUL
if %ErrorLevel% == 0 (
	echo Stop the old Program
	taskkill.exe /F /IM %PRO% >NUL
)
sc query |find /i "xtool" >nul
if  %ErrorLevel% == 0 (
	echo Remove the old Service
	sc delete xtool >NUL
)
if exist %LINK% (
	echo Clean old link 
	rd /s /q %LINK% >NUL
)
 
if exist %DIR% (
	echo Clean old Verson Files
	rd /s /q %DIR% >NUL
)
if exist "%USERPROFILE%\Desktop\xtool.exe.lnk" (
	del /F  "%USERPROFILE%\Desktop\xtool.exe.lnk" >NUL
)

rem make new dir
md %DIR% >NUL
echo Copying
xcopy "%PWD%%TEMP%" %DIR% /e/r/h/y >NUL

ver|findstr /r /i "5.1.*" > NUL && goto WindowsXP
ver|findstr /r /i "6.1.*" > NUL && goto Windows7
ver|findstr /r /i "10.0.*" > NUL && goto Windows10
goto OtherVersion

:WindowsXP
msg %username% /time:7 "Sorry The SoftWare Not Support WindowsXP !!!"
goto TheEnd

:Windows7
echo Windows7
copy /Y "C:\xtool\xtool.exe.lnk" "%USERPROFILE%\Desktop\"
if not exist "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\xtool" (
    md "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\xtool"
)
copy /Y "C:\xtool\xtool.exe.lnk" "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\xtool\"
copy /Y "C:\xtool\uninstall.bat" "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\xtool\"
if not exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\" (
	md "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\" 
)
copy /Y  "C:\xtool\xtool.exe.lnk" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\"
goto TheEnd

:Windows10
echo Windows10
copy /Y "C:\xtool\xtool.exe.lnk" "%USERPROFILE%\Desktop\"
if not exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\xtool" (
    md "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\xtool"
)
copy /Y "C:\xtool\xtool.exe.lnk" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\xtool\"
copy /Y "C:\xtool\uninstall.bat" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\xtool\"
if not exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\" (
	md "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\"
)
copy /Y  "C:\xtool\xtool.exe.lnk" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\"
goto TheEnd

:OtherVersion
echo OtherVersion
echo try to link may not function
copy /Y "C:\xtool\xtool.exe.lnk" "%USERPROFILE%\Desktop\"
if not exist "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\xtool" (
    md "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\xtool"
)
copy /Y "C:\xtool\xtool.exe.lnk" "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\xtool\"
if not exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\" (
	md "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\" 
)
copy /Y  "C:\xtool\xtool.exe.lnk" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\"
goto TheEnd

:TheEnd
msg %username% /time:7 "The xtool install successfully"
pause
