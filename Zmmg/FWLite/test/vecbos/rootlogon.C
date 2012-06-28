{
  if (strcmp(gStyle->GetName(), "Plain") == 0) {
    cout << "Loading CMS Style ..." << endl << flush;
    G__loadfile("CMSStyle.C"); 
    CMSstyle();
  }
}
