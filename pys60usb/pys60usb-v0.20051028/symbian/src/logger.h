#ifndef LOGGER_H
#define LOGGER_H

#ifdef __DO_LOGGING__

#include <flogger.h>

_LIT(KLogFileDir, "iapconnect");
_LIT(KLogFileName, "debug.txt"); 

#define LOG(x) {RFileLogger::Write(KLogFileDir, KLogFileName, EFileLoggingModeAppend, x);}
#define LOGF(x, y) {RFileLogger::WriteFormat(KLogFileDir, KLogFileName, EFileLoggingModeAppend, x, y);}

#else

#define LOG(x)
#define LOGF(x, y)

#endif 


#endif

