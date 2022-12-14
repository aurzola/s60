
#include <aputils.h> 
#include <apsettingshandlerui.h> 
#include <e32base.h>
#include <commdbconnpref.h>

#include "ConnManager.h"
#include "logger.h"

 

CConnManager::CConnManager():CActive(EPriorityStandard)
{
	CActiveScheduler::Add(this);
}

CConnManager::~CConnManager()
{	
	Cancel();
	if (iTimer)
		{
		iTimer->Cancel();
		}
	delete iTimer;

    iPort.Close();
    iServer.Close();		
	
	delete iWaitLoop;	
}

CConnManager*  CConnManager::NewL()
	{
	CConnManager* ctrl = new (ELeave) CConnManager;
	CleanupStack::PushL(ctrl);
	ctrl->ConstructL();
	CleanupStack::Pop(ctrl);
	return ctrl;
	}

void CConnManager::ConstructL()
{
	iWaitLoop = new (ELeave) CActiveSchedulerWait;
	iTimer = CTimeOutTimer::NewL(EPriorityStandard, *this);
}


void CConnManager::ConnectL()
{
	User::LeaveIfError(iServer.Connect());
    
    TCommConfig ConfigBuf;
    TCommConfigV01& Config = ConfigBuf();

    Config.iRate = EBps115200;
    Config.iDataBits = EData8;
    Config.iStopBits = EStop1;
    Config.iParity = EParityNone;
    Config.iHandshake = 0;
    Config.iTerminatorCount = 0;

    User::LeaveIfError(iPort.Open(iServer, _L("ACM::0"), ECommExclusive, ECommRoleDCE));    
    iPort.SetConfig(ConfigBuf);

}

void CConnManager::CloseL()
{
    Cancel();
    iPort.Close();
    iServer.Close();
}


void CConnManager::RunL()
{
	iWaitLoop->AsyncStop();
	iTimer->Cancel();
}

void CConnManager::DoCancel()
{
	iPort.Cancel();
}

void CConnManager::RecvL(TDes8& aBuffer, TInt aTimeout)
{
    iPort.ReadOneOrMore(iStatus, aBuffer);
	SetActive();
	if (aTimeout)
	{
		iTimer->After(aTimeout);
	}
	iWaitLoop->Start();
	
	if (iStatus != KErrEof)
		{		
		// if not KErrNone or KErrEof, leave with error
		User::LeaveIfError(iStatus.Int());
		}	
}

void CConnManager::SendL(const TDesC8& aBuffer, TInt aTimeout)
{
    iPort.Write(iStatus, aBuffer);
	SetActive();
	if (aTimeout)
	{
		iTimer->After(aTimeout);
	}
	
	iWaitLoop->Start();
	User::LeaveIfError(iStatus.Int());
}


void CConnManager::TimerExpired()
	{
	Cancel();
	iStatus = KErrTimedOut;
	iWaitLoop->AsyncStop();
	}
