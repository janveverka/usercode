#ifndef MISC_TREEMAKER_SINGLEBRANCHMANAGER_H
#define MISC_TREEMAKER_SINGLEBRANCHMANAGER_H

#include <string>
#include <memory>
#include <boost/type_traits/is_same.hpp>
#include "TTree.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "FWCore/Utilities/interface/Exception.h"

namespace cit {

  template <typename Collection, typename T>
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
        std::string leafTypeFlag;

        /*
          - B : an 8 bit signed integer (Char_t)
          - b : an 8 bit unsigned integer (UChar_t)
          - S : a 16 bit signed integer (Short_t)
          - s : a 16 bit unsigned integer (UShort_t)
          - I : a 32 bit signed integer (Int_t)
          - i : a 32 bit unsigned integer (UInt_t)
          - F : a 32 bit floating point (Float_t)
          - D : a 64 bit floating point (Double_t)
          - L : a 64 bit signed integer (Long64_t)
          - l : a 64 bit unsigned integer (ULong64_t)
          - O : a boolean (Bool_t)
        */

        if      ( boost::is_same<T, Char_t   >::value ) leafTypeFlag = "B";
        else if ( boost::is_same<T, UChar_t  >::value ) leafTypeFlag = "b";
        else if ( boost::is_same<T, Int_t    >::value ) leafTypeFlag = "I";
        else if ( boost::is_same<T, Float_t  >::value ) leafTypeFlag = "F";
        else if ( boost::is_same<T, Double_t >::value ) leafTypeFlag = "D";
        else if ( boost::is_same<T, Long64_t >::value ) leafTypeFlag = "L";
        else if ( boost::is_same<T, ULong64_t>::value ) leafTypeFlag = "l";
        else 
          throw cms::Exception("IllegalType") 
            << "Illegal template argument T!\n";

        branch_ = tree.Branch( tag_.c_str(),
                               &( data_[0] ),
                               ( tag_ + "[" + size + "]/" +
                                 leafTypeFlag               ).c_str() );
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
      std::vector<T> data_;
      TBranch *branch_;
  }; // end of class SingleBranchManager definition
} // end of namespace cit

#endif
