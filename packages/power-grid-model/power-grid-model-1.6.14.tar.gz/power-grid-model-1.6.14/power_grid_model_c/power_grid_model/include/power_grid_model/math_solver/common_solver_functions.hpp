// SPDX-FileCopyrightText: 2022 Contributors to the Power Grid Model project <dynamic.grid.calculation@alliander.com>
//
// SPDX-License-Identifier: MPL-2.0

#pragma once
#ifndef POWER_GRID_MODEL_COMMON_SOLVER_FUNCTIONS_HPP
#define POWER_GRID_MODEL_COMMON_SOLVER_FUNCTIONS_HPP

#include "y_bus.hpp"

#include "../calculation_parameters.hpp"

namespace power_grid_model::common_solver_functions {

template <bool sym>
void add_sources(grouped_idx_vector_type auto const& sources_per_bus, Idx const& bus_number, YBus<sym> const& y_bus,
                 ComplexVector const& u_source_vector, ComplexTensor<sym>& diagonal_element, ComplexValue<sym>& u_bus) {
    for (Idx const source_number : sources_per_bus.get_element_range(bus_number)) {
        ComplexTensor<sym> const y_source = y_bus.math_model_param().source_param[source_number];
        diagonal_element += y_source; // add y_source to the diagonal of Ybus
        u_bus += dot(y_source, ComplexValue<sym>{u_source_vector[source_number]}); // rhs += Y_source * U_source
    }
}

template <bool sym> void copy_y_bus(YBus<sym> const& y_bus, ComplexTensorVector<sym>& mat_data) {
    ComplexTensorVector<sym> const& ydata = y_bus.admittance();
    std::transform(y_bus.map_lu_y_bus().cbegin(), y_bus.map_lu_y_bus().cend(), mat_data.begin(), [&](Idx k) {
        if (k == -1) {
            return ComplexTensor<sym>{};
        }
        return ydata[k];
    });
}

template <bool sym>
void calculate_source_result(Idx const& bus_number, YBus<sym> const& y_bus, PowerFlowInput<sym> const& input,
                             MathOutput<sym>& output, grouped_idx_vector_type auto const& sources_per_bus) {
    for (Idx const source : sources_per_bus.get_element_range(bus_number)) {
        ComplexValue<sym> const u_ref{input.source[source]};
        ComplexTensor<sym> const y_ref = y_bus.math_model_param().source_param[source];
        output.source[source].i = dot(y_ref, u_ref - output.u[bus_number]);
        output.source[source].s = output.u[bus_number] * conj(output.source[source].i);
    }
}

template <bool sym, class LoadGenFunc>
void calculate_load_gen_result(Idx const& bus_number, PowerFlowInput<sym> const& input, MathOutput<sym>& output,
                               grouped_idx_vector_type auto const& load_gens_per_bus,
                               LoadGenFunc const& load_gen_func) {
    for (auto load_gen : load_gens_per_bus.get_element_range(bus_number)) {
        switch (LoadGenType const type = load_gen_func(load_gen); type) {
            using enum LoadGenType;

        case const_pq:
            // always same power
            output.load_gen[load_gen].s = input.s_injection[load_gen];
            break;
        case const_y:
            // power is quadratic relation to voltage
            output.load_gen[load_gen].s = input.s_injection[load_gen] * abs2(output.u[bus_number]);
            break;
        case const_i:
            // power is linear relation to voltage
            output.load_gen[load_gen].s = input.s_injection[load_gen] * cabs(output.u[bus_number]);
            break;
        default:
            throw MissingCaseForEnumError("Power injection", type);
        }
        output.load_gen[load_gen].i = conj(output.load_gen[load_gen].s / output.u[bus_number]);
    }
}

} // namespace power_grid_model::common_solver_functions

#endif
