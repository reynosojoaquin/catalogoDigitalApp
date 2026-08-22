@ECHO OFF
SETLOCAL
SET APP_HOME=%~dp0
java.exe -classpath "%APP_HOME%gradle\wrapper\gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain %*
ENDLOCAL
