# simulation.py
"""
Main Simulation Runner with Position & PnL Tracking
"""
# from config import Config
# from state import SimulationState
# from matching import process_order
# from funding import sample_premium, calculate_hourly_funding
# from agents.market_maker import MarketMaker
# from agents.taker import Taker
# from oracle import Oracle
# from positions import PositionManager
# import numpy as np

"""Basic version, working"""
# def run_simulation(config):
#     """Run the full simulation"""
#     #state = create_initial_state(config)
#     oracle = Oracle(config.INITIAL_PRICE)
#     position_manager = PositionManager()
#     premium_samples = []
#
#     market_makers = []
#     for i in range(config.NUM_MARKET_MAKERS):
#         strategy = config.MM_STRATEGY_TYPES[i % len(config.MM_STRATEGY_TYPES)]
#         market_makers.append(MarketMaker(i, strategy))
#
#     takers = [Taker(i) for i in range(config.NUM_TAKERS)]
#
#     for step in range(int(config.SIM_DURATION / config.DT)):
#         current_time = step * config.DT
#
#         # Update mark price
#         mark_price, oracle_price = oracle.update(
#             config.INITIAL_PRICE * (1 + 0.00005 * step),
#             mark_price if 'mark_price' in locals() else config.INITIAL_PRICE
#         )
#
#         # Takers open positions
#         for taker in takers:
#             if np.random.random() < 0.25:
#                 side, price, size = taker.get_order(mark_price)
#                 filled, avg_price = process_order(state, side, price, size, current_time, taker.agent_id)
#                 if filled > 0:
#                     position_manager.open_or_update(taker.agent_id, side, filled, avg_price, current_time)
#
#         # Market makers quote
#         for mm in market_makers:
#             bid, ask = mm.get_quotes(mark_price)
#             if bid:
#                 process_order(state, 'buy', bid, 5.0, current_time, mm.agent_id)
#             if ask:
#                 process_order(state, 'sell', ask, 5.0, current_time, mm.agent_id)
#
#         # Update PnL
#         position_manager.update_unrealized(mark_price)
#
#         # Funding
#         sample_premium(premium_samples, mark_price, oracle_price)
#         if int(current_time) % config.FUNDING_INTERVAL == 0:
#             rate = calculate_hourly_funding(premium_samples)
#             position_manager.apply_funding(rate)
#
#         # Liquidations
#         liquidatable = position_manager.get_liquidatable(mark_price, config.MAINTENANCE_MARGIN_RATE)
#         for aid in liquidatable:
#             # Simple liquidation
#             position_manager.close_position(aid, mark_price * 0.99)
#
#         state.record_price(mark_price)
#     # Print summary
#     print(f"Simulation completed: {len(state['price_history'])} steps")
#     print(f"Final price: {state['price_history'][-1]:.2f}")
#     print(f"Number of positions open: {len(state.get('positions', {}))}")
#
#     from metrics import print_simulation_summary
#     print_simulation_summary(state, position_manager)
#
#     return state, position_manager

# simulation.py
"""
Simulation Runner
"""
from config import Config
from state import SimulationState
from matching import process_order
from funding import sample_premium, calculate_hourly_funding
from agents.market_maker import MarketMaker
from agents.taker import Taker
from oracle import Oracle
from positions import PositionManager
from liquidations import check_liquidations, execute_liquidation
from metrics import calculate_pnl_summary, print_simulation_summary
import numpy as np
from visualizations import plot_price_path_debug


# def run_simulation(config):
#     """Full version with all features restored"""
#     state = SimulationState.create_initial_state(config)
#     oracle = Oracle(config.INITIAL_PRICE)
#
#     # Data collection
#     premium_samples = []
#     oracle_prices = []
#     funding_history = []
#     mm_pnl_history = {i: [] for i in range(config.NUM_MARKET_MAKERS)}
#     inventory_history = {i: [] for i in range(config.NUM_MARKET_MAKERS)}
#     total_pnl_history = []
#     liquidation_times = []
#     liquidation_volumes = [0] * (int(config.SIM_DURATION / config.DT) + 10)
#
#     market_makers = [MarketMaker(i, "inventory_aware") for i in range(config.NUM_MARKET_MAKERS)]
#     takers = [Taker(i, "random") for i in range(config.NUM_TAKERS)]
#
#     for step in range(int(config.SIM_DURATION / config.DT)):
#         current_time = step * config.DT
#
#         # === PRICE UPDATE ===
#         mark_price, oracle_price = oracle.update(
#             config.INITIAL_PRICE * (1 + 0.00005 * step),
#             mark_price if 'mark_price' in locals() else config.INITIAL_PRICE
#         )
#         state.record_price(mark_price)
#         oracle_prices.append(oracle_price)
#
#         # Takers
#         for taker in takers:
#             if np.random.random() < 0.25:
#                 side, price, size = taker.get_order(mark_price)
#                 filled, avg_price = process_order(state, side, price, size, current_time, taker.agent_id)
#                 if filled > 0:
#                     state.position_manager.open_or_update(taker.agent_id, side, filled, avg_price, current_time)
#
#         # Market Makers
#         for mm in market_makers:
#             bid, ask = mm.get_quotes(mark_price)
#             if bid:
#                 process_order(state, 'buy', bid, 5.0, current_time, mm.agent_id)
#             if ask:
#                 process_order(state, 'sell', ask, 5.0, current_time, mm.agent_id)
#
#         # PnL Update
#         state.position_manager.update_unrealized(mark_price)
#
#         # Funding
#         sample_premium(premium_samples, mark_price, oracle_price)
#         if int(current_time) % config.FUNDING_INTERVAL == 0 and premium_samples:
#             rate = calculate_hourly_funding(premium_samples)
#             funding_history.append(rate)
#             state.position_manager.apply_funding(rate)
#
#         # Liquidations
#         if step % 20 == 0:  # more frequent for visibility
#             liquidatable = state.position_manager.get_liquidatable(mark_price, config.MAINTENANCE_MARGIN_RATE)
#             for aid in liquidatable:
#                 size_liq, _ = execute_liquidation(state, aid, mark_price, config)
#                 liquidation_times.append(step)
#                 if step < len(liquidation_volumes):
#                     liquidation_volumes[step] += size_liq
#
#         # Track metrics
#         total_pnl = sum(p.realized_pnl + p.unrealized_pnl for p in state.position_manager.positions.values())
#         total_pnl_history.append(total_pnl)
#
#         for mm in market_makers:
#             mm_pnl_history[mm.agent_id].append(total_pnl)
#             inventory_history[mm.agent_id].append(mm.inventory)
#
#     # === FINAL PLOTS ===
#     from visualizations import plot_price_path, plot_funding_rate, plot_mm_pnl_over_time
#     from visualizations import plot_equity_curve, plot_drawdown, plot_inventory_over_time
#
#     plot_price_path(state, oracle_prices, liquidation_times, liquidation_volumes)
#     if funding_history:
#         plot_funding_rate(funding_history)
#     plot_mm_pnl_over_time(mm_pnl_history)
#     plot_equity_curve(total_pnl_history)
#     plot_drawdown(total_pnl_history)
#     plot_inventory_over_time(inventory_history)
#
#     print("Simulation finished. Final price:", state.price_history[-1])
#     return state
# def run_simulation(config):
#     """Full simulation runner with toggleable plots"""
#     np.random.seed(config.RANDOM_SEED)
#     state = SimulationState.create_initial_state(config)
#     oracle = Oracle(config.INITIAL_PRICE)
#     # Data collection
#     premium_samples = []
#     oracle_prices = [config.INITIAL_PRICE]
#     funding_history = []
#     mm_pnl_history = {i: [] for i in range(config.NUM_MARKET_MAKERS)}
#     inventory_history = {i: [] for i in range(config.NUM_MARKET_MAKERS)}
#     total_pnl_history = []
#     liquidation_times = []
#     liquidation_volumes = [0] * (int(config.SIM_DURATION / config.DT) + 100)
#
#     # Order book metrics
#     order_book_snapshots = []
#     spread_history = []
#     imbalance_history = []
#
#     # Diversified strategies
#     strategy_pool = [
#         "inventory_aware",
#         "passive",
#         "aggressive",
#         "volatility_aware",
#         "momentum",
#         "mean_reversion"
#     ]
#
#     market_makers = []
#     for i in range(config.NUM_MARKET_MAKERS):
#         strategy = strategy_pool[i % len(strategy_pool)]
#         market_makers.append(MarketMaker(i, strategy))
#
#
#     takers = [Taker(i, "random") for i in range(config.NUM_TAKERS)]
#
#     for step in range(int(config.SIM_DURATION / config.DT)):
#         current_time = step * config.DT
#
#         # Price update
#         mark_price, oracle_price = oracle.update(
#             config.INITIAL_PRICE * (1 + 0.00005 * step),
#             mark_price if 'mark_price' in locals() else config.INITIAL_PRICE
#         )
#         state.record_price(mark_price)
#         oracle_prices.append(oracle_price)
#
#         # Takers
#         for taker in takers:
#             if np.random.random() < 0.25:
#                 side, price, size = taker.get_order(mark_price)
#                 filled, avg_price = process_order(state, side, price, size, current_time, taker.agent_id)
#                 if filled > 0:
#                     state.position_manager.open_or_update(taker.agent_id, side, filled, avg_price, current_time)
#
#         # Market Makers
#         for mm in market_makers:
#             bid, ask = mm.get_quotes(mark_price)
#             if bid:
#                 process_order(state, 'buy', bid, 5.0, current_time, mm.agent_id)
#             if ask:
#                 process_order(state, 'sell', ask, 5.0, current_time, mm.agent_id)
#
#         state.position_manager.update_unrealized(mark_price)
#
#         # Funding
#         sample_premium(premium_samples, mark_price, oracle_price)
#         if int(current_time) % config.FUNDING_INTERVAL == 0 and premium_samples:
#             rate = calculate_hourly_funding(premium_samples)
#             funding_history.append(rate)
#             state.position_manager.apply_funding(rate)
#
#         # Liquidations
#         if step % 20 == 0:
#             liquidatable = state.position_manager.get_liquidatable(mark_price, config.MAINTENANCE_MARGIN_RATE)
#             for aid in liquidatable:
#                 size_liq, _ = execute_liquidation(state, aid, mark_price, config)
#                 liquidation_times.append(step)
#                 if step < len(liquidation_volumes):
#                     liquidation_volumes[step] += size_liq
#
#         # Order Book Metrics
#         if step % 100 == 0:
#             depth = state.order_book.get_depth(levels=5)
#             bid_depth = sum(size for _, size in depth['bids'])
#             ask_depth = sum(size for _, size in depth['asks'])
#
#             best_bid = state.order_book.get_best_bid()
#             best_ask = state.order_book.get_best_ask()
#             spread = (best_ask.price - best_bid.price) if best_bid and best_ask else 0.0
#
#             imbalance = (bid_depth - ask_depth) / (bid_depth + ask_depth + 1e-8)
#
#             order_book_snapshots.append((bid_depth, ask_depth))
#             spread_history.append(spread)
#             imbalance_history.append(imbalance)
#
#         # PnL tracking
#         total_pnl = sum(p.realized_pnl + p.unrealized_pnl for p in state.position_manager.positions.values())
#         total_pnl_history.append(total_pnl)
#
#         for mm in market_makers:
#             mm_pnl_history[mm.agent_id].append(total_pnl)
#             inventory_history[mm.agent_id].append(mm.inventory)
#
#     # === CONDITIONAL PLOTS ===
#     from visualizations import (
#         plot_price_path, plot_funding_rate, plot_mm_pnl_over_time,
#         plot_equity_curve, plot_drawdown, plot_inventory_over_time,
#         plot_orderbook_depth, plot_spread_over_time, plot_imbalance,
#         plot_sharpe_sortino
#     )
#
#     if getattr(config, 'PLOT_PRICE_AND_LIQS', True):
#         plot_price_path(state, oracle_prices, liquidation_times, liquidation_volumes)
#     if getattr(config, 'PLOT_FUNDING', True) and funding_history:
#         plot_funding_rate(funding_history)
#     if getattr(config, 'PLOT_MM_PNL', True):
#         plot_mm_pnl_over_time(mm_pnl_history)
#     if getattr(config, 'PLOT_EQUITY_CURVE', True):
#         plot_equity_curve(total_pnl_history)
#     if getattr(config, 'PLOT_DRAWDOWN', True):
#         plot_drawdown(total_pnl_history)
#     if getattr(config, 'PLOT_INVENTORY', True):
#         plot_inventory_over_time(inventory_history)
#     if getattr(config, 'PLOT_ORDERBOOK_DEPTH', True):
#         plot_orderbook_depth(order_book_snapshots)
#     if getattr(config, 'PLOT_SPREAD', True) and spread_history:
#         plot_spread_over_time(spread_history)
#     if getattr(config, 'PLOT_IMBALANCE', True) and imbalance_history:
#         plot_imbalance(imbalance_history)
#     if getattr(config, 'PLOT_SHARPE_SORTINO', True):
#         plot_sharpe_sortino(mm_pnl_history)
#
#     print(f"Simulation finished. Final price: {state.price_history[-1]:.2f}")
#     return state


def run_simulation(config):
    """Full simulation with realistic price paths + diversified MM strategies"""
    np.random.seed(config.PRICE_RANDOM_SEED if hasattr(config, 'SIM_RANDOM_SEED') else 42)
    state = SimulationState.create_initial_state(config)

    # === PRICE PATH GENERATOR ===
    from price_path import PricePathGenerator, PricePathConfig
    path_config = PricePathConfig(
        initial_price=config.INITIAL_PRICE,
        num_steps=int(config.SIM_DURATION / config.DT),
        seed=config.PRICE_RANDOM_SEED if hasattr(config, 'PRICE_RANDOM_SEED') else 42
    )
    generator = PricePathGenerator(path_config)
    price_path, _ = generator.generate_with_regimes()  # regime_labels not used yet

    # Data collection
    oracle_prices = [config.INITIAL_PRICE]
    premium_samples = []
    funding_history = []
    mm_pnl_history = {i: [] for i in range(config.NUM_MARKET_MAKERS)}
    inventory_history = {i: [] for i in range(config.NUM_MARKET_MAKERS)}
    total_pnl_history = []
    liquidation_times = []
    liquidation_volumes = [0] * (int(config.SIM_DURATION / config.DT) + 100)

    order_book_snapshots = []
    spread_history = []
    imbalance_history = []

    # Diversified Market Makers
    strategy_pool = ["inventory_aware", "passive", "aggressive", "volatility_aware", "momentum", "mean_reversion"]
    market_makers = [MarketMaker(i, strategy_pool[i % len(strategy_pool)])
                     for i in range(config.NUM_MARKET_MAKERS)]

    takers = [Taker(i, "random") for i in range(config.NUM_TAKERS)]

    for step in range(int(config.SIM_DURATION / config.DT)):
        current_time = step * config.DT
        mark_price = price_path[step]

        # Oracle price (slightly smoothed)
        oracle_price = mark_price * (1 + np.random.normal(0, 0.0003))
        state.record_price(mark_price)
        oracle_prices.append(oracle_price)

        # Takers
        for taker in takers:
            if np.random.random() < 0.25:
                side, price, size = taker.get_order(mark_price)
                filled, avg_price = process_order(state, side, price, size, current_time, taker.agent_id)
                if filled > 0:
                    state.position_manager.open_or_update(taker.agent_id, side, filled, avg_price, current_time)


        # === MARKET MAKERS QUOTING ===
        # Market Makers quoting
        for mm in market_makers:
            bid, ask = mm.get_quotes(mark_price)

            # Strategy-specific base sizes (more variation)
            if mm.strategy_type == "aggressive":
                base_size = 20.0 + np.random.uniform(-5, 12)
            elif mm.strategy_type == "passive":
                base_size = 6.0 + np.random.uniform(-2, 5)
            else:
                base_size = 11.0 + np.random.uniform(-4, 8)

            bid_size = base_size
            ask_size = base_size

            # Strong side-aware inventory control
            if mm.inventory > 60:
                bid_size *= 0.25
                ask_size *= 2.2
            elif mm.inventory < -60:
                bid_size *= 2.2
                ask_size *= 0.25

            bid_size = max(2.5, round(bid_size, 1))
            ask_size = max(2.5, round(ask_size, 1))

            # Submit BID
            if bid is not None:
                filled, avg_price = process_order(state, 'buy', bid, bid_size, current_time, mm.agent_id)
                print(f"MM {mm.agent_id} BID {bid:.2f} size {bid_size:.1f} → filled {filled:.2f}")
                if filled > 0:
                    mm.on_trade(filled, 'sell')

            if ask is not None:
                filled, avg_price = process_order(state, 'sell', ask, ask_size, current_time, mm.agent_id)
                print(f"MM {mm.agent_id} ASK {ask:.2f} size {ask_size:.1f} → filled {filled:.2f}")
                if filled > 0:
                    mm.on_trade(filled, 'buy')

        state.position_manager.update_unrealized(mark_price)

        # Funding
        sample_premium(premium_samples, mark_price, oracle_price)
        if int(current_time) % config.FUNDING_INTERVAL == 0 and premium_samples:
            rate = calculate_hourly_funding(premium_samples, config)  # pass config
            funding_history.append(rate)
            state.position_manager.apply_funding(rate)

        # Liquidations
        if step % 20 == 0:
            liquidatable = state.position_manager.get_liquidatable(mark_price, config.MAINTENANCE_MARGIN_RATE)
            for aid in liquidatable:
                size_liq, _ = execute_liquidation(state, aid, mark_price, config)
                liquidation_times.append(step)
                if step < len(liquidation_volumes):
                    liquidation_volumes[step] += size_liq

        # Order Book Metrics
        if step % 100 == 0:
            depth = state.order_book.get_depth(levels=5)
            bid_depth = sum(size for _, size in depth['bids'])
            ask_depth = sum(size for _, size in depth['asks'])
            best_bid = state.order_book.get_best_bid()
            best_ask = state.order_book.get_best_ask()
            spread = (best_ask.price - best_bid.price) if best_bid and best_ask else 0.0
            imbalance = (bid_depth - ask_depth) / (bid_depth + ask_depth + 1e-8)

            order_book_snapshots.append((bid_depth, ask_depth))
            spread_history.append(spread)
            imbalance_history.append(imbalance)

        # PnL & Inventory
        total_pnl = sum(p.realized_pnl + p.unrealized_pnl for p in state.position_manager.positions.values())
        total_pnl_history.append(total_pnl)

        for mm in market_makers:
            mm_pnl_history[mm.agent_id].append(total_pnl)
            inventory_history[mm.agent_id].append(mm.inventory)

    # DEBUG:
    premiums = [m - o for m, o in zip(state.price_history, oracle_prices[:len(state.price_history)])]
    print(f"Avg Premium: {np.mean(premiums):.5f}")
    print(f"Max Premium: {np.max(premiums):.5f}")
    print(f"Min Premium: {np.min(premiums):.5f}")
    print(f"Funding rate range: {min(funding_history):.5f} to {max(funding_history):.5f}")

    # === PLOTS ===
    from visualizations import (
        plot_price_path, plot_funding_rate, plot_market_dashboard, plot_mm_pnl_over_time,
        plot_equity_curve, plot_drawdown, plot_inventory_over_time,
        plot_orderbook_depth, plot_spread_over_time, plot_imbalance,
        plot_sharpe_sortino
    )
    plot_market_dashboard(state, oracle_prices, funding_history, liquidation_times, liquidation_volumes,
                          funding_interval=config.FUNDING_INTERVAL, dt=config.DT)


    # if getattr(config, 'PLOT_PRICE_AND_LIQS', True):
    #     plot_price_path(state, oracle_prices, liquidation_times, liquidation_volumes)
    # if getattr(config, 'PLOT_FUNDING', True) and funding_history:
    #     plot_funding_rate(funding_history)
    if getattr(config, 'PLOT_MM_PNL', True):
        plot_mm_pnl_over_time(mm_pnl_history)
    if getattr(config, 'PLOT_EQUITY_CURVE', True):
        plot_equity_curve(total_pnl_history)
    if getattr(config, 'PLOT_DRAWDOWN', True):
        plot_drawdown(total_pnl_history)
    if getattr(config, 'PLOT_INVENTORY', True):
        plot_inventory_over_time(inventory_history)
    if getattr(config, 'PLOT_ORDERBOOK_DEPTH', True):
        plot_orderbook_depth(order_book_snapshots)
    if getattr(config, 'PLOT_SPREAD', True) and spread_history:
        plot_spread_over_time(spread_history)
    if getattr(config, 'PLOT_IMBALANCE', True) and imbalance_history:
        plot_imbalance(imbalance_history)
    if getattr(config, 'PLOT_SHARPE_SORTINO', True):
        plot_sharpe_sortino(mm_pnl_history)

    print(f"Simulation finished. Final price: {state.price_history[-1]:.2f}")
    return state

if __name__ == '__main__':
    config = Config()
    state = SimulationState.create_initial_state(config)

    run_simulation(config)


