#ifndef STAN_MATH_PRIM_PROB_POISSON_CDF_HPP
#define STAN_MATH_PRIM_PROB_POISSON_CDF_HPP

#include <stan/math/prim/meta.hpp>
#include <stan/math/prim/err.hpp>
#include <stan/math/prim/fun/as_column_vector_or_scalar.hpp>
#include <stan/math/prim/fun/as_array_or_scalar.hpp>
#include <stan/math/prim/fun/as_value_column_array_or_scalar.hpp>
#include <stan/math/prim/fun/exp.hpp>
#include <stan/math/prim/fun/gamma_q.hpp>
#include <stan/math/prim/fun/max_size.hpp>
#include <stan/math/prim/fun/promote_scalar.hpp>
#include <stan/math/prim/fun/size.hpp>
#include <stan/math/prim/fun/size_zero.hpp>
#include <stan/math/prim/fun/tgamma.hpp>
#include <stan/math/prim/fun/to_ref.hpp>
#include <stan/math/prim/fun/value_of.hpp>
#include <stan/math/prim/functor/partials_propagator.hpp>
#include <cmath>
#include <limits>

namespace stan {
namespace math {

// Poisson CDF
template <typename T_n, typename T_rate>
return_type_t<T_rate> poisson_cdf(const T_n& n, const T_rate& lambda) {
  using T_partials_return = partials_return_t<T_n, T_rate>;
  using T_n_ref = ref_type_if_t<!is_constant<T_n>::value, T_n>;
  using T_lambda_ref = ref_type_if_t<!is_constant<T_rate>::value, T_rate>;
  using std::pow;
  static const char* function = "poisson_cdf";
  check_consistent_sizes(function, "Random variable", n, "Rate parameter",
                         lambda);

  T_n_ref n_ref = n;
  T_lambda_ref lambda_ref = lambda;

  decltype(auto) n_val = to_ref(as_value_column_array_or_scalar(n_ref));
  decltype(auto) lambda_val
      = to_ref(as_value_column_array_or_scalar(lambda_ref));

  check_nonnegative(function, "Rate parameter", lambda_val);

  if (size_zero(n, lambda)) {
    return 1.0;
  }

  auto ops_partials = make_partials_propagator(lambda_ref);

  if (sum(promote_scalar<int>(n_val < 0))) {
    return ops_partials.build(0.0);
  }

  const auto& Pi = to_ref_if<!is_constant_all<T_rate>::value>(
      gamma_q(n_val + 1.0, lambda_val));

  T_partials_return P = prod(Pi);

  if (!is_constant_all<T_rate>::value) {
    partials<0>(ops_partials) = -exp(-lambda_val) * pow(lambda_val, n_val)
                                / (tgamma(n_val + 1.0) * Pi) * P;
  }

  return ops_partials.build(P);
}

}  // namespace math
}  // namespace stan
#endif
