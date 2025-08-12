#!/usr/bin/env python3
"""
Performance testing script for the Whatnot Price Checker
Tests response times and identifies bottlenecks
"""

import asyncio
import aiohttp
import time
import json
import statistics
from typing import List, Dict

class PerformanceTester:
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url
        self.test_products = [
            {"product_name": "Air Jordan 1 Retro High OG Chicago", "size": "10", "condition": "new"},
            {"product_name": "Nike Dunk Low Panda", "size": "9.5", "condition": "new"},
            {"product_name": "Adidas Yeezy Boost 350 V2", "size": "11", "condition": "new"},
            {"product_name": "New Balance 550 White Grey", "size": "10.5", "condition": "new"},
            {"product_name": "Jordan 4 Retro Black Cat", "size": "9", "condition": "new"}
        ]
    
    async def test_single_request(self, session: aiohttp.ClientSession, product: Dict) -> Dict:
        """Test a single price check request"""
        start_time = time.time()
        
        try:
            async with session.post(
                f"{self.base_url}/api/check-price",
                json=product,
                headers={'Content-Type': 'application/json'}
            ) as response:
                result = await response.json()
                end_time = time.time()
                
                return {
                    'product': product['product_name'],
                    'response_time': end_time - start_time,
                    'success': result.get('success', False),
                    'status_code': response.status,
                    'error': result.get('error') if not result.get('success', False) else None
                }
        except Exception as e:
            end_time = time.time()
            return {
                'product': product['product_name'],
                'response_time': end_time - start_time,
                'success': False,
                'status_code': 0,
                'error': str(e)
            }
    
    async def test_concurrent_requests(self, num_concurrent: int = 5) -> List[Dict]:
        """Test multiple concurrent requests"""
        print(f"Testing {num_concurrent} concurrent requests...")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(num_concurrent):
                product = self.test_products[i % len(self.test_products)]
                tasks.append(self.test_single_request(session, product))
            
            results = await asyncio.gather(*tasks)
            return results
    
    async def test_sequential_requests(self, num_requests: int = 10) -> List[Dict]:
        """Test sequential requests to measure baseline performance"""
        print(f"Testing {num_requests} sequential requests...")
        
        results = []
        async with aiohttp.ClientSession() as session:
            for i in range(num_requests):
                product = self.test_products[i % len(self.test_products)]
                result = await self.test_single_request(session, product)
                results.append(result)
                print(f"Request {i+1}: {result['response_time']:.2f}s - {result['product']}")
        
        return results
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze test results and provide performance metrics"""
        successful_results = [r for r in results if r['success']]
        failed_results = [r for r in results if not r['success']]
        
        if not successful_results:
            return {
                'error': 'No successful requests',
                'total_requests': len(results),
                'failed_requests': len(failed_results)
            }
        
        response_times = [r['response_time'] for r in successful_results]
        
        analysis = {
            'total_requests': len(results),
            'successful_requests': len(successful_results),
            'failed_requests': len(failed_results),
            'success_rate': (len(successful_results) / len(results)) * 100,
            'response_times': {
                'min': min(response_times),
                'max': max(response_times),
                'mean': statistics.mean(response_times),
                'median': statistics.median(response_times),
                'std_dev': statistics.stdev(response_times) if len(response_times) > 1 else 0
            },
            'performance_grade': self.grade_performance(response_times),
            'meets_8s_requirement': all(t <= 8.0 for t in response_times),
            'under_5s_percentage': (sum(1 for t in response_times if t <= 5.0) / len(response_times)) * 100,
            'under_3s_percentage': (sum(1 for t in response_times if t <= 3.0) / len(response_times)) * 100
        }
        
        if failed_results:
            analysis['errors'] = [r['error'] for r in failed_results if r['error']]
        
        return analysis
    
    def grade_performance(self, response_times: List[float]) -> str:
        """Grade the performance based on response times"""
        avg_time = statistics.mean(response_times)
        
        if avg_time <= 2.0:
            return 'A+ (Excellent)'
        elif avg_time <= 3.0:
            return 'A (Very Good)'
        elif avg_time <= 5.0:
            return 'B (Good)'
        elif avg_time <= 8.0:
            return 'C (Acceptable)'
        else:
            return 'F (Needs Improvement)'
    
    def print_analysis(self, analysis: Dict):
        """Print formatted analysis results"""
        print("\n" + "="*60)
        print("PERFORMANCE TEST RESULTS")
        print("="*60)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            return
        
        print(f"📊 Total Requests: {analysis['total_requests']}")
        print(f"✅ Successful: {analysis['successful_requests']}")
        print(f"❌ Failed: {analysis['failed_requests']}")
        print(f"📈 Success Rate: {analysis['success_rate']:.1f}%")
        
        print(f"\n⏱️  RESPONSE TIMES:")
        rt = analysis['response_times']
        print(f"   Min: {rt['min']:.2f}s")
        print(f"   Max: {rt['max']:.2f}s")
        print(f"   Mean: {rt['mean']:.2f}s")
        print(f"   Median: {rt['median']:.2f}s")
        print(f"   Std Dev: {rt['std_dev']:.2f}s")
        
        print(f"\n🎯 PERFORMANCE METRICS:")
        print(f"   Grade: {analysis['performance_grade']}")
        print(f"   Meets 8s requirement: {'✅ Yes' if analysis['meets_8s_requirement'] else '❌ No'}")
        print(f"   Under 5s: {analysis['under_5s_percentage']:.1f}%")
        print(f"   Under 3s: {analysis['under_3s_percentage']:.1f}%")
        
        if 'errors' in analysis:
            print(f"\n❌ ERRORS:")
            for error in set(analysis['errors']):
                print(f"   - {error}")
    
    async def run_comprehensive_test(self):
        """Run a comprehensive performance test suite"""
        print("🚀 Starting Comprehensive Performance Test")
        print("="*60)
        
        # Test 1: Sequential requests
        print("\n📋 Test 1: Sequential Performance")
        sequential_results = await self.test_sequential_requests(10)
        sequential_analysis = self.analyze_results(sequential_results)
        self.print_analysis(sequential_analysis)
        
        # Test 2: Concurrent requests
        print("\n📋 Test 2: Concurrent Performance")
        concurrent_results = await self.test_concurrent_requests(5)
        concurrent_analysis = self.analyze_results(concurrent_results)
        self.print_analysis(concurrent_analysis)
        
        # Test 3: Stress test
        print("\n📋 Test 3: Stress Test (10 concurrent)")
        stress_results = await self.test_concurrent_requests(10)
        stress_analysis = self.analyze_results(stress_results)
        self.print_analysis(stress_analysis)
        
        # Overall recommendations
        print("\n💡 RECOMMENDATIONS:")
        avg_time = sequential_analysis['response_times']['mean']
        
        if avg_time <= 3.0:
            print("   ✅ Performance is excellent! System ready for production.")
        elif avg_time <= 5.0:
            print("   ✅ Performance is good. Consider minor optimizations.")
        elif avg_time <= 8.0:
            print("   ⚠️  Performance meets requirements but could be improved.")
            print("   💡 Consider implementing caching or optimizing API calls.")
        else:
            print("   ❌ Performance needs improvement to meet 8-second requirement.")
            print("   💡 Implement caching, connection pooling, and async optimizations.")
        
        return {
            'sequential': sequential_analysis,
            'concurrent': concurrent_analysis,
            'stress': stress_analysis
        }

async def main():
    """Main function to run performance tests"""
    tester = PerformanceTester()
    
    # Check if server is running
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{tester.base_url}/api/health") as response:
                if response.status != 200:
                    print("❌ Server is not responding. Please start the Flask server first.")
                    return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Please start the Flask server first with: python src/main.py")
        return
    
    # Run comprehensive tests
    results = await tester.run_comprehensive_test()
    
    # Save results to file
    with open('/home/ubuntu/whatnot-price-checker/performance_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to: performance_results.json")

if __name__ == "__main__":
    asyncio.run(main())

