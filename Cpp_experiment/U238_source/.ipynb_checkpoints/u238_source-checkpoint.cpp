#include <memory>
#include <cmath>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "openmc/distribution.h"

class U238SpontaneousFissionSource : public openmc::Source 
{
private:
    // Maxwell distribution for U-238 with T = 1.346 MeV
    openmc::Maxwell maxwell_dist{1.346};

    // Sample number of neutrons using discrete distribution
    int sample_num_neutrons(uint64_t* seed) const {
        double xi = openmc::prn(seed);
        
        if (xi < 0.0481677) return 0;
        if (xi < 0.0481677 + 0.2485215) return 1;
        if (xi < 0.0481677 + 0.2485215 + 0.4253044) return 2;
        if (xi < 0.0481677 + 0.2485215 + 0.4253044 + 0.2284094) return 3;
        if (xi < 0.0481677 + 0.2485215 + 0.4253044 + 0.2284094 + 0.0423438) return 4;
        return 5;
    }

public:
    openmc::SourceSite sample(uint64_t* seed) const override 
    {
        openmc::SourceSite particle;
        
        // Set particle type and weight
        particle.particle = openmc::ParticleType::neutron;
        particle.wgt = 1.0;
        
        // Sample position (point source at origin)
        particle.r = {0.0, 0.0, 0.0};
        
        // Sample isotropic direction
        particle.u = openmc::Isotropic().sample(seed);
        
        // Sample energy from Maxwell distribution
        particle.E = maxwell_dist.sample(seed);
        
        // Sample number of neutrons (stored in delayed_group for this example)
        particle.delayed_group = sample_num_neutrons(seed);
        
        return particle;
    }
};

extern "C" std::unique_ptr<U238SpontaneousFissionSource> openmc_create_source(std::string parameters)
{
    return std::make_unique<U238SpontaneousFissionSource>();
}