# Agent-Based Perpetual Futures Market Simulator

A quantitative research framework for simulating perpetual futures markets, market microstructure, and algorithmic trading strategies.

## Overview

This project is an agent-based simulation framework designed to study the dynamics of crypto perpetual futures markets, including order book behavior, liquidity provision, leverage, funding mechanisms, and liquidation events.

The goal is to build a high-fidelity research environment for experimenting with market-making strategies, analyzing execution dynamics, and studying the interaction between market participants, liquidity, and risk.

The framework is inspired by modern crypto perpetual futures venues and is designed for quantitative research rather than production trading.

---

## Motivation

Perpetual futures markets are complex adaptive systems where traders, liquidity providers, funding mechanisms, and leveraged positions interact to determine market outcomes.

This project aims to provide a controlled simulation environment for investigating questions such as:

- How do market-making strategies perform under different market conditions?
- How does inventory risk affect liquidity provision?
- How do funding rates influence trader behavior and market equilibrium?
- How do leverage and volatility contribute to liquidation events?
- How do market mechanics impact execution quality and profitability?

---

## Current Status

This project is an active research prototype. The core simulation framework, exchange mechanics, agent architecture, and risk systems have been implemented and are producing simulated market outputs.

Current development focuses on improving market realism and extending the framework for quantitative strategy research, including:

- Inventory-aware market-making algorithms
- Strategy backtesting and performance evaluation
- Quote optimization and spread modeling
- Market impact and adverse selection analysis
- Calibration and validation of simulated market behavior

The framework is intended as a research environment for studying perpetual futures market dynamics rather than a production trading system.

---

## Architecture

The simulator is built using a modular architecture separating exchange mechanics, market participants, risk systems, and analytics.

```
                    Market Environment
                           |
                           |
        -----------------------------------------
        |                 |                     |
   Order Book          Agents              Risk Engine
        |                 |                     |
 Matching Engine   Market Makers          Liquidations
        |          Takers                  Positions
        |
   Execution
        |
 Metrics & Analysis
```

---

## Core Components

### Exchange Mechanics

### Order Book (`order_book.py`)
- Limit order book representation
- Bid/ask liquidity tracking
- Market depth modeling

### Matching Engine (`matching.py`)
- Order matching logic
- Trade execution
- Market and limit order handling

### Simulation Engine (`simulation.py`)
- Coordinates market evolution
- Manages simulation steps
- Updates market state

---

## Trading Agents

### Market Makers (`market_maker.py`)

Models liquidity providers participating in the order book.

Research applications:
- Spread optimization
- Inventory management
- Liquidity provision strategies

### Takers (`taker.py`)

Models market participants consuming liquidity.

Research applications:
- Order flow dynamics
- Execution behavior
- Market impact analysis

---

## Perpetual Futures Mechanics

### Funding (`funding.py`)

Models perpetual futures funding mechanisms and their effect on market participants.

### Positions (`positions.py`)

Tracks:

- Trader exposure
- Leverage
- Unrealized PnL
- Position states

### Liquidations (`liquidations.py`)

Models forced position closures resulting from insufficient margin.

Research applications:

- Liquidation cascades
- Leverage risk
- Market stress scenarios

---

## Current Research Areas

### Market Making

Investigating:

- Inventory-aware quoting strategies
- Spread optimization
- Liquidity provision under changing volatility conditions
- Trade execution and profitability

### Market Microstructure

Studying:

- Order book dynamics
- Liquidity distribution
- Market participant interactions
- Execution quality

### Risk Modeling

Analyzing:

- Leverage effects
- Liquidation behavior
- Funding dynamics
- Market stress scenarios

---

## Example Outputs

The simulator generates quantitative outputs and visualizations for:

- Funding rate dynamics
- Liquidation events
- Position exposure
- Market participant behavior
- Trading performance metrics
- Simulation statistics

Additional strategy research and optimization experiments are currently under development.

---

## Technical Implementation

Built in Python using a modular architecture designed for quantitative experimentation and reproducible research.

### Technologies

- Python
- NumPy
- Pandas
- SciPy
- Matplotlib

### Project Structure

```
perpetual-futures-market-simulator/

├── agents/
│   ├── market_maker.py
│   └── taker.py
│
├── order_book.py
├── matching.py
├── funding.py
├── liquidations.py
├── positions.py
├── oracle.py
├── price_path.py
├── simulation.py
├── state.py
├── metrics.py
├── visualizations.py
├── config.py
│
├── requirements.txt
└── README.md
```

---

## Future Development

Planned extensions include:

- Advanced market-making strategies
- Parameter optimization
- Statistical strategy evaluation
- Multi-agent market simulations
- More realistic market impact models
- Historical market calibration
- Comparison of different trading approaches

---

## Disclaimer

This project is for research and educational purposes only. It is not intended to represent a production trading system or provide financial advice.