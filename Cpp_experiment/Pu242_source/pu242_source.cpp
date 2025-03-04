#include <memory>
#include <cmath>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "openmc/distribution.h"

class Pu242SpontaneousFissionSource : public openmc::Source {
private:
    // Maxwell distribution for Pu-242 (you may need to adjust these parameters)
    openmc::Watt watt_dist{0.794930, 4.689270};

    // Sample number of neutrons using discrete distribution for Pu-242
    int sample_num_neutrons(uint64_t* seed) const {
        double xi = openmc::prn(seed);
        if (xi < 0.0679423) return 0;        // 6.79423%
        if (xi < 0.0679423 + 0.2293159) return 1;   // 22.34159%
        if (xi < 0.0679423 + 0.2293159 + 0.3341228) return 2;   // 33.98467%
        if (xi < 0.0679423 + 0.2293159 + 0.3341228 + 0.2475501) return 3;   // 25.28467%
        if (xi < 0.0679423 + 0.2293159 + 0.3341228 + 0.2475501 + 0.0996922) return 4;   // 9.86922%
        if (xi < 0.0679423 + 0.2293159 + 0.3341228 + 0.2475501 + 0.0996922 + 0.0182398) return 5;   // 1.53398%
        return 6;   // remaining probability (approximately 0.20406%)
    }

public:
    openmc::SourceSite sample(uint64_t* seed) const override {
        openmc::SourceSite particle;
        
        // Set particle type and weight
        particle.particle = openmc::ParticleType::neutron;
        particle.wgt = 1.0;
        
        // Sample position (point source at origin)
        particle.r = {0.0, 0.0, 0.0};
        
        // Sample isotropic direction
        particle.u = openmc::Isotropic().sample(seed);
        
        // Sample energy from Maxwell distribution
        particle.E = watt_dist.sample(seed);
        
        // Sample number of neutrons
        particle.delayed_group = sample_num_neutrons(seed);
        
        return particle;
    }
};

extern "C" std::unique_ptr<Pu242SpontaneousFissionSource> openmc_create_source(std::string parameters) {
    return std::make_unique<Pu242SpontaneousFissionSource>();
}
