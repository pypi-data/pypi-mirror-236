/*************
Python bindings to CMSGen (http://msoos.org)

Copyright (c) 2013, Ilan Schnell, Continuum Analytics, Inc.
              2014, Mate Soos
              2017, Pierre Vignet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
**********************************/

#include <Python.h>
#include <structmember.h>
#include <limits>
#include <cassert>
#include <algorithm>
#include <signal.h>
#include "../../src/cmsgen.h"
#include "solvertypesmini.h"
using namespace CMSGen;

#define MODULE_NAME "pycmsgen"
#define MODULE_DOC "CMSGen almost-uniform sampler."

#define IS_INT(x)  PyLong_Check(x)
#define MODULE_INIT_FUNC(name) \
PyMODINIT_FUNC PyInit_ ## name(void); \
PyMODINIT_FUNC PyInit_ ## name(void)

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    SATSolver* cmsat;
    std::vector<Lit> tmp_cl_lits;

    int verbose;
    double time_limit;
    long confl_limit;
} Solver;

typedef void (*sighandler_t)(int);

static const char solver_create_docstring[] = \
"Solver(verbose=0, time_limit=max_numeric_limits, confl_limit=max_numeric_limits)\n\
Create Solver object.\n\
\n\
:param verbose: Verbosity level: 0: nothing printed; 15: very verbose.\n\
:param time_limit: Propagation limit: abort after this many seconds has elapsed.\n\
:param confl_limit: Propagation limit: abort after this many conflicts.\n\
    Default: never abort.\n\
:type verbose: <int>\n\
:type time_limit: <double>\n\
:type confl_limit: <long>\n";

static void setup_solver(Solver *self, PyObject *args, PyObject *kwds)
{
    static char const* kwlist[] = {"verbose", "time_limit", "confl_limit", NULL};

    self->cmsat = NULL;
    self->verbose = 0;
    self->time_limit = std::numeric_limits<double>::max();
    self->confl_limit = std::numeric_limits<long>::max();

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|idl",  const_cast<char**>(kwlist),
        &self->verbose, &self->time_limit, &self->confl_limit))
    {
        return;
    }

    if (self->verbose < 0) {
        PyErr_SetString(PyExc_ValueError, "verbosity must be at least 0");
        return;
    }
    if (self->time_limit < 0) {
        PyErr_SetString(PyExc_ValueError, "time_limit must be at least 0");
        return;
    }
    if (self->confl_limit < 0) {
        PyErr_SetString(PyExc_ValueError, "conflict limit must be at least 0");
        return;
    }

    self->cmsat = new SATSolver;
    self->cmsat->set_verbosity(self->verbose);
    self->cmsat->set_max_time(self->time_limit);
    self->cmsat->set_max_confl(self->confl_limit);

    return;
}

static int convert_lit_to_sign_and_var(PyObject* lit, long& var, bool& sign)
{
    if (!IS_INT(lit))  {
        PyErr_SetString(PyExc_TypeError, "integer expected !");
        return 0;
    }

    long val = PyLong_AsLong(lit);
    if (val == 0) {
        PyErr_SetString(PyExc_ValueError, "non-zero integer expected");
        return 0;
    }
    if (val > std::numeric_limits<int>::max()/2
        || val < std::numeric_limits<int>::min()/2
    ) {
        PyErr_Format(PyExc_ValueError, "integer %ld is too small or too large", val);
        return 0;
    }

    sign = (val < 0);
    var = std::abs(val) - 1;

    return 1;
}

static int parse_clause(
    Solver *self
    , PyObject *clause
    , std::vector<Lit>& lits
) {
    PyObject *iterator = PyObject_GetIter(clause);
    if (iterator == NULL) {
        PyErr_SetString(PyExc_TypeError, "iterable object expected");
        return 0;
    }

    PyObject *lit;
    long int max_var = 0;
    while ((lit = PyIter_Next(iterator)) != NULL) {
        long var;
        bool sign;
        int ret = convert_lit_to_sign_and_var(lit, var, sign);
        Py_DECREF(lit);
        if (!ret) {
            Py_DECREF(iterator);
            return 0;
        }
        max_var = std::max(var, max_var);

        lits.push_back(Lit(var, sign));
    }

    if (!lits.empty() && max_var >= (long int)self->cmsat->nVars()) {
        self->cmsat->new_vars(max_var-(long int)self->cmsat->nVars()+1);
    }

    Py_DECREF(iterator);
    if (PyErr_Occurred()) {
        return 0;
    }

    return 1;
}

static int parse_xor_clause(
    Solver *self
    , PyObject *clause
    , std::vector<uint32_t>& vars
) {
    PyObject *iterator = PyObject_GetIter(clause);
    if (iterator == NULL) {
        PyErr_SetString(PyExc_TypeError, "iterable object expected");
        return 0;
    }

    PyObject *lit;
    while ((lit = PyIter_Next(iterator)) != NULL) {
        long var;
        bool sign;
        int ret = convert_lit_to_sign_and_var(lit, var, sign);
        Py_DECREF(lit);
        if (!ret) {
            Py_DECREF(iterator);
            return 0;
        }
        if (sign) {
            PyErr_SetString(PyExc_ValueError, "XOR clause must contiain only positive variables (not inverted literals)");
            Py_DECREF(iterator);
            return 0;
        }

        if (var >= self->cmsat->nVars()) {
            for(long i = (long)self->cmsat->nVars(); i <= var ; i++) {
                self->cmsat->new_var();
            }
        }

        vars.push_back(var);
    }
    Py_DECREF(iterator);
    if (PyErr_Occurred()) {
        return 0;
    }

    return 1;
}

PyDoc_STRVAR(set_var_weight_doc,
"set_var_weight(var, weight)\n\
Set the weight of a variable.\n\
\n\
:param var: Variable for which to set the weight\n\
:param weight: Weight\n\
:type var: int\n\
:type weight: double\n\
:return: None\n\
:rtype: <None>"
);

static PyObject* set_var_weight(Solver *self, PyObject *args, PyObject *kwds)
{
    static char const* kwlist[] = {"var", "weight", NULL};
    int var;
    double weight;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "id",  const_cast<char**>(kwlist),
        &var, &weight))
    {
        PyErr_SetString(PyExc_ValueError, "invalid parameters to set_var_weight");
        return 0;
    }

    if (var <= 0) {
        PyErr_SetString(PyExc_ValueError, "invalid variable number, it must be a positive integer");
        return 0;
    }

    if (weight < 0 || weight > 1.0) {
        PyErr_SetString(PyExc_ValueError, "invalid weight, it must be a non-negative value between 0 and 1, inclusive");
        return 0;
    }
    var--;

    if (self->cmsat->nVars() <= var) self->cmsat->new_vars(var-(self->cmsat->nVars())+1);
    self->cmsat->set_var_weight(Lit(var, false), weight);

    Py_INCREF(Py_None);
    return Py_None;
}

static int _add_clause(Solver *self, PyObject *clause)
{
    self->tmp_cl_lits.clear();
    if (!parse_clause(self, clause, self->tmp_cl_lits)) {
        return 0;
    }
    self->cmsat->add_clause(self->tmp_cl_lits);

    return 1;
}

PyDoc_STRVAR(add_clause_doc,
"add_clause(clause)\n\
Add a clause to the solver.\n\
\n\
:param clause: A clause contains literals (ints)\n\
:type clause: <list>\n\
:return: None\n\
:rtype: <None>"
);

static PyObject* add_clause(Solver *self, PyObject *args, PyObject *kwds)
{
    static char const* kwlist[] = {"clause", NULL};
    PyObject *clause;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", const_cast<char**>(kwlist), &clause)) {
        return NULL;
    }

    if (_add_clause(self, clause) == 0 ) {
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

template <typename T>
static int _add_clauses_from_array(Solver *self, const size_t array_length, const T *array)
{
    if (array_length == 0) {
        return 1;
    }
    if (array[array_length - 1] != 0) {
        PyErr_SetString(PyExc_ValueError, "last clause not terminated by zero");
        return 0;
    }
    size_t k = 0;
    long val = 0;
    std::vector<Lit>& lits = self->tmp_cl_lits;
    for (val = (long) array[k]; k < array_length; val = (long) array[++k]) {
        lits.clear();
        long int max_var = 0;
        for (; k < array_length && val != 0; val = (long) array[++k]) {
            long var;
            bool sign;
            if (val > std::numeric_limits<int>::max()/2
                || val < std::numeric_limits<int>::min()/2
            ) {
                PyErr_Format(PyExc_ValueError, "integer %ld is too small or too large", val);
                return 0;
            }

            sign = (val < 0);
            var = std::abs(val) - 1;
            max_var = std::max(var, max_var);

            lits.push_back(Lit(var, sign));
        }
        if (!lits.empty()) {
            if (max_var >= (long int)self->cmsat->nVars()) {
                self->cmsat->new_vars(max_var-(long int)self->cmsat->nVars()+1);
            }
            self->cmsat->add_clause(lits);
        }
    }
    return 1;
}

static int _add_clauses_from_buffer_info(Solver *self, PyObject *buffer_info, const size_t itemsize)
{
    PyObject *py_array_length = PyTuple_GetItem(buffer_info, 1);
    if (py_array_length == NULL) {
        PyErr_SetString(PyExc_ValueError, "invalid clause array: could not get array length");
        return 0;
    }
    long array_length = PyLong_AsLong(py_array_length);
    if (array_length < 0) {
        PyErr_SetString(PyExc_ValueError, "invalid clause array: could not get array length");
        return 0;
    }
    PyObject *py_array_address = PyTuple_GetItem(buffer_info, 0);
    if (py_array_address == NULL) {
        PyErr_SetString(PyExc_ValueError, "invalid clause array: could not get array address");
        return 0;
    }
    const void *array_address = PyLong_AsVoidPtr(py_array_address);
    if (array_address == NULL) {
        PyErr_SetString(PyExc_ValueError, "invalid clause array: could not get array address");
        return 0;
    }
    if (itemsize == sizeof(int)) {
        return _add_clauses_from_array(self, array_length, (const int *) array_address);
    }
    if (itemsize == sizeof(long)) {
        return _add_clauses_from_array(self, array_length, (const long *) array_address);
    }
    if (itemsize == sizeof(long long)) {
        return _add_clauses_from_array(self, array_length, (const long long *) array_address);
    }
    PyErr_Format(PyExc_ValueError, "invalid clause array: invalid itemsize '%ld'", itemsize);
    return 0;
}

static int _check_array_typecode(PyObject *clauses)
{
    PyObject *py_typecode = PyObject_GetAttrString(clauses, "typecode");
    if (py_typecode == NULL) {
        PyErr_SetString(PyExc_ValueError, "invalid clause array: typecode is NULL");
        return 0;
    }

    PyObject *typecode_bytes = PyUnicode_AsASCIIString(py_typecode);
    Py_DECREF(py_typecode);
    if (typecode_bytes == NULL) {
        PyErr_SetString(PyExc_ValueError, "invalid clause array: could not get typecode bytes");
        return 0;
    }

    const char *typecode_cstr = PyBytes_AsString(typecode_bytes);
    if (typecode_cstr == NULL) {
        Py_DECREF(typecode_bytes);
        PyErr_SetString(PyExc_ValueError, "invalid clause array: could not get typecode cstring");
        return 0;
    }
    const char typecode = typecode_cstr[0];
    if (typecode == '\0' || typecode_cstr[1] != '\0') {
        PyErr_Format(PyExc_ValueError, "invalid clause array: invalid typecode '%s'", typecode_cstr);
        Py_DECREF(typecode_bytes);
        return 0;
    }
    Py_DECREF(typecode_bytes);
    if (typecode != 'i' && typecode != 'l' && typecode != 'q') {
        PyErr_Format(PyExc_ValueError, "invalid clause array: invalid typecode '%c'", typecode);
        return 0;
    }
    return 1;
}

static int add_clauses_array(Solver *self, PyObject *clauses)
{
    if (_check_array_typecode(clauses) == 0) {
        return 0;
    }
    PyObject *py_itemsize = PyObject_GetAttrString(clauses, "itemsize");
    if (py_itemsize == NULL) {
        PyErr_SetString(PyExc_ValueError, "invalid clause array: itemsize is NULL");
        return 0;
    }
    const long itemsize = PyLong_AsLong(py_itemsize);
    Py_DECREF(py_itemsize);
    if (itemsize < 0) {
        PyErr_SetString(PyExc_ValueError, "invalid clause array: could not get itemsize");
        return 0;
    }
    PyObject *buffer_info = PyObject_CallMethod(clauses, "buffer_info", NULL);
    if (buffer_info == NULL) {
        PyErr_SetString(PyExc_ValueError, "invalid clause array: buffer_info is NULL");
        return 0;
    }
    int ret = _add_clauses_from_buffer_info(self, buffer_info, itemsize);
    Py_DECREF(buffer_info);
    return ret;
}

PyDoc_STRVAR(add_clauses_doc,
"add_clauses(clauses)\n\
Add iterable of clauses to the solver.\n\
\n\
:param clauses: List of clauses. Each clause contains literals (ints)\n\
    Alternatively, this can be a flat array.array (typecode 'i', 'l', or 'q')\n\
    of zero separated and terminated clauses of literals (ints).\n\
:type clauses: <list> or <array.array>\n\
:return: None\n\
:rtype: <None>"
);

static PyObject* add_clauses(Solver *self, PyObject *args, PyObject *kwds)
{
    static char const* kwlist[] = {"clauses", NULL};
    PyObject *clauses;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", const_cast<char**>(kwlist), &clauses)) {
        return NULL;
    }

    if (
        PyObject_HasAttr(clauses, PyUnicode_FromString("buffer_info")) &&
        PyObject_HasAttr(clauses, PyUnicode_FromString("typecode")) &&
        PyObject_HasAttr(clauses, PyUnicode_FromString("itemsize"))
    ) {
        int ret = add_clauses_array(self, clauses);
        if (ret == 0 || PyErr_Occurred()) {
            return 0;
        }
        Py_INCREF(Py_None);
        return Py_None;
    }

    PyObject *iterator = PyObject_GetIter(clauses);
    if (iterator == NULL) {
        PyErr_SetString(PyExc_TypeError, "iterable object expected");
        return NULL;
    }

    PyObject *clause;
    while ((clause = PyIter_Next(iterator)) != NULL) {
        _add_clause(self, clause);
        /* release reference when done */
        Py_DECREF(clause);
    }

    /* release reference when done */
    Py_DECREF(iterator);
    if (PyErr_Occurred()) {
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* add_xor_clause(Solver *self, PyObject *args, PyObject *kwds)
{
    static char const* kwlist[] = {"xor_clause", "rhs", NULL};
    PyObject *rhs;
    PyObject *clause;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO", const_cast<char**>(kwlist), &clause, &rhs)) {
        return NULL;
    }
    if (!PyBool_Check(rhs)) {
        PyErr_SetString(PyExc_TypeError, "rhs must be boolean");
        return NULL;
    }
    bool real_rhs = PyObject_IsTrue(rhs);

    std::vector<uint32_t> vars;
    if (!parse_xor_clause(self, clause, vars)) {
        return 0;
    }

    self->cmsat->add_xor_clause(vars, real_rhs);

    Py_INCREF(Py_None);
    return Py_None;
}


PyDoc_STRVAR(nb_vars_doc,
"nb_vars()\n\
Return the number of literals in the solver.\n\
\n\
:return: Number of literals\n\
:rtype: <int>"
);

static PyObject* nb_vars(Solver *self)
{
    return PyLong_FromLong(self->cmsat->nVars());

}

PyDoc_STRVAR(get_model_doc,
"get_model()\n\
Return the model.\n\
\n\
:return: List of integers for the values\n\
:rtype: <list>"
);

static PyObject* get_model(Solver *self) {
    SATSolver* cmsat = self->cmsat;
    if (!cmsat->okay()) {
        PyErr_SetString(PyExc_SystemError, "called get_model on an UNSAT solver");
        return NULL;
    }

    // Create tuple with the size of number of variables in model
    unsigned max_idx = cmsat->nVars();
    PyObject *list = PyList_New((Py_ssize_t)max_idx);
    if (list == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }

    // Add each variable in model to the list
    PyObject *py_value;
    int sign;
    for (long var = 0; var != (long)max_idx; var++) {
        if (cmsat->get_model()[var] != l_Undef) {
            sign = (cmsat->get_model()[var] == l_True) ? 1 : -1;
            py_value = PyLong_FromLong((var + 1) * sign);
            PyList_SET_ITEM(list, (Py_ssize_t)var, py_value);
        }
    }
    return list;
}

static int parse_assumption_lits(PyObject* assumptions, SATSolver* cmsat, std::vector<Lit>& assumption_lits)
{
    PyObject *iterator = PyObject_GetIter(assumptions);
    if (iterator == NULL) {
        PyErr_SetString(PyExc_TypeError, "interable object expected");
        return 0;
    }

    PyObject *lit;
    while ((lit = PyIter_Next(iterator)) != NULL) {
        long var;
        bool sign;
        int ret = convert_lit_to_sign_and_var(lit, var, sign);
        Py_DECREF(lit);
        if (!ret) {
            Py_DECREF(iterator);
            return 0;
        }

        if (var >= cmsat->nVars()) {
            Py_DECREF(iterator);
            PyErr_Format(PyExc_ValueError, "Variable %ld not used in clauses", var+1);
            return 0;
        }

        assumption_lits.push_back(Lit(var, sign));
    }
    Py_DECREF(iterator);
    if (PyErr_Occurred()) {
        return 0;
    }

    return 1;
}

PyDoc_STRVAR(solve_doc,
"solve(assumptions=None, verbose=None, time_limit=None, confl_limit=None)\n\
Solve the system of equations that have been added with add_clause();\n\
\n\
.. example:: \n\
    from pycmsgen import Solver\n\
    >>> s = Solver()\n\
    >>> s.add_clause([1])\n\
    >>> s.add_clause([-2])\n\
    >>> s.add_clause([3])\n\
    >>> s.add_clause([-1, 2, 3])\n\
    >>> sat, solution = s.solve()\n\
    >>> print sat\n\
    True\n\
    >>> print solution\n\
    (None, True, False, True)\n\
    \n\
    We can also try to assume any variable values for a single solver run:\n\
    \n\
    sat, solution = s.solve([-3])\n\
    >>> print sat\n\
    False\n\
    >>> print solution\n\
    None\n\
\n\
:param assumptions: (Optional) Allows the user to set values to specific\n\
    ariables in the solver in a temporary fashion. This means that in case\n\
    the problem is satisfiable but e.g it's unsatisfiable if variable 2 is\n\
    FALSE, then solve([-2]) will return UNSAT. However, a subsequent call to\n\
    solve() will still return a solution.\n\
:type assumptions: <list>\n\
:param verbose: (Optional) Allows the user to set a verbosity for just this\n\
    solve.\n\
:type verbose: <int>\n\
:param time_limit: (Optional) Allows the user to set a timeout for just this\n\
    solve.\n\
:type time_limit: <double>\n\
:param confl_limit: (Optional) Allows the user to set a conflict limit for just\n\
    this solve.\n\
:type confl_limit: <long>\n\
:return: Whether we succeeded\n\
:rtype: <Bool>"
);

static SATSolver* solverToInterrupt = NULL;
void SIGINT_handler(int)
{
    SATSolver* solver = solverToInterrupt;
    if (solverToInterrupt == NULL) { exit(-1); }
    solver->interrupt_asap();
}

static PyObject* solve(Solver *self, PyObject *args, PyObject *kwds)
{
    PyObject* assumptions = NULL;
    solverToInterrupt = self->cmsat;
    sighandler_t old_sig_int_handler = signal(SIGINT, SIGINT_handler);
    sighandler_t old_sig_term_handler = signal(SIGTERM, SIGINT_handler);

    int verbose = self->verbose;
    double time_limit = self->time_limit;
    long confl_limit = self->confl_limit;

    static char const* kwlist[] = {"assumptions", "verbose", "time_limit", "confl_limit", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|Oidl", const_cast<char**>(kwlist), &assumptions, &verbose, &time_limit, &confl_limit)) {
        return NULL;
    }
    if (verbose < 0) {
        PyErr_SetString(PyExc_ValueError, "verbosity must be at least 0");
        return NULL;
    }
    if (time_limit < 0) {
        PyErr_SetString(PyExc_ValueError, "time_limit must be at least 0");
        return NULL;
    }
    if (confl_limit < 0) {
        PyErr_SetString(PyExc_ValueError, "conflict limit must be at least 0");
        return NULL;
    }

    std::vector<Lit> assumption_lits;
    if (assumptions) {
        if (!parse_assumption_lits(assumptions, self->cmsat, assumption_lits)) {
            return 0;
        }
    }

    self->cmsat->set_verbosity(verbose);
    self->cmsat->set_max_time(time_limit);
    self->cmsat->set_max_confl(confl_limit);

    lbool res;
    res = self->cmsat->solve(&assumption_lits);
    signal(SIGINT, old_sig_int_handler);
    signal(SIGTERM, old_sig_term_handler);
    self->cmsat->set_verbosity(self->verbose);
    self->cmsat->set_max_time(self->time_limit);
    self->cmsat->set_max_confl(self->confl_limit);

    PyObject *result;
    if (res == l_True) {
        result = Py_True;
        Py_INCREF(Py_True);
    } else if (res == l_False) {
        result = Py_False;
        Py_INCREF(Py_False);
    } else if (res == l_Undef) {
        result = Py_None;
        Py_INCREF(Py_None);
    } else {
        assert((res == l_False) || (res == l_True) || (res == l_Undef));
        return PyErr_NewExceptionWithDoc("pycmsgen.IllegalState", "Error Occurred in CyrptoMiniSat", NULL, NULL);
    }

    return result;
}

PyDoc_STRVAR(is_satisfiable_doc,
"is_satisfiable()\n\
Return satisfiability of the system.\n\
\n\
:return: True or False\n\
:rtype: <boolean>"
);

static PyObject* is_satisfiable(Solver *self)
{
    lbool res;
    res = self->cmsat->solve();

    if (res == l_True) {
        Py_INCREF(Py_True);
        return Py_True;
    } else if (res == l_False) {
        Py_INCREF(Py_False);
        return Py_False;
    } else if (res == l_Undef) {
        return Py_None;
    } else {
        // res can only be l_False, l_True, l_Undef
        assert((res == l_False) || (res == l_True) || (res == l_Undef));
        return NULL;
    }
}

/*************************** Method definitions *************************/

// TODO weights
static PyMethodDef Solver_methods[] = {
    {"solve",     (PyCFunction) solve,       METH_VARARGS | METH_KEYWORDS, solve_doc},
    {"set_var_weight",(PyCFunction) set_var_weight,  METH_VARARGS | METH_KEYWORDS, set_var_weight_doc},
    {"add_clause",(PyCFunction) add_clause,  METH_VARARGS | METH_KEYWORDS, add_clause_doc},
    {"add_clauses", (PyCFunction) add_clauses,  METH_VARARGS | METH_KEYWORDS, add_clauses_doc},
    {"add_xor_clause",(PyCFunction) add_xor_clause,  METH_VARARGS | METH_KEYWORDS, "adds an XOR clause to the system"},
    {"nb_vars", (PyCFunction) nb_vars, METH_VARARGS | METH_KEYWORDS, nb_vars_doc},
    {"get_model", (PyCFunction) get_model, METH_VARARGS | METH_KEYWORDS, get_model_doc},
    {"is_satisfiable", (PyCFunction) is_satisfiable, METH_VARARGS | METH_KEYWORDS, is_satisfiable_doc},

    {NULL,        NULL}  /* sentinel - marks the end of this structure */
};

static void
Solver_dealloc(Solver* self)
{
    delete self->cmsat;
    Py_TYPE(self)->tp_free ((PyObject*) self);
}

static int
Solver_init(Solver *self, PyObject *args, PyObject *kwds)
{
    if (self->cmsat != NULL) {
        delete self->cmsat;
    }

    setup_solver(self, args, kwds);
    if (!self->cmsat) {
        return -1;
    }
    return 0;
}

static PyTypeObject pycmsgen_SolverType = {
    PyVarObject_HEAD_INIT(NULL, 0) /*ob_size*/
    "pycmsgen.Solver",       /*tp_name*/
    sizeof(Solver),             /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    (destructor)Solver_dealloc, /*tp_dealloc*/
    0,                          /*tp_print*/
    0,                          /*tp_getattr*/
    0,                          /*tp_setattr*/
    0,                          /*tp_compare*/
    0,                          /*tp_repr*/
    0,                          /*tp_as_number*/
    0,                          /*tp_as_sequence*/
    0,                          /*tp_as_mapping*/
    0,                          /*tp_hash */
    0,                          /*tp_call*/
    0,                          /*tp_str*/
    0,                          /*tp_getattro*/
    0,                          /*tp_setattro*/
    0,                          /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    solver_create_docstring,    /* tp_doc */
    0,                          /* tp_traverse */
    0,                          /* tp_clear */
    0,                          /* tp_richcompare */
    0,                          /* tp_weaklistoffset */
    0,                          /* tp_iter */
    0,                          /* tp_iternext */
    Solver_methods,             /* tp_methods */
    0,                          /* tp_members */
    0,                          /* tp_getset */
    0,                          /* tp_base */
    0,                          /* tp_dict */
    0,                          /* tp_descr_get */
    0,                          /* tp_descr_set */
    0,                          /* tp_dictoffset */
    (initproc)Solver_init,      /* tp_init */
};

MODULE_INIT_FUNC(pycmsgen)
{
    PyObject* m;

    pycmsgen_SolverType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&pycmsgen_SolverType) < 0) {
        // Return NULL on Python3 and on Python2 with MODULE_INIT_FUNC macro
        // In pure Python2: return nothing.
        return NULL;
    }

    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,  /* m_base */
        MODULE_NAME,            /* m_name */
        MODULE_DOC,             /* m_doc */
        -1,                     /* m_size */
        NULL,                   /* m_methods */
        NULL,                   /* m_reload */
        NULL,                   /* m_traverse */
        NULL,                   /* m_clear */
        NULL,                   /* m_free */
    };

    m = PyModule_Create(&moduledef);

    // Return NULL on Python3 and on Python2 with MODULE_INIT_FUNC macro
    // In pure Python2: return nothing.
    if (!m) {
        return NULL;
    }

    // Add the version string so users know what version of CMSGen
    // they're using.
#if defined(_MSC_VER)
#else
    if (PyModule_AddStringConstant(m, "__version__", CMSGEN_FULL_VERSION) == -1) {
        Py_DECREF(m);
        return NULL;
    }
    if (PyModule_AddStringConstant(m, "VERSION", CMSGEN_FULL_VERSION) == -1) {
        Py_DECREF(m);
        return NULL;
    }
#endif

    // Add the Solver type.
    Py_INCREF(&pycmsgen_SolverType);
    if (PyModule_AddObject(m, "Solver", (PyObject *)&pycmsgen_SolverType)) {
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
