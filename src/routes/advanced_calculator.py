from flask import Blueprint, jsonify, request
from typing import Dict, List, Optional
import time

advanced_calculator_bp = Blueprint('advanced_calculator', __name__)

class AdvancedMarginCalculator:
    def __init__(self):
        self.platform_fees = {
            'stockx': 0.095,  # 9.5%
            'goat': 0.095,    # 9.5%
            'kickscrew': 0.08  # 8%
        }
        
        self.shipping_costs = {
            'stockx': 15.0,
            'goat': 15.0,
            'kickscrew': 20.0  # International shipping
        }
    
    def calculate_detailed_margins(self, prices: List[Dict], custom_targets: List[float] = None) -> Dict:
        """Calculate detailed margin analysis with custom ROI targets"""
        if custom_targets is None:
            custom_targets = [1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
        
        available_prices = [p for p in prices if p.get('available', False)]
        
        if not available_prices:
            return {'error': 'No prices available'}
        
        # Calculate net selling prices for each platform
        platform_analysis = {}
        for price_data in available_prices:
            platform = price_data['platform']
            ask_price = price_data.get('lowest_ask', 0)
            fees = price_data.get('fees', 0)
            shipping = self.shipping_costs.get(platform, 15.0)
            
            net_price = ask_price - fees - shipping
            
            platform_analysis[platform] = {
                'ask_price': ask_price,
                'fees': fees,
                'shipping': shipping,
                'net_selling_price': net_price,
                'total_costs': fees + shipping,
                'profit_margin_percentage': ((net_price / ask_price) * 100) if ask_price > 0 else 0
            }
        
        # Find best platform (highest net selling price)
        best_platform = max(platform_analysis.keys(), 
                          key=lambda x: platform_analysis[x]['net_selling_price'])
        best_net_price = platform_analysis[best_platform]['net_selling_price']
        
        # Calculate bidding recommendations for each target
        bidding_recommendations = []
        for target in custom_targets:
            max_bid = best_net_price / target
            expected_profit = best_net_price - max_bid
            roi_percentage = ((best_net_price - max_bid) / max_bid) * 100 if max_bid > 0 else 0
            
            bidding_recommendations.append({
                'target_multiplier': target,
                'max_bid': round(max_bid, 2),
                'expected_profit': round(expected_profit, 2),
                'roi_percentage': round(roi_percentage, 2),
                'break_even_bid': round(best_net_price, 2)
            })
        
        # Risk analysis
        risk_analysis = self.calculate_risk_analysis(platform_analysis, best_net_price)
        
        # Market comparison
        market_comparison = self.calculate_market_comparison(platform_analysis)
        
        return {
            'platform_analysis': platform_analysis,
            'best_platform': best_platform,
            'best_net_price': best_net_price,
            'bidding_recommendations': bidding_recommendations,
            'risk_analysis': risk_analysis,
            'market_comparison': market_comparison,
            'timestamp': int(time.time())
        }
    
    def calculate_risk_analysis(self, platform_analysis: Dict, best_net_price: float) -> Dict:
        """Calculate risk factors for the investment"""
        platforms = list(platform_analysis.keys())
        net_prices = [platform_analysis[p]['net_selling_price'] for p in platforms]
        
        if len(net_prices) < 2:
            return {'error': 'Insufficient data for risk analysis'}
        
        # Price volatility (standard deviation)
        mean_price = sum(net_prices) / len(net_prices)
        variance = sum((price - mean_price) ** 2 for price in net_prices) / len(net_prices)
        std_deviation = variance ** 0.5
        
        # Risk metrics
        price_spread = max(net_prices) - min(net_prices)
        price_spread_percentage = (price_spread / mean_price) * 100 if mean_price > 0 else 0
        
        # Risk level assessment
        if price_spread_percentage < 5:
            risk_level = 'Low'
        elif price_spread_percentage < 15:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        return {
            'price_spread': round(price_spread, 2),
            'price_spread_percentage': round(price_spread_percentage, 2),
            'volatility': round(std_deviation, 2),
            'risk_level': risk_level,
            'confidence_score': max(0, 100 - price_spread_percentage)
        }
    
    def calculate_market_comparison(self, platform_analysis: Dict) -> Dict:
        """Compare prices across platforms"""
        platforms = list(platform_analysis.keys())
        
        # Sort platforms by net selling price
        sorted_platforms = sorted(platforms, 
                                key=lambda x: platform_analysis[x]['net_selling_price'], 
                                reverse=True)
        
        best_platform = sorted_platforms[0]
        worst_platform = sorted_platforms[-1]
        
        best_price = platform_analysis[best_platform]['net_selling_price']
        worst_price = platform_analysis[worst_platform]['net_selling_price']
        
        price_advantage = best_price - worst_price
        price_advantage_percentage = (price_advantage / worst_price) * 100 if worst_price > 0 else 0
        
        return {
            'platform_ranking': sorted_platforms,
            'best_platform': best_platform,
            'worst_platform': worst_platform,
            'price_advantage': round(price_advantage, 2),
            'price_advantage_percentage': round(price_advantage_percentage, 2),
            'recommendation': f"Sell on {best_platform} for ${price_advantage:.2f} more profit"
        }
    
    def calculate_auction_strategy(self, net_selling_price: float, auction_time_remaining: int = 10) -> Dict:
        """Calculate bidding strategy based on auction dynamics"""
        
        # Conservative, moderate, and aggressive strategies
        strategies = {
            'conservative': {
                'target_multiplier': 2.5,
                'description': 'Low risk, high profit margin',
                'max_bid_percentage': 0.4  # 40% of net selling price
            },
            'moderate': {
                'target_multiplier': 2.0,
                'description': 'Balanced risk and profit',
                'max_bid_percentage': 0.5  # 50% of net selling price
            },
            'aggressive': {
                'target_multiplier': 1.5,
                'description': 'Higher risk, faster turnover',
                'max_bid_percentage': 0.67  # 67% of net selling price
            }
        }
        
        strategy_recommendations = {}
        for strategy_name, strategy in strategies.items():
            max_bid = net_selling_price / strategy['target_multiplier']
            expected_profit = net_selling_price - max_bid
            
            strategy_recommendations[strategy_name] = {
                'max_bid': round(max_bid, 2),
                'expected_profit': round(expected_profit, 2),
                'target_multiplier': strategy['target_multiplier'],
                'description': strategy['description'],
                'success_probability': self.estimate_success_probability(strategy['target_multiplier'])
            }
        
        # Time-based recommendations
        if auction_time_remaining <= 5:
            recommended_strategy = 'aggressive'
            urgency_note = "Limited time - consider aggressive bidding"
        elif auction_time_remaining <= 15:
            recommended_strategy = 'moderate'
            urgency_note = "Moderate time remaining - balanced approach recommended"
        else:
            recommended_strategy = 'conservative'
            urgency_note = "Plenty of time - can afford to be conservative"
        
        return {
            'strategies': strategy_recommendations,
            'recommended_strategy': recommended_strategy,
            'urgency_note': urgency_note,
            'auction_time_remaining': auction_time_remaining
        }
    
    def estimate_success_probability(self, target_multiplier: float) -> float:
        """Estimate probability of successful resale based on target multiplier"""
        # Simple heuristic - higher multipliers have lower success probability
        if target_multiplier >= 3.0:
            return 60.0
        elif target_multiplier >= 2.5:
            return 75.0
        elif target_multiplier >= 2.0:
            return 85.0
        elif target_multiplier >= 1.5:
            return 95.0
        else:
            return 98.0

# Initialize calculator
advanced_calculator = AdvancedMarginCalculator()

@advanced_calculator_bp.route('/advanced-analysis', methods=['POST'])
def advanced_analysis():
    """Advanced margin analysis endpoint"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        prices = data.get('prices', [])
        custom_targets = data.get('custom_targets')
        auction_time = data.get('auction_time_remaining', 10)
        
        if not prices:
            return jsonify({'error': 'Price data is required'}), 400
        
        # Convert prices to expected format
        price_list = []
        for platform, price_data in prices.items():
            price_list.append({
                'platform': platform,
                'lowest_ask': price_data.get('lowest_ask', 0),
                'fees': price_data.get('fees', 0),
                'available': price_data.get('available', True)
            })
        
        # Calculate detailed analysis
        analysis = advanced_calculator.calculate_detailed_margins(price_list, custom_targets)
        
        # Add auction strategy
        if 'best_net_price' in analysis:
            auction_strategy = advanced_calculator.calculate_auction_strategy(
                analysis['best_net_price'], auction_time
            )
            analysis['auction_strategy'] = auction_strategy
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@advanced_calculator_bp.route('/quick-bid-calc', methods=['POST'])
def quick_bid_calculator():
    """Quick bid calculator for live auctions"""
    try:
        data = request.json
        
        selling_price = data.get('selling_price', 0)
        target_multiplier = data.get('target_multiplier', 2.0)
        platform_fees = data.get('platform_fees', 0.095)
        shipping_cost = data.get('shipping_cost', 15.0)
        
        if selling_price <= 0:
            return jsonify({'error': 'Valid selling price is required'}), 400
        
        # Calculate net selling price
        fees = selling_price * platform_fees
        net_selling_price = selling_price - fees - shipping_cost
        
        # Calculate max bid
        max_bid = net_selling_price / target_multiplier
        expected_profit = net_selling_price - max_bid
        roi_percentage = ((net_selling_price - max_bid) / max_bid) * 100 if max_bid > 0 else 0
        
        return jsonify({
            'success': True,
            'selling_price': selling_price,
            'fees': round(fees, 2),
            'shipping_cost': shipping_cost,
            'net_selling_price': round(net_selling_price, 2),
            'max_bid': round(max_bid, 2),
            'expected_profit': round(expected_profit, 2),
            'roi_percentage': round(roi_percentage, 2),
            'target_multiplier': target_multiplier
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

