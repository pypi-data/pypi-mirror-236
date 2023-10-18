// copyright ############################### #
// This file is part of the Xcoll Package.   #
// Copyright (c) CERN, 2023.                 #
// ######################################### #

#ifndef XCOLL_EVEREST_ENGINE_H
#define XCOLL_EVEREST_ENGINE_H

/*gpufun*/
void Drift_single_particle_4d(LocalParticle* part, double length){
    double zeta = LocalParticle_get_zeta(part);
    Drift_single_particle(part, length);
    LocalParticle_set_zeta(part, zeta);
}

/*gpufun*/
double drift_zeta_single(double rvv, double xp, double yp, double length){
    double const rv0v = 1./rvv;
    double const dzeta = 1 - rv0v * (1. + (pow(xp,2.) + pow(yp,2.))/2.);
    return length * dzeta;
}

/*gpukern*/
void RandomRutherford_set_by_xcoll_material(RandomRutherfordData ran, GeneralMaterialData material){
    double const zatom    = GeneralMaterialData_get_Z(material);
    double const emr      = GeneralMaterialData_get_nuclear_radius(material);
    double const hcut     = GeneralMaterialData_get_hcut(material);
    double const lcut     = 0.0009982;
    double const c = 0.8561e3; // TODO: Where tha fuck does this come from??
    double A = pow(zatom,2);
    double B = c*pow(emr,2);
    RandomRutherford_set(ran, A, B, lcut, hcut);
}

#endif /* XCOLL_EVEREST_ENGINE_H */
