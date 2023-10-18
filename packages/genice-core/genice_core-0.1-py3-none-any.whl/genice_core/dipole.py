import itertools as it
from logging import getLogger

import numpy as np


def minimize_net_dipole(paths, pos, maxiter=2000, pbc=False):
    """Minimize the net polarization by flipping paths.

    Args:
        paths (_type_): List of directed paths
        pos (_type_): Positions of the nodes
        maxiter (int, optional): Number of random orientations for the paths. Defaults to 1000.
        cell: Periodic cell; it it is given, the positions of the nodes must be in the fractional coordinate system.
    Returns:
        list of paths: Optimized paths.
    """
    logger = getLogger()

    # polarized chains and cycles. Small cycle of dipoles are eliminated.
    polarized = []

    dipoles = []
    for i, path in enumerate(paths):
        if pbc:
            # vectors between adjacent vertices.
            displace = pos[path[1:]] - pos[path[:-1]]
            # PBC wrap
            displace -= np.floor(displace + 0.5)
            # total dipole along the chain (or a cycle)
            chain_pol = np.sum(displace, axis=0)
            # if it is large enough,
            if chain_pol @ chain_pol > 1e-6:
                logger.debug(path)
                dipoles.append(chain_pol)
                polarized.append(i)
        else:
            # dipole moment of a path; NOTE: No PBC.
            if path[0] != path[-1]:
                # If no PBC, a chain pol is simply an end-to-end pol.
                chain_pol = pos[path[-1]] - pos[path[0]]
                dipoles.append(chain_pol)
                polarized.append(i)
    dipoles = np.array(dipoles)
    # logger.debug(dipoles)

    pol_optimal = np.sum(dipoles, axis=0)
    logger.info(f"init {np.linalg.norm(pol_optimal)} dipole")
    parity_optimal = np.ones(len(dipoles))
    for loop in range(maxiter):
        parity = np.random.randint(2, size=len(dipoles)) * 2 - 1
        net_pol = parity @ dipoles
        if net_pol @ net_pol < pol_optimal @ pol_optimal:
            pol_optimal = net_pol
            parity_optimal = parity
            logger.info(f"{loop} {np.linalg.norm(pol_optimal)} dipole")
            if pol_optimal @ pol_optimal < 1e-10:
                break

    for i, dir in zip(polarized, parity_optimal):
        if dir < 0:
            paths[i] = paths[i][::-1]

    VERIFY = False
    if VERIFY:
        # assert the chains are properly inversed.

        dipoles = []
        for i, path in enumerate(paths):
            # dipole moment of a path; NOTE: No PBC.
            if path[0] != path[-1]:
                # If no PBC, a chain pol is simply an end-to-end pol.
                chain_pol = pos[path[-1]] - pos[path[0]]
                dipoles.append(chain_pol)
        dipoles = np.array(dipoles)

        pol = np.sum(dipoles, axis=0)
        pol -= pol_optimal
        assert pol @ pol < 1e-20

    return paths
