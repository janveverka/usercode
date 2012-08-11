#ifndef MISC_TREEMAKER_BRANCHMANAGER_H
#define MISC_TREEMAKER_BRANCHMANAGER_H

#include <string>
#include <vector>
#include <boost/ptr_container/ptr_vector.hpp>

#include "TTree.h"

#include "Misc/TreeMaker/interface/ConditionalSingleBranchManager.h"
#include "Misc/TreeMaker/interface/SingleBranchManager.h"

namespace cit {

  template <typename Collection, typename T=Float_t>
  class BranchManager {
    public:
      typedef SingleBranchManager<Collection, T> var_type;
      typedef ConditionalSingleBranchManager<Collection, T> condvar_type;
      typedef typename var_type::obj_type obj_type;
      typedef typename var_type::func_type func_type;
      typedef typename condvar_type::cut_type cut_type;
      typedef typename var_type::func_ptr_type func_ptr_type;
      typedef typename condvar_type::cut_ptr_type cut_ptr_type;

      // ctor
      BranchManager(const edm::ParameterSet& iConfig) :
        src_       ( iConfig.getParameter<edm::InputTag>("src") ),
        prefix_    ( iConfig.getUntrackedParameter<std::string>("prefix", "") ),
        lazyParser_( iConfig.getUntrackedParameter<bool>("lazyParser", true) ),
        sizeTag_( iConfig.getUntrackedParameter<std::string>( "sizeName",
                                                              "n"         ) ),
        size(0)
      {
        typedef edm::ParameterSet PSet;
        typedef std::vector<PSet> VPSet;
        VPSet variables = iConfig.getParameter<VPSet>("variables");
        for (VPSet::const_iterator q = variables.begin();
             q != variables.end(); ++q)
        {
          std::string tag = prefix_ + q->getUntrackedParameter<std::string>("tag");

          if ( q->existsAs<std::string>("quantity", false) ) {
            func_ptr_type quantity( new func_type(
              q->getUntrackedParameter<std::string>("quantity"),
              lazyParser_                                        ) );

            variables_.push_back( new var_type(tag, quantity) );
          } else {
            // expect a conditional quantity
            PSet const &
            cfg = q->getUntrackedParameter<PSet>( "conditionalQuantity" );

            cut_ptr_type condition( new cut_type(
              cfg.getUntrackedParameter<std::string>("ifCondition"),
              lazyParser_                                            ) );

            func_ptr_type quantity( new func_type(
              cfg.getUntrackedParameter<std::string>("thenQuantity"),
              lazyParser_                                             ) );

            func_ptr_type elseQuantity( new func_type(
              cfg.getUntrackedParameter<std::string>("elseQuantity"),
              lazyParser_                                             ) );

            variables_.push_back( new condvar_type( tag,
                                                    condition,
                                                    quantity,
                                                    elseQuantity ) );
          } // end if is a standard or conditional quantity
        } // end of loop over variables
      } // end of BranchManager ctor


      // dtor
      ~BranchManager()
      {
        // No need to delete the vars pointed by the variables_ explicitly,
        // boost::ptr_vector takes care of that.
      }



      void
      init(TTree &tree)
      {
        tree.Branch(sizeTag_.c_str(), &size, (sizeTag_ + "/I").c_str() );

        for (typename boost::ptr_vector<var_type>::iterator
             var = variables_.begin(); var != variables_.end(); ++var) {
          var->makeBranch(tree, sizeTag_.c_str() );
        } // end of loop over variables_

      } // end of method init(...)


      void
      getData( const edm::Event& iEvent,
               const edm::EventSetup& iSetup )
      {

        edm::Handle<Collection> collection;
        iEvent.getByLabel(src_, collection);

        size = collection->size();

        // loop over all variables_
        for (typename boost::ptr_vector<var_type>::iterator
             var = variables_.begin(); var != variables_.end(); ++var) {
          var->clearData();
          var->getData(*collection);
          var->updateBranchAddress();
        } // end of loop over variables_

      } // end of method getData(...)


    private:
      edm::InputTag src_;
      std::string prefix_;
      bool lazyParser_;
      std::string sizeTag_;

      boost::ptr_vector<var_type> variables_;
      Int_t size;
  }; // end of class BranchManager
} // end of namespace cit

#endif
