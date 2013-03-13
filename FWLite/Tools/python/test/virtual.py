'''
Test the method virtuality behavior of python methods.

Does the method Daughter.name in the derived class Daughter(Mother)
shadow the method Mother.name even when called within the base
class in the method Mother.hello?

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


#==============================================================================
class Daughter(Mother):
    #__________________________________________________________________________
    def name(self):
        '''
        Shadows Mother.name().
        '''
        return 'virtual baby'


#==============================================================================
def main():
    '''
    Main entry point of execution.
    '''
    dau = Daughter()
    
    ## Expect one of:
    ## 1. "Hello! I am your baby." or
    ## 2. "Hello! I am your mum."
    ## Dan claims it will be 1.  Will it?
    print dau.hello()
    ## Yes.  However, there is a workaround:
    print dau.hello_workaround()


#==============================================================================
if __name__ == '__main__':
    main()
