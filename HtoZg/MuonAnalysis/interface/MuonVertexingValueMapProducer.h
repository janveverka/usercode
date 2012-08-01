#ifndef HtoZg_MuonAnalysis_MuonVertexingValueMapProducer_h
#define HtoZg_MuonAnalysis_MuonVertexingValueMapProducer_h
/**
 * \file HtoZg/MuonAnalysis/interface/MuonVertexingValueMapProducer.h
 * \brief Defines Producer of Tight Muon ID Variables that Involve Vertex
 * Defines an EDProducer template class producing muon value maps of dxy and dz w.r.t.
 * the primary vertex. Muon type (reco or pat) is the template paramters.
 * They have the instance labels dxy and dz, so the values maps are named
 * *_*_dxy_* and *_*_dz_*.
 * Configuration parameters:
 *      muonSource - InputTag of the source muon collection
 *      vertexSource - InputTag of the source vertex collection
 * \author Jan Veverka, Caltech
 * \date 1 August 2012
 */

namespace cit {
  namespace hzg {
    /**
     * \class MuonVertexingValueMapProducer 
     */
    template <typename MuonType>
    class MuonVertexingValueMapProducer : public edm::EDProducer {
    public:
      explicit MuonVertexingValueMapProducer(const edm::ParameterSet&);
      ~EgammaUserDataProducer();
    private:
      virtual void produce(edm::Event&, const edm::EventSetup&);
      
      // ----------member data ---------------------------
      void putMap(edm::Event & iEvent,
                  edm::Handle<edm::View<MuonType> >& muons,
                  std::vector<float>& vertexingData,
                  const std::string& name);
      edm::InputTag muonSource_;
      edm::InputTag vertexSource_;
    }; /// class MuonVertexingValueMapProducer
    
    /**
     * Constructor
     */
    template <typename MuonType>
    MuonVertexingValueMapProducer<MuonType>::MuonVertexingValueMapProducer (
      const edm::ParameterSet& iConfig
      ):
      muonSource_(iConfig.getParameter<edm::InputTag>("muonSource")),
      vertexSource_(iConfig.getParameter<edm::InputTag>("vertexSource"))
    {
      produces<edm::ValueMap<float> >("dxy");
      produces<edm::ValueMap<float> >("dz");
    } /// Constructor
    
    /**
     * Destructor
     */
    template <typename MuonType>
    MuonVertexingValueMapProducer<MuonType>::~MuonVertexingValueMapProducer()
    {
    } /// Destructor
    
    /**
     * Method called for each event
     */
    template <typename EgammaType>
    void
    MuonVertexingValueMapProducer<MuonType>::produce (
      edm::Event& iEvent, const edm::EventSetup& iSetup
      )
    {
      using namespace std;
      using namespace edm;

      Handle<View<MuonType> > muons;

      vector<float> dxy;
      vector<float> dz;
      
      putMap(iEvent, muons, dxy, "dxy");
      putMap(iEvent, muons, dz, "dxy");
    } /// produce(..)
    
    /**
     * Helper method that puts one value map in the event.
     */
    template <typename MuonType>
    void
    MuonVertexingValueMapProducer<MuonType>::putMap (
      edm::Event & iEvent,
      edm::Handle<edm::View<MuonType> >& muons,
      std::vector<float>& data,
      const std::string& name
      )
    {
      using namespace std;
      using namespace edm;

      auto_ptr<ValueMap<float> > prod(new ValueMap<float>());
      typename ValueMap<float>::Filler filler (*prod);
      filler.insert(muons, data.begin(), data.end());
      filler.fill();
      iEvent.put(prod, name);
    } /// MuonVertexingValueMapProducer<MuonType>::putMap(...)    
  } // namespace cit::hzg
} // namespace cit

#endif