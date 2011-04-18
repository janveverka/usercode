#ifndef MISC_TREEMAKER_SINGLEBRANCHMANAGER_H
#define MISC_TREEMAKER_SINGLEBRANCHMANAGER_H

#include <string>
#include <memory>
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "TTree.h"

namespace cit {

  template <typename Collection>
  class SingleBranchManager {
    public:
      /// typedefs
      enum MAX_SIZE {VECTOR_SIZE = 100};
      typedef typename Collection::value_type obj_type;
      typedef StringObjectFunction<obj_type> func_type;
      typedef std::auto_ptr<func_type> func_ptr_type;

      /// ctor
      SingleBranchManager( const std::string &iTag,
                           func_ptr_type iQuantity,
                           size_t size = VECTOR_SIZE ) :
        tag_( iTag ), quantity_( iQuantity ), data_( size ), branch_( 0 )
      { data_.clear(); }


      /// dtor
      ~SingleBranchManager() {}


      /// member methods
      void
      makeBranch( TTree &tree, const char *size )
      {
        branch_ = tree.Branch(tag_.c_str(),
                              &(data_[0]),
                              (tag_ + "[" + size + "]/F").c_str() );
      } // end of method makeBranch(...)


      void
      clearData()
      { data_.clear(); }


      virtual void
      getData( Collection const & collection )
      {
        for (typename Collection::const_iterator element = collection.begin();
            element != collection.end(); ++element) {
          data_.push_back( (*quantity_)(*element) );
        } // end of loop over collection
      } // end of method getData(...)


      void
      updateBranchAddress()
      { if (branch_ != 0) branch_->SetAddress( &(data_[0]) ); }


    protected:
      std::string tag_;
      func_ptr_type quantity_;
      std::vector<Float_t> data_;
      TBranch *branch_;
  }; // end of class SingleBranchManager definition
} // end of namespace cit

#endif
