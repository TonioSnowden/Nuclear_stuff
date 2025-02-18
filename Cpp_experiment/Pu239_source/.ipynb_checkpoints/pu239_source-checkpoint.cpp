#include <memory>
#include <cmath>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "openmc/distribution.h"

class Pu239SpontaneousFissionSource : public openmc::Source {
private:
    // Maxwell distribution for Pu-239 (parameters would need to be adjusted)
    openmc::Watt watt_dist{0.794930, 4.689270}; // Note: Keep these parameters as they are if no specific values are given

    // Sample number of neutrons using discrete distribution for Pu-239
    int sample_num_neutrons(uint64_t* seed) const {
        double xi = openmc::prn(seed);
        if (xi < 0.0084842) return 0;        // 0.84842%
        if (xi < 0.0084842 + 0.0790030) return 1;   // 7.90030%
        if (xi < 0.0084842 + 0.0790030 + 0.2536173) return 2;   // 25.36173%
        if (xi < 0.0084842 + 0.0790030 + 0.2536173 + 0.3288770) return 3;   // 32.88770%
        if (xi < 0.0084842 + 0.0790030 + 0.2536173 + 0.3288770 + 0.2323811) return 4;   // 23.23811%
        if (xi < 0.0084842 + 0.0790030 + 0.2536173 + 0.3288770 + 0.2323811 + 0.0800161) return 5;   // 8.00161%
        if (xi < 0.0084842 + 0.0790030 + 0.2536173 + 0.3288770 + 0.2323811 + 0.0800161 + 0.0155581) return 6;   // 1.55581%
        if (xi < 0.0084842 + 0.0790030 + 0.2536173 + 0.3288770 + 0.2323811 + 0.0800161 + 0.0155581 + 0.0011760) return 7;   // 0.11760%
        return 8;   // remaining (0.003469%)
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

extern "C" std::unique_ptr<Pu239SpontaneousFissionSource> openmc_create_source(std::string parameters) {
    return std::make_unique<Pu239SpontaneousFissionSource>();
}
