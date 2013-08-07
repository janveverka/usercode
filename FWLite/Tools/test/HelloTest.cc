/**
 * \file FWLite/Tools/test/HelloTest.cc
 * \class HelloTest
 *
 * \brief Unit test of the class Hello
 *  A minimalistic example of a unit test using CppUnit and Scram, see
 *  o http://www.yolinux.com/TUTORIALS/CppUnit.html
 *  o https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideDevelopersGuide
 *     #Add_tests_to_your_package
 *
 * \author Jan Veverka, MIT, jan.veverka@cern.ch
 * \date 7 August 2013
 */

#include <cppunit/extensions/HelperMacros.h>
#include "FWLite/Tools/interface/Hello.h"

using ::fwlite::tools::Hello;

//_____________________________________________________________________________
/**
 * Hello test fixture
 */
class HelloTest : public ::CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(HelloTest);
  CPPUNIT_TEST(testPrintDefault);
  CPPUNIT_TEST(testPrintCustom);
  CPPUNIT_TEST(testPrintFail);
  CPPUNIT_TEST(testLeftShiftOperatorOverload);
  CPPUNIT_TEST_SUITE_END();

public:
  void setUp(void);
  void tearDown(void);

protected:
  void testPrintDefault(void);
  void testPrintCustom(void);
  void testPrintFail(void);
  void testLeftShiftOperatorOverload(void);

private:
  std::string customExpected_;
  Hello *defaultHello_;
  Hello *customHello_ ;
}; // class HelloTest

//_____________________________________________________________________________
CPPUNIT_TEST_SUITE_REGISTRATION(HelloTest);

//_____________________________________________________________________________
void
HelloTest::setUp(void)
{
  customExpected_ = "what's up, buddy?";
  defaultHello_ = new Hello();
  customHello_  = new Hello(customExpected_);
} // HelloTest::setUp(void)


//_____________________________________________________________________________
void
HelloTest::tearDown(void)
{
  delete defaultHello_;
  delete customHello_ ;
} // HelloTest::tearDown(void)


//_____________________________________________________________________________
void
HelloTest::testPrintDefault(void)
{
  std::ostringstream out;
  defaultHello_->print(out);
  CPPUNIT_ASSERT("hello, world!" == out.str());
} //HelloTest::testPrintDefault(void)


//_____________________________________________________________________________
void
HelloTest::testPrintCustom(void)
{
  std::ostringstream out;
  customHello_->print(out);
  CPPUNIT_ASSERT(customExpected_ == out.str());
} //HelloTest::testPrintDefault(void)


//_____________________________________________________________________________
/**
 * Fail intentionally to check the effect.
 */
void
HelloTest::testPrintFail(void)
{
  std::ostringstream out;
  customHello_->print(out);
  CPPUNIT_ASSERT_MESSAGE("NO FAIL", true);
  // CPPUNIT_ASSERT(out.str() == "customExpected_");
  // CPPUNIT_ASSERT_EQUAL(std::string("customExpected_"), out.str());
/*  CPPUNIT_ASSERT_EQUAL_MESSAGE("THIS SHOULD FAIL",
                               std::string("customExpected_"), out.str());*/
} //HelloTest::testPrintFail(void)


//_____________________________________________________________________________
void
HelloTest::testLeftShiftOperatorOverload(void)
{
  std::ostringstream out;
  out << (*customHello_);
  CPPUNIT_ASSERT(out.str() == customExpected_);
  out << *defaultHello_;
  CPPUNIT_ASSERT(out.str() == customExpected_ + "hello, world!");
} //HelloTest::testPrintDefault(void)
