#include <Python.h>

static const long long COIN = 100000000;

double ConvertBitsToDouble(unsigned int nBits)
{
    int nShift = (nBits >> 24) & 0xff;

    double dDiff =
        (double)0x0000ffff / (double)(nBits & 0x00ffffff);

    while (nShift < 29)
    {
        dDiff *= 256.0;
        nShift++;
    }
    while (nShift > 29)
    {
        dDiff /= 256.0;
        nShift--;
    }

    return dDiff;
}

long long static GetBlockBaseValue(int nBits, int nHeight, bool fTestNet = false)
{
double dDiff = (double)0x0000ffff / (double)(nBits & 0x00ffffff);
	dDiff = ConvertBitsToDouble(nBits);
	int64_t nSubsidy = 0;
	
		nSubsidy = (2222222.0 / (pow((dDiff+2600.0)/9.0,2.0))); // 2222222/(((x+2600)/9)^2)
		if (nSubsidy > 25) nSubsidy = 25;
		if (nSubsidy < 1) nSubsidy = 1;
		nSubsidy *= COIN;
		// yearly decline of production by 7% per year, 50% over 4 years 
		for(int i = 210240; i <= nHeight; i += 210240) nSubsidy -= nSubsidy/6;
		nSubsidy -= nSubsidy/10; 
    
    return nSubsidy;
}

static PyObject *eternity_subsidy_getblockbasevalue(PyObject *self, PyObject *args)
{
    int input_bits;
    int input_height;
    if (!PyArg_ParseTuple(args, "ii", &input_bits, &input_height))
        return NULL;
    long long output = GetBlockBaseValue(input_bits, input_height);
    return Py_BuildValue("L", output);
}

static PyObject *eternity_subsidy_getblockbasevalue_testnet(PyObject *self, PyObject *args)
{
    int input_bits;
    int input_height;
    if (!PyArg_ParseTuple(args, "ii", &input_bits, &input_height))
        return NULL;
    long long output = GetBlockBaseValue(input_bits, input_height, true);
    return Py_BuildValue("L", output);
}

static PyMethodDef eternity_subsidy_methods[] = {
    { "GetBlockBaseValue", eternity_subsidy_getblockbasevalue, METH_VARARGS, "Returns the block value" },
    { "GetBlockBaseValue_testnet", eternity_subsidy_getblockbasevalue_testnet, METH_VARARGS, "Returns the block value for testnet" },
    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC initeternity_subsidy(void) {
    (void) Py_InitModule("eternity_subsidy", eternity_subsidy_methods);
}
