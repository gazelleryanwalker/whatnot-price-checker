from flask import Blueprint, jsonify, request
import asyncio
import aiohttp
import time
import re
from typing import Dict, List, Optional, Tuple

price_checker_bp = Blueprint('price_checker', __name__)

class PriceChecker:
    def __init__(self):
        self.stockx_api_key = None  # Will be set via environment or config
        self.kickscrew_api_key = None  # Will be set via environment or config
        
    async def fetch_stockx_price(self, session: aiohttp.ClientSession, product_name: str, size: str) -> Dict:
        """Fetch price from StockX using RapidAPI service"""
        try:
            # For demo purposes, we'll simulate the API call
            # In production, you would use the actual RapidAPI endpoint
            headers = {
                'X-RapidAPI-Key': self.stockx_api_key or 'demo_key',
                'X-RapidAPI-Host': 'stockx-pricing-data-and-market-analytics.p.rapidapi.com'
            }
            
            # Simulate API response time
            await asyncio.sleep(0.5)
            
            # Mock response for demo
            return {
                'platform': 'stockx',
                'lowest_ask': 450,
                'available': True,
                'fees': 42.75,  # 9.5% fee
                'response_time': 0.5
            }
            
        except Exception as e:
            return {
                'platform': 'stockx',
                'error': str(e),
                'available': False
            }
    
    async def fetch_goat_price(self, session: aiohttp.ClientSession, product_name: str, size: str) -> Dict:
        """Fetch price from GOAT using mobile API endpoints"""
        try:
            headers = {
                'user-agent': 'GOAT/19 CFNetwork/1410.0.3 Darwin/22.6.0',
                'x-emb-id': '7E2DEE62833C40A0B733085027D1A5BC',
                'accept': 'application/json'
            }
            
            # Simulate API response time
            await asyncio.sleep(0.7)
            
            # Mock response for demo
            return {
                'platform': 'goat',
                'lowest_ask': 465,
                'available': True,
                'fees': 44.18,  # 9.5% fee
                'response_time': 0.7
            }
            
        except Exception as e:
            return {
                'platform': 'goat',
                'error': str(e),
                'available': False
            }
    
    async def fetch_kickscrew_price(self, session: aiohttp.ClientSession, product_name: str, size: str) -> Dict:
        """Fetch price from KicksCrew using RapidAPI service"""
        try:
            headers = {
                'X-RapidAPI-Key': self.kickscrew_api_key or 'demo_key',
                'X-RapidAPI-Host': 'kickscrew-sneakers-data.p.rapidapi.com'
            }
            
            # Simulate API response time
            await asyncio.sleep(0.3)
            
            # Mock response for demo
            return {
                'platform': 'kickscrew',
                'lowest_ask': 440,
                'available': True,
                'fees': 35.20,  # 8% fee
                'response_time': 0.3
            }
            
        except Exception as e:
            return {
                'platform': 'kickscrew',
                'error': str(e),
                'available': False
            }
    
    def parse_product_input(self, product_input: str) -> Tuple[str, str, str]:
        """Parse product input to extract brand, model, and other details"""
        # Simple parsing logic - can be enhanced with ML/NLP
        product_input = product_input.strip().lower()
        
        # Extract common brands
        brands = ['nike', 'adidas', 'jordan', 'yeezy', 'new balance', 'puma', 'vans', 'converse']
        brand = 'unknown'
        for b in brands:
            if b in product_input:
                brand = b
                break
        
        # Extract model (simplified)
        model = product_input.replace(brand, '').strip()
        
        return brand, model, product_input
    
    def calculate_margins(self, prices: List[Dict], target_multipliers: List[float] = [1.5, 2.0]) -> Dict:
        """Calculate margin recommendations based on current prices"""
        available_prices = [p for p in prices if p.get('available', False)]
        
        if not available_prices:
            return {'error': 'No prices available'}
        
        # Find best price (lowest after fees)
        best_price_data = min(available_prices, key=lambda x: x.get('lowest_ask', float('inf')) + x.get('fees', 0))
        best_price = best_price_data.get('lowest_ask', 0)
        best_fees = best_price_data.get('fees', 0)
        net_selling_price = best_price - best_fees
        
        recommendations = {
            'best_platform': best_price_data.get('platform'),
            'best_price': best_price,
            'best_fees': best_fees,
            'net_selling_price': net_selling_price
        }
        
        for multiplier in target_multipliers:
            # Calculate max bid price for target ROI
            # If we want multiplier return, we need: net_selling_price = max_bid * multiplier
            # So: max_bid = net_selling_price / multiplier
            max_bid = net_selling_price / multiplier
            expected_profit = net_selling_price - max_bid
            roi_percentage = ((net_selling_price - max_bid) / max_bid) * 100 if max_bid > 0 else 0
            
            multiplier_str = str(multiplier).replace('.', '_')
            recommendations[f'max_bid_{multiplier_str}x'] = round(max_bid, 2)
            recommendations[f'expected_profit_{multiplier_str}x'] = round(expected_profit, 2)
            recommendations[f'roi_{multiplier_str}x'] = round(roi_percentage, 2)
        
        return recommendations
    
    async def check_prices(self, product_name: str, size: str, condition: str = 'new') -> Dict:
        """Main function to check prices across all platforms"""
        start_time = time.time()
        
        # Parse product input
        brand, model, parsed_name = self.parse_product_input(product_name)
        
        async with aiohttp.ClientSession() as session:
            # Fetch prices from all platforms concurrently
            tasks = [
                self.fetch_stockx_price(session, product_name, size),
                self.fetch_goat_price(session, product_name, size),
                self.fetch_kickscrew_price(session, product_name, size)
            ]
            
            prices = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions and format results
            valid_prices = []
            for price in prices:
                if isinstance(price, dict) and not isinstance(price, Exception):
                    valid_prices.append(price)
        
        # Calculate recommendations
        recommendations = self.calculate_margins(valid_prices)
        
        total_time = round(time.time() - start_time, 2)
        
        return {
            'success': True,
            'response_time': f"{total_time}s",
            'product': {
                'name': product_name,
                'brand': brand,
                'model': model,
                'size': size,
                'condition': condition
            },
            'prices': {price['platform']: price for price in valid_prices},
            'recommendations': recommendations,
            'timestamp': int(time.time())
        }

# Initialize price checker
price_checker = PriceChecker()

@price_checker_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'whatnot-price-checker',
        'timestamp': int(time.time())
    })

@price_checker_bp.route('/check-price', methods=['POST'])
def check_price():
    """API endpoint to check prices across platforms"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        product_name = data.get('product_name', '').strip()
        size = data.get('size', '').strip()
        condition = data.get('condition', 'new').strip()
        
        if not product_name:
            return jsonify({'error': 'Product name is required'}), 400
        
        if not size:
            return jsonify({'error': 'Size is required'}), 400
        
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                price_checker.check_prices(product_name, size, condition)
            )
        finally:
            loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@price_checker_bp.route('/platforms', methods=['GET'])
def get_platforms():
    """Get supported platforms"""
    return jsonify({
        'platforms': [
            {
                'name': 'StockX',
                'id': 'stockx',
                'fee_percentage': 9.5,
                'status': 'active'
            },
            {
                'name': 'GOAT',
                'id': 'goat',
                'fee_percentage': 9.5,
                'status': 'active'
            },
            {
                'name': 'KicksCrew',
                'id': 'kickscrew',
                'fee_percentage': 8.0,
                'status': 'active'
            }
        ]
    })

