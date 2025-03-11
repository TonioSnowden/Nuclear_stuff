#include <memory>
#include <cmath>
#include "openmc/random_lcg.h"
#include "openmc/source.h"
#include "openmc/particle.h"
#include "openmc/distribution.h"

class Cf250SpontaneousFissionSource : public openmc::Source {
private:
    // Note: You might want to verify these Watt parameters for Cf-250
    openmc::Watt watt_dist{1.18, 0.8475};

    // Sample number of neutrons using discrete distribution for Cf-250
    int sample_num_neutrons(uint64_t* seed) const {
        double xi = openmc::prn(seed);
        if (xi < 0.0038191) return 0;        // 0.217%
        if (xi < 0.0038191 + 0.0365432) return 1;   // 2.556%
        if (xi < 0.0038191 + 0.0365432 + 0.1673371) return 2;   // 12.741%
        if (xi < 0.0038191 + 0.0365432 + 0.1673371 + 0.2945302) return 3;   // 27.72%
        if (xi < 0.0038191 + 0.0365432 + 0.1673371 + 0.2945302 + 0.2982732) return 4;   // 30.517%
        if (xi < 0.0038191 + 0.0365432 + 0.1673371 + 0.2945302 + 0.2982732 + 0.1451396) return 5;   // 18.529%
        if (xi < 0.0038191 + 0.0365432 + 0.1673371 + 0.2945302 + 0.2982732 + 0.1451396 + 0.0472215) return 6;   // 6.607%
        if (xi < 0.0038191 + 0.0365432 + 0.1673371 + 0.2945302 + 0.2982732 + 0.1451396 + 0.0472215 + 0.0040174) return 7;   // 1.414%
        return 8;   // 0.006%
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

extern "C" std::unique_ptr<Cf250SpontaneousFissionSource> openmc_create_source(std::string parameters) {
    return std::make_unique<Cf250SpontaneousFissionSource>();
}
