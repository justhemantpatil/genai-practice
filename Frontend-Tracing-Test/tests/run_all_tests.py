"""
Test Runner - Executes all test cases sequentially
"""
import subprocess
import sys
import os

def run_test(test_file):
    """Run a single test file"""
    print(f"\n{'#'*70}")
    print(f"# Running: {test_file}")
    print(f"{'#'*70}\n")
    
    result = subprocess.run([sys.executable, test_file], capture_output=False)
    return result.returncode == 0

def main():
    """Run all tests"""
    tests_dir = os.path.dirname(__file__)
    
    test_files = [
        os.path.join(tests_dir, "test_app_dashboard.py"),
        os.path.join(tests_dir, "test_dashboard_network.py"),
        os.path.join(tests_dir, "test_network_async.py"),
        os.path.join(tests_dir, "test_comprehensive.py"),
    ]
    
    print("\n" + "="*70)
    print(" Frontend Tracing - Test Suite Runner")
    print("="*70)
    print(f"\nTotal tests to run: {len(test_files)}\n")
    
    results = {}
    for test_file in test_files:
        test_name = os.path.basename(test_file)
        success = run_test(test_file)
        results[test_name] = success
    
    # Summary
    print("\n" + "="*70)
    print(" Test Summary")
    print("="*70 + "\n")
    
    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed
    
    for test_name, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status:12} - {test_name}")
    
    print(f"\nTotal: {len(results)} | Passed: {passed} | Failed: {failed}")
    print("="*70 + "\n")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
