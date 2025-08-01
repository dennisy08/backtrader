#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2023 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
//@version=5
strategy(title='[SMT] Buy & Sell Renko Based - Cleaned', shorttitle='[SMT] B&S Renko', overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// INPUT
renkoATRLength = input.int(10, title='Renko ATR Length')

// RENKO CHART (ATR BRICKS)
renkoChart = ticker.renko(syminfo.tickerid, "ATR", renkoATRLength)

// GET RENKO PRICES (with lookahead OFF)
renkoClose = request.security(renkoChart, timeframe.period, close, lookahead=barmerge.lookahead_off)
renkoOpen  = request.security(renkoChart, timeframe.period, open,  lookahead=barmerge.lookahead_off)

// COLOR
renkoColor = renkoClose < renkoOpen ? color.red : color.green

// PLOT RENKO OPEN
plot(renkoOpen, title="Renko Open", style=plot.style_line, linewidth=2, color=renkoColor)

// SIGNALS
buySignal  = ta.crossunder(renkoOpen, renkoClose)
sellSignal = ta.crossover(renkoOpen, renkoClose)

// STRATEGY ENTRIES (no delay)
if buySignal
    strategy.entry("Long", strategy.long)

if sellSignal
    strategy.entry("Short", strategy.short)

// PLOT SHAPES
plotshape(buySignal, title="Buy", location=location.belowbar, color=color.green, style=shape.labelup, text="Buy", textcolor=color.white)
plotshape(sellSignal, title="Sell", location=location.abovebar, color=color.red, style=shape.labeldown, text="Sell", textcolor=color.white)

