# liquidations.py
"""
Liquidation Logic with Cascade Potential

Liquidations execute as aggressive orders against the book,
creating price impact that can trigger further liquidations.
"""


def check_liquidations(state, mark_price: float, maintenance_margin_rate: float) -> list:
    """Return list of agent_ids that should be liquidated"""
    liquidatable = []
    for agent_id, pos in state.position_manager.positions.items():
        notional = abs(pos.size * mark_price)
        if notional > 0:
            margin_ratio = abs(pos.realized_pnl + pos.unrealized_pnl) / notional
            if margin_ratio < maintenance_margin_rate:
                liquidatable.append(agent_id)
    return liquidatable


def execute_liquidation(state, agent_id: int, price: float, config):
    """Liquidate position. Returns (size_liquidated, price_impact)"""
    if agent_id not in state.position_manager.positions:
        return 0.0, 0.0

    pos = state.position_manager.positions[agent_id]
    size_liquidated = abs(pos.size)

    # Realized PnL from closing
    direction = 1 if pos.side == 'long' else -1
    realized = size_liquidated * (price - pos.entry_price) * direction
    pos.realized_pnl += realized

    # Liquidation penalty
    penalty = size_liquidated * price * config.LIQUIDATION_PENALTY
    pos.realized_pnl -= penalty

    # Remove position
    del state.position_manager.positions[agent_id]

    # Price impact for potential cascade
    impact = size_liquidated * config.IMPACT_COEFFICIENT

    return size_liquidated, impact