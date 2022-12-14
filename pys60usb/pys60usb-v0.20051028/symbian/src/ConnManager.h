#ifndef CONNMANAGER_H
#define CONNMANAGER_H

#include <e32base.h>
#include <c32comm.h>

#include "TimeoutTimer.h"
#include "Timeoutnotifier.h"

class CConnManager : public CActive, public MTimeOutNotifier
{
public:
	static CConnManager* NewL();	
  
	void ConnectL();
	void CloseL();

	void RecvL(TDes8& aBuffer, TInt aTimeout);
	void SendL(const TDesC8& aBuffer, TInt aTimeout);

	~CConnManager();

public: // from MTimeOutNotifier
	void TimerExpired();

protected:
	CConnManager();	
	void ConstructL();

	void RunL();
	void DoCancel();

private:
    	RComm iPort;
	RCommServ iServer;
  	CActiveSchedulerWait* iWaitLoop;
  	CTimeOutTimer* iTimer;
};

#endif
