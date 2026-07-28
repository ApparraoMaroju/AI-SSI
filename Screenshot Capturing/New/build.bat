@echo off
echo =============================================
echo Screenshot Tool - Build Script
echo =============================================
echo.

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Creating directories...
if not exist "lib" mkdir lib
if not exist "build" mkdir build
if not exist "build\classes" mkdir build\classes

echo.
echo Downloading Apache POI dependencies...
echo.

:: Download Apache POI and dependencies
set POI_VERSION=5.2.5
set POI_URL=https://repo1.maven.org/maven2/org/apache/poi

:: Main POI libraries
powershell -Command "if (!(Test-Path 'lib\poi-%POI_VERSION%.jar')) { Invoke-WebRequest -Uri '%POI_URL%/poi/%POI_VERSION%/poi-%POI_VERSION%.jar' -OutFile 'lib\poi-%POI_VERSION%.jar' }"
powershell -Command "if (!(Test-Path 'lib\poi-ooxml-%POI_VERSION%.jar')) { Invoke-WebRequest -Uri '%POI_URL%/poi-ooxml/%POI_VERSION%/poi-ooxml-%POI_VERSION%.jar' -OutFile 'lib\poi-ooxml-%POI_VERSION%.jar' }"
powershell -Command "if (!(Test-Path 'lib\poi-ooxml-lite-%POI_VERSION%.jar')) { Invoke-WebRequest -Uri '%POI_URL%/poi-ooxml-lite/%POI_VERSION%/poi-ooxml-lite-%POI_VERSION%.jar' -OutFile 'lib\poi-ooxml-lite-%POI_VERSION%.jar' }"

:: XMLBeans
set XMLBEANS_VERSION=5.2.0
powershell -Command "if (!(Test-Path 'lib\xmlbeans-%XMLBEANS_VERSION%.jar')) { Invoke-WebRequest -Uri 'https://repo1.maven.org/maven2/org/apache/xmlbeans/xmlbeans/%XMLBEANS_VERSION%/xmlbeans-%XMLBEANS_VERSION%.jar' -OutFile 'lib\xmlbeans-%XMLBEANS_VERSION%.jar' }"

:: Commons libraries
powershell -Command "if (!(Test-Path 'lib\commons-compress-1.25.0.jar')) { Invoke-WebRequest -Uri 'https://repo1.maven.org/maven2/org/apache/commons/commons-compress/1.25.0/commons-compress-1.25.0.jar' -OutFile 'lib\commons-compress-1.25.0.jar' }"
powershell -Command "if (!(Test-Path 'lib\commons-io-2.15.1.jar')) { Invoke-WebRequest -Uri 'https://repo1.maven.org/maven2/commons-io/commons-io/2.15.1/commons-io-2.15.1.jar' -OutFile 'lib\commons-io-2.15.1.jar' }"
powershell -Command "if (!(Test-Path 'lib\commons-collections4-4.4.jar')) { Invoke-WebRequest -Uri 'https://repo1.maven.org/maven2/org/apache/commons/commons-collections4/4.4/commons-collections4-4.4.jar' -OutFile 'lib\commons-collections4-4.4.jar' }"

:: Log4j API (required by POI)
powershell -Command "if (!(Test-Path 'lib\log4j-api-2.22.1.jar')) { Invoke-WebRequest -Uri 'https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.22.1/log4j-api-2.22.1.jar' -OutFile 'lib\log4j-api-2.22.1.jar' }"

echo.
echo Dependencies downloaded.
echo.

echo Compiling Java source...
javac -d build\classes -cp "lib\*" src\ScreenshotTool.java
if errorlevel 1 (
    echo Compilation failed!
    pause
    exit /b 1
)

echo Compilation successful.
echo.

echo Creating fat JAR with all dependencies...
cd build\classes

:: Extract all dependency JARs
for %%f in (..\..\lib\*.jar) do (
    echo Extracting %%f...
    jar xf "%%f"
)

:: Remove signature files to avoid conflicts
if exist META-INF\*.SF del META-INF\*.SF
if exist META-INF\*.DSA del META-INF\*.DSA
if exist META-INF\*.RSA del META-INF\*.RSA

cd ..\..

:: Create the final JAR
echo Creating final JAR...
jar cfm ScreenshotTool.jar MANIFEST.MF -C build\classes .

if errorlevel 1 (
    echo JAR creation failed!
    pause
    exit /b 1
)

echo.
echo =============================================
echo Build complete! 
echo JAR file: %SCRIPT_DIR%ScreenshotTool.jar
echo =============================================
echo.
echo To run: java -jar ScreenshotTool.jar
echo.
pause
