#ifndef STAN_MATH_PRIM_PROB_CHI_SQUARE_LCDF_HPP
#define STAN_MATH_PRIM_PROB_CHI_SQUARE_LCDF_HPP

#include <stan/math/prim/meta.hpp>
#include <stan/math/prim/err.hpp>
#include <stan/math/prim/fun/constants.hpp>
#include <stan/math/prim/fun/digamma.hpp>
#include <stan/math/prim/fun/exp.hpp>
#include <stan/math/prim/fun/gamma_p.hpp>
#include <stan/math/prim/fun/grad_reg_inc_gamma.hpp>
#include <stan/math/prim/fun/log.hpp>
#include <stan/math/prim/fun/max_size.hpp>
#include <stan/math/prim/fun/scalar_seq_view.hpp>
#include <stan/math/prim/fun/size.hpp>
#include <stan/math/prim/fun/size_zero.hpp>
#include <stan/math/prim/fun/tgamma.hpp>
#include <stan/math/prim/fun/value_of.hpp>
#include <stan/math/prim/functor/partials_propagator.hpp>
#include <cmath>

namespace stan {
namespace math {

/** \ingroup prob_dists
 * Returns the chi square log cumulative distribution function for the given
 * variate and degrees of freedom. If given containers of matching sizes,
 * returns the log sum of probabilities.
 *
 * @tparam T_y type of scalar parameter
 * @tparam T_dof type of degrees of freedom parameter
 * @param y scalar parameter
 * @param nu degrees of freedom parameter
 * @return log probability or log sum of probabilities
 * @throw std::domain_error if y is negative or nu is nonpositive
 * @throw std::invalid_argument if container sizes mismatch
 */
template <typename T_y, typename T_dof>
return_type_t<T_y, T_dof> chi_square_lcdf(const T_y& y, const T_dof& nu) {
  using T_partials_return = partials_return_t<T_y, T_dof>;
  using std::exp;
  using std::log;
  using std::pow;
  using T_y_ref = ref_type_t<T_y>;
  using T_nu_ref = ref_type_t<T_dof>;
  static const char* function = "chi_square_lcdf";
  check_consistent_sizes(function, "Random variable", y,
                         "Degrees of freedom parameter", nu);
  T_y_ref y_ref = y;
  T_nu_ref nu_ref = nu;
  check_not_nan(function, "Random variable", y_ref);
  check_nonnegative(function, "Random variable", y_ref);
  check_positive_finite(function, "Degrees of freedom parameter", nu_ref);

  if (size_zero(y, nu)) {
    return 0;
  }

  T_partials_return cdf_log(0.0);
  auto ops_partials = make_partials_propagator(y_ref, nu_ref);

  scalar_seq_view<T_y_ref> y_vec(y_ref);
  scalar_seq_view<T_nu_ref> nu_vec(nu_ref);
  size_t N = max_size(y, nu);

  // Explicit return for extreme values
  // The gradients are technically ill-defined, but treated as zero
  for (size_t i = 0; i < stan::math::size(y); i++) {
    if (y_vec.val(i) == 0) {
      return ops_partials.build(negative_infinity());
    }
  }

  VectorBuilder<!is_constant_all<T_dof>::value, T_partials_return, T_dof>
      gamma_vec(math::size(nu));
  VectorBuilder<!is_constant_all<T_dof>::value, T_partials_return, T_dof>
      digamma_vec(math::size(nu));

  if (!is_constant_all<T_dof>::value) {
    for (size_t i = 0; i < stan::math::size(nu); i++) {
      const T_partials_return alpha_dbl = nu_vec.val(i) * 0.5;
      gamma_vec[i] = tgamma(alpha_dbl);
      digamma_vec[i] = digamma(alpha_dbl);
    }
  }

  for (size_t n = 0; n < N; n++) {
    // Explicit results for extreme values
    // The gradients are technically ill-defined, but treated as zero
    if (y_vec.val(n) == INFTY) {
      return ops_partials.build(0.0);
    }

    const T_partials_return y_dbl = y_vec.val(n);
    const T_partials_return alpha_dbl = nu_vec.val(n) * 0.5;
    const T_partials_return beta_dbl = 0.5;

    const T_partials_return Pn = gamma_p(alpha_dbl, beta_dbl * y_dbl);

    cdf_log += log(Pn);

    if (!is_constant_all<T_y>::value) {
      partials<0>(ops_partials)[n] += beta_dbl * exp(-beta_dbl * y_dbl)
                                      * pow(beta_dbl * y_dbl, alpha_dbl - 1)
                                      / tgamma(alpha_dbl) / Pn;
    }
    if (!is_constant_all<T_dof>::value) {
      partials<1>(ops_partials)[n]
          -= 0.5
             * grad_reg_inc_gamma(alpha_dbl, beta_dbl * y_dbl, gamma_vec[n],
                                  digamma_vec[n])
             / Pn;
    }
  }
  return ops_partials.build(cdf_log);
}

}  // namespace math
}  // namespace stan
#endif
