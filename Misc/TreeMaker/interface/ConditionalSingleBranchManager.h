#ifndef MISC_TREEMAKER_CONDITIONALSINGLEBRANCHMANAGER_H
#define MISC_TREEMAKER_CONDITIONALSINGLEBRANCHMANAGER_H

#include <string>

#include "TTree.h"

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"
#include "Misc/TreeMaker/interface/SingleBranchManager.h"

namespace cit {

  template <typename Collection>
  class ConditionalSingleBranchManager :
    public SingleBranchManager<Collection>
  {
    public:

      /// typedefs
      typedef typename SingleBranchManager<Collection>::obj_type obj_type;
      typedef typename SingleBranchManager<Collection>::func_ptr_type func_ptr_type;
      typedef StringCutObjectSelector<obj_type, true> cut_type;
      typedef std::auto_ptr<cut_type> cut_ptr_type;

      /// ctor
      ConditionalSingleBranchManager(
          const std::string &iTag,
          cut_ptr_type iCondition,
          func_ptr_type iQuantity,
          func_ptr_type iElseQuantity,
          size_t size = SingleBranchManager<Collection>::VECTOR_SIZE) :
        SingleBranchManager<Collection>(iTag, iQuantity, size),
        condition_(iCondition),
        elseQuantity_(iElseQuantity)
      {} // end of ctor


      void
      getData(Collection const & collection)
      {
        for (typename Collection::const_iterator element = collection.begin();
              element != collection.end(); ++element) {
          if ( (*condition_)( *element ) ) {
            this->data_.push_back( (*this->quantity_)( *element ) );
          } else {
            this->data_.push_back( (*elseQuantity_)( *element ) );
          }
        } // end of loop over collection
      } // end of getData(...) method

    protected:
      // data members
      cut_ptr_type condition_;
      func_ptr_type elseQuantity_;
  }; // end of class ConditionalSingleBranchManager
} // end of namespace cit

#endif
