#include <memory>
#include <cmath>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "openmc/distribution.h"

class Cf252SpontaneousFissionSource : public openmc::Source {
private:
    // Maxwell distribution for Cf-252 
    // Note: You might want to verify these Watt parameters for Cf-252
    openmc::Watt watt_dist{1.18, 0.8475};

    // Sample number of neutrons using discrete distribution for Cf-252
    int sample_num_neutrons(uint64_t* seed) const {
        double xi = openmc::prn(seed);
        if (xi < 0.00217) return 0;        // 0.217%
        if (xi < 0.00217 + 0.02556) return 1;   // 2.556%
        if (xi < 0.00217 + 0.02556 + 0.12741) return 2;   // 12.741%
        if (xi < 0.00217 + 0.02556 + 0.12741 + 0.27433) return 3;   // 27.72%
        if (xi < 0.00217 + 0.02556 + 0.12741 + 0.27433 + 0.30517) return 4;   // 30.517%
        if (xi < 0.00217 + 0.02556 + 0.12741 + 0.27433 + 0.30517 + 0.18523) return 5;   // 18.529%
        if (xi < 0.00217 + 0.02556 + 0.12741 + 0.27433 + 0.30517 + 0.18523 + 0.06607) return 6;   // 6.607%
        if (xi < 0.00217 + 0.02556 + 0.12741 + 0.27433 + 0.30517 + 0.18523 + 0.06607 + 0.01414) return 7;   // 1.414%
        if (xi < 0.00217 + 0.02556 + 0.12741 + 0.27433 + 0.30517 + 0.18523 + 0.06607 + 0.01414 + 0.00186) return 8;   // 0.186%
        return 9;   // 0.006%
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

extern "C" std::unique_ptr<Cf252SpontaneousFissionSource> openmc_create_source(std::string parameters) {
    return std::make_unique<Cf252SpontaneousFissionSource>();
}
