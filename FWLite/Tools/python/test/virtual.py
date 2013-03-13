'''
Test the method virtuality behavior in Python.

Does the method Daughter.name() in the class Daughter(Mother)
derived from the base class Mother shadow the method 
Mother.name() even when called within the base
class in the method Mother.hello()?

Yes.  However, there is a workaround: Mother.hello_workaround().
You can call the base-class method directly like this:
Mother.name(self).

USAGE: python virtual.py

Jan Veverka, Caltech, veverka@caltech.edu
13 March 2013
'''

#==============================================================================
class Mother:
    #__________________________________________________________________________
    def name(self):
        return 'real mum'
    
    #__________________________________________________________________________
    def hello(self):
        '''
        Test what version of the self.name() method is called.
        Is it the one defined in Mother or in the derived Daughter?
        '''
        return 'Hello! I am your %s.' % self.name()

    #__________________________________________________________________________
    def hello_workaround(self):
        '''
        A workaround that ensures that the "local" name method
        is called.
        '''
        return 'Hello! I am your %s.' % Mother.name(self)
## End of class Mother


#==============================================================================
class Daughter(Mother):
    #__________________________________________________________________________
    def name(self):
        '''
        Shadows Mother.name().
        '''
        return 'virtual baby'
## End of class Daughter


#==============================================================================
def main():
    '''
    Main entry point of execution.
    '''
    dau = Daughter()
    
    ## Expect one of:
    ## 1. "Hello! I am your virtual baby." or
    ## 2. "Hello! I am your real mum."
    ## Dan claims it will be 1. Will it?
    print dau.hello()
    ## Yes.  However, there is a workaround:
    print dau.hello_workaround()
## End of main()


#==============================================================================
if __name__ == '__main__':
    main()
## End of this module
