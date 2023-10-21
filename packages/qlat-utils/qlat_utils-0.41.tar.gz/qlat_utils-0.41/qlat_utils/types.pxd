from . cimport everything as cqlat_utils

cdef class Buffer:
    cdef object obj
    cdef int ndim
    cdef Py_ssize_t itemsize
    cdef cqlat_utils.std_vector[Py_ssize_t] shape_strides # shape.size() == 2 * ndim
    cdef Py_ssize_t get_len(self)
    cdef void set_strides(self)

### -------------------------------------------------------------------

cdef class ElemType:
    pass

cdef class ElemTypeColorMatrix(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeWilsonMatrix(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeNonRelWilsonMatrix(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeIsospinMatrix(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeSpinMatrix(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeWilsonVector(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeComplex(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeComplexF(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeDouble(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeFloat(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeLong(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeInt64t(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeInt8t(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()

cdef class ElemTypeChar(ElemType):
    @staticmethod
    cdef char* format()
    @staticmethod
    cdef Py_ssize_t itemsize()
    @staticmethod
    cdef int ndim()
    @staticmethod
    cdef cqlat_utils.std_vector[Py_ssize_t] shape()
    @staticmethod
    cdef Py_ssize_t size()
