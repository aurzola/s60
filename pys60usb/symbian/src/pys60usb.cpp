#include <e32std.h>
#include <e32base.h>

#include "Python.h"
#include "symbian_python_ext_util.h"

#include "ConnManager.h"
#include "logger.h"

#define USBConnection_type_string "USBConnection.type_USBConnection"
#define type_USBConnection (*(PyTypeObject *)SPyGetGlobalString(USBConnection_type_string))


// type-definition
typedef struct {
    PyObject_HEAD;
    CConnManager* iConnManager;
} obj_USBConnection;


static PyObject* USBConnection_connect(obj_USBConnection* self, PyObject* args, PyObject * keywds);
static PyObject* USBConnection_send(obj_USBConnection* self, PyObject* args);
static PyObject* USBConnection_recv(obj_USBConnection* self, PyObject* args);
static PyObject* USBConnection_close(obj_USBConnection* self, PyObject* args);


// ctor (factory-function)
static PyObject* USBConnection_USBConnection(PyObject* /*self*/, PyObject * /*args*/)
{
  obj_USBConnection *Connection = PyObject_New(obj_USBConnection, &type_USBConnection);

	if (!Connection)
  {
		return 0;
  }	
	
	Connection->iConnManager = 0;
	TRAPD(err,
        Connection->iConnManager = CConnManager::NewL();		
        );	

	if (err)
  {
		PyObject_Del(Connection);		
		return SPyErr_SetFromSymbianOSErr(err);
  }

  return (PyObject*)Connection;
}

// dtor
static void dealloc_USBConnection(obj_USBConnection* Connection)
{
	delete Connection->iConnManager;
	Connection->iConnManager = 0;
  PyObject_Del(Connection);    
}
 


static const PyMethodDef USBConnection_methods[] =
{
  {"connect", (PyCFunction)USBConnection_connect, METH_VARARGS | METH_KEYWORDS},
	{"send", (PyCFunction)USBConnection_send, METH_VARARGS},    
	{"recv", (PyCFunction)USBConnection_recv, METH_VARARGS},    
	{"close", (PyCFunction)USBConnection_close, METH_NOARGS},   
  {NULL, NULL} /* sentinel */
};

static PyObject *getattr_USBConnection(PyObject *self, char *name)
{
  return Py_FindMethod(const_cast<PyMethodDef*>(&USBConnection_methods[0]), self, name);
}

static const PyTypeObject type_template_USBConnection = {
  /*******************************************************/
  PyObject_HEAD_INIT(0)    /* initialize to 0 to ensure Win32 portability */
  0,                 /*ob_size*/
  "USBConnection.USBConnection",            /*tp_name*/
  sizeof(obj_USBConnection), /*tp_basicsize*/
  0,                 /*tp_itemsize*/
  /* methods */
  (destructor)dealloc_USBConnection, /*tp_dealloc*/
  0, /*tp_print*/
  (getattrfunc)getattr_USBConnection, /*tp_getattr*/

  /* implied by ISO C: all zeros thereafter */
}; 


// Connection methods
_LIT(KDefaultConnType, "ACM" );

static PyObject* USBConnection_connect(obj_USBConnection* self, PyObject* args, PyObject * keywds)
{
	TInt   err;
	TInt   aPort          = 0;
	TChar* tmpPortType    = NULL;
	TInt   aLenPortType   = 0;
    TInt   aMode          = ECommShared;
    TInt   aRole          = ECommRoleDCE;
    
	static const char *const kwlist[] =
        {
        "port", "port_type", "mode", "role", NULL
        };

    if (
        !PyArg_ParseTupleAndKeywords
            (
            args, keywds, "|iu#ii", ( char** ) kwlist,
            &aPort, &tmpPortType, &aLenPortType, &aMode, &aRole
            )
       )
    {
        return 0;
    }
    
    TBuf<10> aPortType;    
	if( aLenPortType <= 0 ) {
        aPortType.Append(KDefaultConnType );
    }
    else {
        TPtrC buf((TUint16*)tmpPortType, aLenPortType);
        aPortType.Append( buf );
    }                     
    
	Py_BEGIN_ALLOW_THREADS;
	TRAP(err,	
       self->iConnManager->ConnectL( aPortType, aPort, aMode, aRole);
       );
	Py_END_ALLOW_THREADS;

	if (err)
	{
		return SPyErr_SetFromSymbianOSErr(err); 
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* USBConnection_send(obj_USBConnection* self, PyObject* args)
{
	char* b = NULL;	
	TInt l = 0;
	TInt timeout = 0;

	if (!PyArg_ParseTuple(args, "s#|i", &b, &l, &timeout))
	{
		return 0;
	}
	
	TInt err;
	Py_BEGIN_ALLOW_THREADS;
	TRAP(err,
       TPtrC8 buf((TUint8*)b, l);		
       self->iConnManager->SendL(buf, timeout);
       );
	Py_END_ALLOW_THREADS;

	if (err)
	{
		return SPyErr_SetFromSymbianOSErr(err); 
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* USBConnection_recv(obj_USBConnection* self, PyObject* args)
{	
	TInt l = 0;
	TInt timeout = 0;

	if (!PyArg_ParseTuple(args, "i|i", &l, &timeout))
	{
		return 0;
	}

	TUint8* buf = 0;
    TPtr8 tmp(buf, 0);
	TInt err;
	TBool alloc_ok = EFalse;

	Py_BEGIN_ALLOW_THREADS;			
	TRAP(err,
       buf = (TUint8*) User::AllocLC(l);
       tmp.Set(buf, 0, l);
       alloc_ok = ETrue;
       self->iConnManager->RecvL(tmp, timeout);
       CleanupStack::Pop(buf);
       );
	Py_END_ALLOW_THREADS;

	if (err)
	{	
		if (alloc_ok)
    {
			delete buf;
    }		
		return SPyErr_SetFromSymbianOSErr(err); 
	}
	
	PyObject* rv = Py_BuildValue("s#", buf, tmp.Length());
  
	delete buf;
	return rv;
}

static PyObject* USBConnection_close(obj_USBConnection* self, PyObject* /*args*/)
{
	TInt err;
	Py_BEGIN_ALLOW_THREADS;
	TRAP(err,
       self->iConnManager->CloseL();
       );
	Py_END_ALLOW_THREADS;

	if (err)
	{
		return SPyErr_SetFromSymbianOSErr(err); 
	}
	
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* kill_faxmodem(PyObject* /*self*/, PyObject* /*args*/)
{
  // this should kill the faxmodem
  
  // code by plamendev, see:
  // http://forum.newlc.com/index.php/topic,6353.0.html
  
  _LIT8(KFAXMODEM, "FaxModem");
  TBuf8<50> buf;
  TFullName repName;

  TFindProcess process;
  while(process.Next(repName) != KErrNotFound)
  {
    buf.Copy(repName);
 
    if ((buf.Find(KFAXMODEM) != KErrNotFound))
    {
      RProcess aProcess;
      aProcess.Open(process);
      aProcess.Kill(0);
      aProcess.Close();       
    }
  }
   
  Py_INCREF(Py_None);
  return Py_None;
}

static const PyMethodDef pys60usb_methods[] =
{
	{"USBConnection", (PyCFunction)USBConnection_USBConnection, METH_NOARGS},		
	{"kill_faxmodem", (PyCFunction)kill_faxmodem, METH_NOARGS},
	{0, 0} /* sentinel */
};

DL_EXPORT(void) init_pys60usb()
{
	// work done here:
	// 1. init module
  // 2. create type object for our Connection type


	PyObject* module = Py_InitModule("pys60usb", (PyMethodDef*) pys60usb_methods);
	if (!module)
		return;

	PyTypeObject *USBConnectionTypeObject = PyObject_New(PyTypeObject, &PyType_Type);
	if (!USBConnectionTypeObject)
		return;
    
    //--------------------------------------------------------
    // Add constants 
    //--------------------------------------------------------
    PyObject *module_dict = PyModule_GetDict( module );
    
    // TCommAccess
    PyDict_SetItemString(module_dict, "ECommExclusive",   PyInt_FromLong( ECommExclusive ));
    PyDict_SetItemString(module_dict, "ECommShared",      PyInt_FromLong( ECommShared ));
    PyDict_SetItemString(module_dict, "ECommPreemptable", PyInt_FromLong( ECommPreemptable ));
    
    // TCommRole
    PyDict_SetItemString(module_dict, "ECommRoleDTE", PyInt_FromLong( ECommRoleDTE ));
    PyDict_SetItemString(module_dict, "ECommRoleDCE", PyInt_FromLong( ECommRoleDCE ));            
    //--------------------------------------------------------
    
    *USBConnectionTypeObject = type_template_USBConnection;
    
    TInt err = SPyAddGlobalString(USBConnection_type_string, (PyObject *)USBConnectionTypeObject);
    if (0 != err) // 0 is success
    {
    	PyObject_Del(USBConnectionTypeObject);
    	PyErr_SetString(PyExc_Exception, "SPyAddGlobalString failed");
    	return;
    }
    
    // notice that the this uses the macro defined in the beginning of file
    type_USBConnection.ob_type = &PyType_Type; 
}


GLDEF_C TInt E32Dll(TDllReason)
{
	return KErrNone;
}


