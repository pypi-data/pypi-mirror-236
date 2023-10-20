import numpy as np
import scipy.stats as st

from hestia_earth.distribution.likelihood import generate_likl_file
from .cycle import YIELD_COLUMN, FERTILISER_COLUMNS


def _compute_MC_likelihood(candidate: list, kernel):
    iso = kernel(candidate)
    sample = kernel.resample(size=10000)
    insample = kernel(sample) < iso
    integral = insample.sum() / float(insample.shape[0])
    return integral


def _get_data_bounds(data: list):
    return (data, min(data), max(data)) if len(data) > 0 else ([], None, None)


def _get_df_bounds(df, columns):
    df = df[columns].dropna(axis=0, how='any')
    results = [_get_data_bounds(df[col].to_list()) for col in columns] if len(df) > 0 else (
            [None, None, None]
    )
    return [[r[i] for r in results] for i in range(3)]  # [m, mins, maxs]


def _fit_user_data_mv(candidate, df, columns=list, return_z: bool = False, dim_x: int = 0, dim_y: int = 1):
    m, mins, maxs = _get_df_bounds(df, columns)

    plottable = all([m[i] != [] and mins[i] != maxs[i] for i in range(len(m))])

    values = np.vstack(m)
    likelihood = _compute_MC_likelihood(candidate, st.gaussian_kde(values)) if (
                                        plottable and ~np.isnan(candidate).any()) else None

    def calculate_Z(dim_x: int = 0, dim_y: int = 1):
        X, Y = np.mgrid[mins[dim_x]:maxs[dim_x]:100j, mins[dim_y]:maxs[dim_y]:100j]
        positions = np.vstack([X.ravel(), Y.ravel()])

        kernel = st.gaussian_kde(values)
        Z = np.reshape(kernel(positions).T, X.shape)
        return Z / Z.sum()

    return likelihood, calculate_Z(dim_x, dim_y) if return_z and plottable else [
           [mins[dim_x], maxs[dim_x]], [[mins[dim_y], maxs[dim_y]]]
           ]


def calculate_fit_mv(candidate: list, country_id: str, product_id: str,
                     columns=FERTILISER_COLUMNS[:3] + [YIELD_COLUMN],
                     return_z: bool = False):
    """
    Return the likelihood of a combination of candidate values using bivariate or multivariate distribution.
    The returned probability approximates how reasonable the candidate is by using Monte Carlo integration.
    Any returned probability above 5% should be acceptable.

    Parameters
    ----------
    candidate: list
        List of values to be tested following the order of 'columns', e.g. [250, 8500] by default
        meaning the Nitrogen use is 250 and yield is 8500.
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR'.
    product_id: str
        Product term `@id` from Hestia glossary, e.g. 'wheatGrain'.
    columns: list
        List of column names in the likelihood csv file, by defualt:
        'Nitrogen (kg N)' and 'Grain yield (kg/ha)'
    return_z: bool
        Whether to calculate Z for plotting. Defaults to `False`.
        Only set to 'True' when plotting 2D distributions.

    Returns
    -------
    likelihood: float
        The probability of how likely the candidate is reasonable, or an
        approximation of what percentage of samples the candidate stands above
    """
    df = generate_likl_file(country_id, product_id)
    return _fit_user_data_mv(candidate, df, columns, return_z=return_z)


def calculate_fit_2d(candidate: list, country_id: str, product_id: str,
                     columns=[FERTILISER_COLUMNS[0], YIELD_COLUMN],
                     return_z: bool = False):
    """
    Return the likelihood of a combination of candidate values using bivariate distribution.
    The returned probability approximates how reasonable the candidate is by using Monte Carlo integration.
    Any returned probability above 5% should be acceptable.

    Parameters
    ----------
    candidate: list
        List of values to be tested following the order of 'columns', e.g. [250, 8500] by default
        meaning the Nitrogen use is 250 and yield is 8500.
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR'.
    product_id: str
        Product term `@id` from Hestia glossary, e.g. 'wheatGrain'.
    columns: list
        List of column names in the likelihood csv file, by defualt:
        'Nitrogen (kg N)' and 'Grain yield (kg/ha)'
    return_z: bool
        Whether to calculate Z for plotting. Defaults to `False`.

    Returns
    -------
    likelihood: float
        The probability of how likely the candidate is reasonable, or an
        approximation of what percentage of samples the candidate stands above
    """
    return calculate_fit_mv(candidate, country_id, product_id, columns, return_z)
