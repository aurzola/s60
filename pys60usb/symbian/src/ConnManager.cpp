
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

_LIT(KConnFormat, "%S::%d");
void CConnManager::ConnectL( TDesC& aPortType, TInt aPort, TInt aMode, TInt aRole )
{
	
  User::LeaveIfError(iServer.Connect());
  
  TCommConfig ConfigBuf;
  TCommConfigV01& Config = ConfigBuf();

  Config.iRate              = EBps115200;
  Config.iDataBits          = EData8;
  Config.iStopBits          = EStop1;
  Config.iParity            = EParityNone;
  Config.iHandshake         = 0;
  Config.iTerminatorCount   = 0;
  
  TBuf<64> connection_string;
  connection_string.Format( KConnFormat, &aPortType, aPort );
  
  TInt err = KErrNone;
  err = iPort.Open( iServer, 
                    connection_string, 
                    TCommAccess(aMode), 
                    TCommRole(aRole) );
  User::LeaveIfError( err );
  iPort.SetConfig(ConfigBuf);
}

void CConnManager::CloseL()
{
  if (iWaitLoop->IsStarted())
  {
    iWaitLoop->AsyncStop();
  }

  iTimer->Cancel();
  
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

void CConnManager::IsErrorL(TInt aStatus) {
    // KErrEof        = data channel closed, not an error condition
    // KErrInUse      = Don't let this block the use of usbconsole. Just try again.
    // -6710, -6709   = Cable disconnected. TODO: Add different error levels at init
    if ( aStatus != KErrEof && aStatus != KErrInUse)
    {
        User::LeaveIfError( aStatus );
    }
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

    IsErrorL( iStatus.Int() );	
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
    
	IsErrorL( iStatus.Int() );	
}


void CConnManager::TimerExpired()
{
	Cancel();
	iWaitLoop->AsyncStop();
}
