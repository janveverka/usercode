'''
Defines the class Resampler that facilitates resampling of 
a dataset.

Test usage: python -i resampler.py
'''
import math
import random
import ROOT
import FWLite.Tools.roofit as roo

class Resampler():
    '''
    Facilitates resampling a dataset
    '''
    #__________________________________________________________________________
    def __init__(self, data):
        self.data = data.Clone()
    ## End of __init__
    
    
    #__________________________________________________________________________
    def __getslice__(self, i, j):
        '''
        Implements the python slice operator notatin [i:j].
        '''
        return self.get_slice(i, j)
    ## End of __getslice__(..)

    
    #__________________________________________________________________________
    def get_slice(self, i, j, name='', title=''):
        '''
        Returns a subrange of the original data with i <= entry < j.
        Implements the python bracket operator [].
        '''
        resampled_data = self.data.reduce(roo.EventRange(i, j))
        
        if name:
            resampled_data.SetName(name)
            resampled_data.SetTitle(name)
        
        if title:
            resampled_data.SetTitle(title)
        
        return resampled_data
    ## End of get_slice(..)

    
    #__________________________________________________________________________
    def prescale(self, period, keep_entries = [0], name='', title=''):
        '''
        Prescales the dataset with the given period keeping entries with
        entries in the given list.  An entry n is kept if and only if
        n mod p is in K 
        where p = period and K = keep_entries.
        Example usage:
            resampler = Resampler(data)
            data_half_even = resampler.prescale(2, [0])
            data_half_odd = resampler.prescale(2, [1])
        '''
        resampled_data = self.get_slice(0, 0, name, title)
        
        for entry in range(self.data.numEntries()):
            if entry % period in keep_entries:
                ## Keep this entry
                row = self.data.get(entry)
                weight = self.data.weight()
                weight_error = self.data.weightError()
                resampled_data.addFast(row, weight, weight_error)
        return resampled_data
    ## End of prescale(..)
    
    
    #__________________________________________________________________________
    def bootstrap(self, size=-1, seed=-1, name='', title=''):
        '''
        Returns a bootstrap replica of the original dataset of the given size.
        By default, set the size equal the size of the original sample.
        '''
        resampled_data = self.get_slice(0, 0, name, title)
        
        if size < 0:
            size = self.data.numEntries()
        
        if seed < 0:
            ## Use the system resource to randomize the seed
            seed = random.SystemRandom().randint(0, math.pow(2, 2*8))
        
        random3 = ROOT.TRandom3(seed)
        
        for new_entry in range(size):
            entry = random3.Integer(self.data.numEntries())
            row = self.data.get(entry)
            weight = self.data.weight()
            weight_error = self.data.weightError()
            resampled_data.addFast(row, weight, weight_error)

        return resampled_data
    ## End of bootstrap(..)
    
## End of Resampler


#______________________________________________________________________________
def test_prescaling():
    '''
    Test the prescaling.
    '''
    print '== Prescaling Test =='
    data = get_toy_data(100)
    resampler = Resampler(data)
    data_half_even = resampler.prescale(2, [0], 'data_even', 'Even entries')
    data_half_odd = resampler.prescale(2, [1], 'data_odd', 'Odd entries')
    for d in [data, data_half_even, data_half_odd]:
        d.Print()
        for i in range(4):
            print 'Entry', i, 
            d.get(i).Print('v')
    print
## End of test_prescaling(..)    


#______________________________________________________________________________
def test_bootstrapping():
    '''
    Test the prescaling.
    '''
    import FWLite.Tools.canvases as canvases
    print '== Bootstrapping Test =='
    data = get_toy_data(5)
    resampler = Resampler(data)
    data_boot1 = resampler.bootstrap(name='boot1')
    data_boot2 = resampler.bootstrap(name='boot2')
    for d in [data, data_boot1, data_boot2]:
        d.Print()
        for i in range(d.numEntries()):
            print 'Entry', i, 
            d.get(i).Print('v')
    print
    
    data = get_toy_data(20)
    xvar = data.get()['x']
    
    resampler = Resampler(data)
    boot_mean_hist = ROOT.TH1F('mean', 'mean', 100, -1, 1)
    boot_rms_hist = ROOT.TH1F('RMS', 'RMS', 100, 0, 2)
    for i in range(1000):
        boot_mean_hist.Fill(resampler.bootstrap().mean(xvar))
        boot_rms_hist.Fill(resampler.bootstrap().rmsVar(xvar).getVal())
    
    canvases.next('boot_mean')
    boot_mean_hist.DrawCopy()
    canvases.next('boot_rms')
    boot_rms_hist.DrawCopy()
    canvases.update()

    data.meanVar(xvar).Print()
    print '  bootstrap error:', boot_mean_hist.GetRMS()
    data.rmsVar(xvar).Print()
    print '  bootstrap error:', boot_rms_hist.GetRMS()
## End of test_bootstrapping(..)    


#______________________________________________________________________________
def get_toy_data(size=100):
    '''
    Create a toy dataset of the given size.
    '''
    w = ROOT.RooWorkspace('w')
    g = w.factory('Gaussian::g(x[-5,5], 0, 1)')
    x = w.var('x')
    return g.generate(ROOT.RooArgSet(x), size)
## get_toy_data(..)


#______________________________________________________________________________
def test():
    '''
    Tests the Resampler class.
    '''
    test_prescaling()
    test_bootstrapping()
## End of test()


if __name__ == '__main__':
    test()
    import user