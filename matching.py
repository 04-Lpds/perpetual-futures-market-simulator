def process_order(state, side: str, price: float, size: float,
                  timestamp: float, agent_id: int = None) -> tuple:
    """
    Process a new order.
    Returns (filled_size, average_fill_price)
    """
    if size <= 0:
        return 0.0, 0.0

    filled = 0.0
    total_cost = 0.0
    remaining = size

    while remaining > 0:
        if side == 'buy':
            best = state.order_book.get_best_ask()
            if not best or best.price > price:
                break
        else:
            best = state.order_book.get_best_bid()
            if not best or best.price < price:
                break

        fill_size = min(remaining, best.size)

        # Record trade
        trade = {
            'maker_id': best.order_id,
            'taker_id': agent_id,
            'price': best.price,
            'size': fill_size,
            'timestamp': timestamp
        }
        if not hasattr(state, 'trades'):
            state.trades = []
        state.trades.append(trade)

        filled += fill_size
        total_cost += fill_size * best.price
        remaining -= fill_size

        best.size -= fill_size
        if best.size <= 0:
            state.order_book.cancel_order(best.order_id)

    if remaining > 0:
        state.order_book.add_order(side, price, remaining, timestamp, agent_id)

    avg_price = total_cost / filled if filled > 0 else 0.0
    return filled, avg_price