if __name__ != '__main__':
    import sys
    from Vgamma.Analysis.bookkeeping.sampleregister import SampleRegister
    __module__ = sys.modules[__name__]
    # setattr(__module__, __name__, SampleRegister(__module__))
    samples = SampleRegister(__module__)
