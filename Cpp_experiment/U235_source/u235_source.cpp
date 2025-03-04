#include <memory>
#include <cmath>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "openmc/distribution.h"

class U235FissionSource : public openmc::Source {
private:
    // Maxwell distribution for U-235 
    // Note: You'll need to verify these Watt distribution parameters for U-235
    openmc::Watt watt_dist{0.988, 2.249}; // Example values - please verify

    // Sample number of neutrons using discrete distribution for U-235 (thermal)
    int sample_num_neutrons(uint64_t* seed) const {
        double xi = openmc::prn(seed);
        if (xi < 0.0238) return 0;        // 2.38%
        if (xi < 0.0238 + 0.1556) return 1;   // 15.56%
        if (xi < 0.0238 + 0.1556 + 0.3216) return 2;   // 32.16%
        if (xi < 0.0238 + 0.1556 + 0.3216 + 0.3134) return 3;   // 31.34%
        if (xi < 0.0238 + 0.1556 + 0.3216 + 0.3134 + 0.1356) return 4;   // 13.56%
        if (xi < 0.0238 + 0.1556 + 0.3216 + 0.3134 + 0.1356 + 0.0356) return 5;   // 3.56%
        if (xi < 0.0238 + 0.1556 + 0.3216 + 0.3134 + 0.1356 + 0.0356 + 0.0043) return 6;   // 0.43%
        return 7;   // remaining 0.01%
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

extern "C" std::unique_ptr<U235FissionSource> openmc_create_source(std::string parameters) {
    return std::make_unique<U235FissionSource>();
}
