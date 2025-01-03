#include <memory>
#include <cmath>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "openmc/distribution.h"

class Pu240SpontaneousFissionSource : public openmc::Source {
private:
    // Maxwell distribution for Pu-240 with T = 1.346 MeV (same as typical fission spectrum)
    openmc::Watt watt_dist{0.794930, 4.689270};

    // Sample number of neutrons using discrete distribution for Pu-240
    int sample_num_neutrons(uint64_t* seed) const {
        double xi = openmc::prn(seed);
        if (xi < 0.0631) return 0;        // 6.31%
        if (xi < 0.0631 + 0.2319) return 1;   // 23.19%
        if (xi < 0.0631 + 0.2319 + 0.3333) return 2;   // 33.33%
        if (xi < 0.0631 + 0.2319 + 0.3333 + 0.2475) return 3;   // 24.75%
        if (xi < 0.0631 + 0.2319 + 0.3333 + 0.2475 + 0.0996) return 4;   // 9.96%
        if (xi < 0.0631 + 0.2319 + 0.3333 + 0.2475 + 0.0996 + 0.0180) return 5;   // 1.8%
        return 6;   // remaining 1%
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

extern "C" std::unique_ptr<Pu240SpontaneousFissionSource> openmc_create_source(std::string parameters) {
    return std::make_unique<Pu240SpontaneousFissionSource>();
}
