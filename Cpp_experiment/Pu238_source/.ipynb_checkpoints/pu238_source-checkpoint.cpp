#include <memory>
#include <cmath>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "openmc/distribution.h"

class Pu238SpontaneousFissionSource : public openmc::Source {
private:
    // Maxwell distribution for Pu-238 (you may need to adjust these parameters)
    openmc::Watt watt_dist{0.794930, 4.689270};

    // Sample number of neutrons using discrete distribution for Pu-238
    int sample_num_neutrons(uint64_t* seed) const {
        double xi = openmc::prn(seed);
        if (xi < 0.0562929) return 0;        // 5.62929%
        if (xi < 0.0562929 + 0.2106764) return 1;   // 21.06764%
        if (xi < 0.0562929 + 0.2106764 + 0.3707428) return 2;   // 37.07428%
        if (xi < 0.0562929 + 0.2106764 + 0.3707428 + 0.2224394) return 3;   // 22.24394%
        if (xi < 0.0562929 + 0.2106764 + 0.3707428 + 0.2224394 + 0.1046818) return 4;   // 10.46818%
        return 5;   // 2.61665%
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

extern "C" std::unique_ptr<Pu238SpontaneousFissionSource> openmc_create_source(std::string parameters) {
    return std::make_unique<Pu238SpontaneousFissionSource>();
}
