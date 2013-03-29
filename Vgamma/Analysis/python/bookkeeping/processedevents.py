import os
import datetime
from Vgamma.Analysis.bookkeeping.samples import eegamma
from Vgamma.Analysis.bookkeeping.samples import mumugamma
from Vgamma.Analysis.bookkeeping.samples import test

#______________________________________________________________________________
def main():
    print 'START:', datetime.datetime.now().isoformat()

    to_process = [
        ('EEG', eegamma), 
        ('MMG', mumugamma),
        ('TEST', test)
        ]
        
    for name, collection in to_process:
        ## Give a heads-up
        print '==', name, '=='
        print 'Samples to process:', collection.keys()

        ## Loop over datasets
        for sample in (collection.values())[:]:
            total = sample.get_total_processed_events()
            if total == sample.total_processed_events:
                print sample.name, 'up to date'
            else:
                print sample.name, 'total processed events updating to', total
                filename = os.path.join(collection.package.__path__[0], 
                                        sample.name + '.py')
                with file(filename, 'a') as pyfile:
                    line = ('%s.total_processed_events = '
                            '%s\n') % (sample.name, total)
                    pyfile.write(line)
        
    print 'FIN:', datetime.datetime.now().isoformat()

#______________________________________________________________________________
if __name__ == '__main__':
    main()
    import user
