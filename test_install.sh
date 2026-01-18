#!/bin/bash
# Test script for lumpy-log package

echo "=== Testing Lumpy Log Package ==="
echo ""

# Step 1: Install the package in development mode
echo "Step 1: Installing package in development mode..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "❌ Installation failed"
    exit 1
fi
echo "✅ Installation successful"
echo ""

# Step 2: Test CLI command
echo "Step 2: Testing CLI command..."
lumpy-log --help
if [ $? -ne 0 ]; then
    echo "❌ CLI command failed"
    exit 1
fi
echo "✅ CLI command works"
echo ""

# Step 3: Test as module
echo "Step 3: Testing as Python module..."
python -m lumpy_log --help
if [ $? -ne 0 ]; then
    echo "❌ Module execution failed"
    exit 1
fi
echo "✅ Module execution works"
echo ""

# Step 4: Test with current repository
echo "Step 4: Testing with current repository (dry run)..."
lumpy-log -i . -o test_output --dryrun --verbose
if [ $? -ne 0 ]; then
    echo "❌ Execution test failed"
    exit 1
fi
echo "✅ Execution test successful"
echo ""

echo "=== All tests passed! ==="
