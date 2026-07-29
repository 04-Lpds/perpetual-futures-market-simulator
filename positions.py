# positions.py
"""
Position & PnL Management
"""

from dataclasses import dataclass
from collections import defaultdict



@dataclass
class Position:
    agent_id: int
    side: str
    size: float
    entry_price: float
    entry_time: float
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0

class PositionManager:
    def __init__(self):
        self.positions = {}  # agent_id -> Position

    def open_or_update(self, agent_id: int, side: str, size: float, price: float, timestamp: float):
        if agent_id not in self.positions:
            self.positions[agent_id] = Position(agent_id, side, size, price, timestamp)
        else:
            pos = self.positions[agent_id]
            if pos.side == side:
                total = pos.size * pos.entry_price + size * price
                pos.size += size
                pos.entry_price = total / pos.size
            else:
                # Opposite side - close
                close_size = min(pos.size, size)
                pnl = (price - pos.entry_price) * close_size if pos.side == 'long' else (pos.entry_price - price) * close_size
                pos.realized_pnl += pnl
                pos.size -= close_size
                if pos.size <= 0:
                    del self.positions[agent_id]

    def close_position(self, agent_id: int, price: float):
        """Close the entire position at a given price"""
        if agent_id not in self.positions:
            return
        pos = self.positions[agent_id]
        pnl = (price - pos.entry_price) * pos.size if pos.side == 'long' else (pos.entry_price - price) * pos.size
        pos.realized_pnl += pnl
        del self.positions[agent_id]

    def apply_funding(self, funding_rate: float):
        """Apply hourly funding payments"""
        for pos in self.positions.values():
            payment = funding_rate * pos.size * pos.entry_price
            if pos.side == 'long':
                pos.realized_pnl -= payment
            else:
                pos.realized_pnl += payment

    def update_unrealized(self, mark_price: float):
        for pos in self.positions.values():
            pos.unrealized_pnl = (mark_price - pos.entry_price) * pos.size if pos.side == 'long' else (pos.entry_price - mark_price) * pos.size

    def get_total_pnl(self, agent_id: int) -> float:
        """Total PnL (realized + unrealized) for an agent"""
        if agent_id not in self.positions:
            return 0.0
        pos = self.positions[agent_id]
        return pos.realized_pnl + pos.unrealized_pnl

    def get_liquidatable(self, mark_price: float, mm_rate: float):
        return [aid for aid, pos in self.positions.items() if abs(pos.size * mark_price) > 0 and abs(pos.realized_pnl + pos.unrealized_pnl) / (abs(pos.size * mark_price)) < mm_rate]