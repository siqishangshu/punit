@echo off

rem Start make punit.exe
echo Start make punit.exe

cd /d %~dp0
echo "At %CD%"

set PWD=%CD%
set CONFIG=%PWD%\config
set DIST=%PWD%\dist
set LOG=%PWD%\log
set STATIC=%PWD%\static
set TOOL=%PWD%\tool
set SCRIPT=%PWD%\script
set TARGET=%PWD%\punit
set DRIVER=%PWD%\driver
set RAR=punit-build-%PROCESSOR_ARCHITECTURE%.rar

echo now you at %PWD%

if exist "%PWD%\__pycache__" (
	echo Clean last build
	rd /s /q "%PWD%\__pycache__"
)

if exist "%PWD%\build" (
	echo Clean last build
	rd /s /q "%PWD%\build"
)
if exist "%PWD%\dist" (
	echo Clean last dist
	rd /s /q "%PWD%\dist"
)

if exist "%PWD%\punit.spec" (
	echo Clean last dist
	del /F "%PWD%\punit.spec"
)

if exist "%TARGET%" (
	echo Clean last version
	rd /s /q "%TARGET%"
)

if exist "%DRIVER%" (
	echo Clean last version
	rd /s /q "%DRIVER%"
)

md %TARGET% 
echo  %CONFIG%  %TARGET%
echo d|xcopy "%CONFIG%"  "%TARGET%\config" /e/r/h/y
echo d|xcopy "%STATIC%"  "%TARGET%\static" /e/r/h/y
echo d|xcopy "%TOOL%"  "%TARGET%\tool" /e/r/h/y
echo d|xcopy "%LOG%"  "%TARGET%\log" /e/r/h/y
echo d|xcopy "%DRIVER%"  "%TARGET%\driver" /e/r/h/y
echo Y|del "%TARGET%\log\*"
copy /Y "%SCRIPT%\punit.exe.lnk" "%TARGET%\"
copy /Y "%SCRIPT%\install.bat" "%PWD%\"
copy /Y "%SCRIPT%\uninstall.bat" "%TARGET%\"
copy /Y "%SCRIPT%\使用必读.txt" "%PWD%\"

pyinstaller -F punit.py

copy /Y "%DIST%\punit.exe" "%TARGET%\"

if exist "%RAR%" (
	echo Clean rar version
	echo Y|del "%PWD%\%RAR%"
)

"C:\Program Files\WinRAR\Rar.exe" a -df -ep1 punit-build-%PROCESSOR_ARCHITECTURE%.rar "%TARGET%"
"C:\Program Files\WinRAR\Rar.exe" a -df -ep1 punit-build-%PROCESSOR_ARCHITECTURE%.rar "%PWD%\install.bat"
"C:\Program Files\WinRAR\Rar.exe" a -ep1 punit-build-%PROCESSOR_ARCHITECTURE%.rar "%PWD%\README.md"

msg %username% /time:7  "The punit-build-%PROCESSOR_ARCHITECTURE%.rar build successfully"

echo Done