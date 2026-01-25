# Test Command Examples

This guide shows how to use `lumpy-log test` with various TAP-compatible testing frameworks across different programming languages.

## Table of Contents

- [Python](#python)
- [JavaScript/Node.js](#javascriptnodejs)
- [Perl](#perl)
- [Ruby](#ruby)
- [PHP](#php)
- [Go](#go)
- [Rust](#rust)
- [Java](#java)
- [C/C++](#cc)
- [General Tips](#general-tips)

---

## Python

### pytest with pytest-tap

**Install:**
```bash
pip install pytest pytest-tap
```

**Bash/Linux/macOS:**
```bash
# Direct pipe
pytest --tap | lumpy-log test

# With verbose output
pytest --tap -v | lumpy-log test

# Save to file first
pytest --tap > test_results.tap
lumpy-log test --input test_results.tap

# Include raw output in report
pytest --tap | lumpy-log test --raw-output

# Custom output folder
pytest --tap | lumpy-log test -o docs/test-logs
```

**Windows cmd.exe:**
```cmd
REM Direct pipe
py -m pytest --tap | lumpy-log test

REM Save to file
py -m pytest --tap > test_results.tap
lumpy-log test --input test_results.tap

REM Include raw output
py -m pytest --tap | lumpy-log test --raw-output
```

**Windows PowerShell:**
```powershell
# Direct pipe
pytest --tap | lumpy-log test

# Save to file
pytest --tap | Out-File -Encoding utf8 test_results.tap
lumpy-log test --input test_results.tap

# Include raw output
pytest --tap | lumpy-log test --raw-output
```

---

## JavaScript/Node.js

### tape

**Install:**
```bash
npm install --save-dev tape
```

**Bash/Linux/macOS:**
```bash
# Direct pipe
node test.js | lumpy-log test

# All test files
tape test/*.js | lumpy-log test

# Save to file
tape test/*.js > test_results.tap
lumpy-log test --input test_results.tap
```

**Windows cmd.exe:**
```cmd
REM Direct pipe
node test.js | lumpy-log test

REM All test files
tape test\*.js | lumpy-log test
```

**Windows PowerShell:**
```powershell
# Direct pipe
node test.js | lumpy-log test

# All test files
tape test\*.js | lumpy-log test
```

### node-tap

**Install:**
```bash
npm install --save-dev tap
```

**Bash/Linux/macOS:**
```bash
# Direct pipe
tap test/*.js | lumpy-log test

# With coverage
tap test/*.js --coverage | lumpy-log test --raw-output

# Save to file
tap test/*.js > test_results.tap
lumpy-log test --input test_results.tap
```

**Windows cmd.exe:**
```cmd
REM Direct pipe
tap test\*.js | lumpy-log test

REM Save to file
tap test\*.js > test_results.tap
lumpy-log test --input test_results.tap
```

**Windows PowerShell:**
```powershell
# Direct pipe
tap test\*.js | lumpy-log test

# With specific tests
tap "test\**\*.test.js" | lumpy-log test
```

### Jest with jest-tap-reporter

**Install:**
```bash
npm install --save-dev jest jest-tap-reporter
```

**Bash/Linux/macOS:**
```bash
# Direct pipe
jest --testResultsProcessor=jest-tap-reporter | lumpy-log test

# Save to file
jest --testResultsProcessor=jest-tap-reporter > test_results.tap
lumpy-log test --input test_results.tap
```

**Windows cmd.exe/PowerShell:**
```cmd
jest --testResultsProcessor=jest-tap-reporter | lumpy-log test
```

---

## Perl

### Test::More (Native TAP)

**Bash/Linux/macOS:**
```bash
# Direct pipe
prove -v t/*.t | lumpy-log test

# All tests recursively
prove -rv t/ | lumpy-log test

# Save to file
prove -v t/*.t > test_results.tap
lumpy-log test --input test_results.tap

# With TAP archive
prove --archive results.tar.gz t/*.t
tar -xzOf results.tar.gz | lumpy-log test
```

**Windows cmd.exe:**
```cmd
REM Direct pipe
prove -v t\*.t | lumpy-log test

REM Save to file
prove -v t\*.t > test_results.tap
lumpy-log test --input test_results.tap
```

**Windows PowerShell:**
```powershell
# Direct pipe
prove -v t\*.t | lumpy-log test

# Recursive
prove -rv t\ | lumpy-log test
```

---

## Ruby

### Minitest with minitest-reporters

**Install:**
```bash
gem install minitest minitest-reporters
```

**Add to test file:**
```ruby
require 'minitest/reporters'
Minitest::Reporters.use! Minitest::Reporters::TapReporter.new
```

**Bash/Linux/macOS:**
```bash
# Direct pipe
ruby test/test_*.rb | lumpy-log test

# Using rake
rake test | lumpy-log test

# Save to file
ruby test/test_*.rb > test_results.tap
lumpy-log test --input test_results.tap
```

**Windows cmd.exe:**
```cmd
REM Direct pipe
ruby test\test_*.rb | lumpy-log test
```

**Windows PowerShell:**
```powershell
# Direct pipe
ruby test\test_*.rb | lumpy-log test
```

---

## PHP

### PHPUnit with TAP Logger

**Install:**
```bash
composer require --dev phpunit/phpunit
```

**Bash/Linux/macOS:**
```bash
# Direct pipe
phpunit --log-tap php://stdout | lumpy-log test

# Save to file
phpunit --log-tap test_results.tap
lumpy-log test --input test_results.tap

# Specific test suite
phpunit --log-tap php://stdout --testsuite unit | lumpy-log test
```

**Windows cmd.exe:**
```cmd
REM Direct pipe
phpunit --log-tap php://stdout | lumpy-log test

REM Save to file
phpunit --log-tap test_results.tap
lumpy-log test --input test_results.tap
```

**Windows PowerShell:**
```powershell
# Direct pipe
phpunit --log-tap php://stdout | lumpy-log test
```

---

## Go

### go test with TAP formatter

**Install:**
```bash
go install github.com/mfridman/tparse@latest
```

**Bash/Linux/macOS:**
```bash
# Using go-tap
go test -v ./... | tparse -format tap | lumpy-log test

# Save to file
go test -v ./... | tparse -format tap > test_results.tap
lumpy-log test --input test_results.tap

# Specific package
go test -v ./pkg/... | tparse -format tap | lumpy-log test
```

**Windows cmd.exe:**
```cmd
REM Direct pipe
go test -v .\... | tparse -format tap | lumpy-log test
```

**Windows PowerShell:**
```powershell
# Direct pipe
go test -v .\... | tparse -format tap | lumpy-log test
```

---

## Rust

### cargo test with TAP formatter

**Install TAP formatter:**
```bash
cargo install cargo-tap
```

**Bash/Linux/macOS:**
```bash
# Direct pipe (requires custom runner)
cargo test -- -Z unstable-options --format json | json-to-tap | lumpy-log test

# Or using cargo-nextest with TAP
cargo install cargo-nextest
cargo nextest run --message-format json | nextest-to-tap | lumpy-log test

# Save to file
cargo test 2>&1 | lumpy-log test --input -
```

**Windows cmd.exe:**
```cmd
REM Using cargo test
cargo test 2>&1 | lumpy-log test
```

**Windows PowerShell:**
```powershell
# Direct pipe
cargo test 2>&1 | lumpy-log test
```

**Note:** Rust's built-in test framework doesn't natively output TAP. Consider using a TAP adapter or custom test harness.

---

## Java

### JUnit with TAP Reporter

**Add dependency (Maven):**
```xml
<dependency>
    <groupId>org.tap4j</groupId>
    <artifactId>tap4j</artifactId>
    <version>4.4.2</version>
</dependency>
```

**Bash/Linux/macOS:**
```bash
# Using Maven with TAP plugin
mvn test -Dtap.output=true | grep -A 99999 "^TAP" | lumpy-log test

# Save to file
mvn test -Dtap.output=true > test_results.tap
lumpy-log test --input test_results.tap

# Using Gradle with custom TAP reporter
./gradlew test --console=plain | lumpy-log test
```

**Windows cmd.exe:**
```cmd
REM Using Maven
mvn test -Dtap.output=true | findstr /R "^[0-9]" | lumpy-log test

REM Save to file
mvn test > test_results.tap
lumpy-log test --input test_results.tap
```

**Windows PowerShell:**
```powershell
# Using Maven
mvn test -Dtap.output=true | Select-String "^[0-9]|^ok|^not ok" | lumpy-log test
```

---

## C/C++

### libtap

**Install:**
```bash
# Ubuntu/Debian
sudo apt-get install libtap-dev

# macOS
brew install libtap
```

**Bash/Linux/macOS:**
```bash
# Run compiled test binary
./test_suite | lumpy-log test

# Multiple test binaries
for test in tests/*; do $test; done | lumpy-log test

# Save to file
./test_suite > test_results.tap
lumpy-log test --input test_results.tap
```

**Windows (MinGW/Cygwin):**
```bash
# Run test executable
./test_suite.exe | lumpy-log test

# Save to file
./test_suite.exe > test_results.tap
lumpy-log test --input test_results.tap
```

### Google Test with TAP Listener

**Bash/Linux/macOS:**
```bash
# Run with TAP output
./test_binary --gtest_output=tap | lumpy-log test

# Save to file
./test_binary --gtest_output=tap:test_results.tap
lumpy-log test --input test_results.tap
```

---

## General Tips

### Combining Multiple Test Runs

**Bash/Linux/macOS:**
```bash
# Run all tests and combine output
{
  pytest --tap
  node test.js
  prove -v t/*.t
} | lumpy-log test

# Run sequentially and save each
pytest --tap | lumpy-log test
npm test | lumpy-log test
```

### Continuous Integration

**GitHub Actions:**
```yaml
- name: Run tests and generate logs
  run: |
    pytest --tap | lumpy-log test -o test-logs
    
- name: Upload test logs
  uses: actions/upload-artifact@v3
  with:
    name: test-logs
    path: test-logs/
```

**GitLab CI:**
```yaml
test:
  script:
    - pytest --tap | lumpy-log test -o test-logs
  artifacts:
    paths:
      - test-logs/
```

### Filtering Test Output

**Bash/Linux/macOS:**
```bash
# Remove ANSI color codes before piping
pytest --tap --color=no | lumpy-log test

# Filter out warnings
pytest --tap 2>&1 | grep -v "DeprecationWarning" | lumpy-log test
```

**Windows PowerShell:**
```powershell
# Filter and pipe
pytest --tap --color=no | lumpy-log test
```

### Debugging Failed Tests

```bash
# Include raw output to see full details
pytest --tap -vv | lumpy-log test --raw-output

# Save both TAP and raw output
pytest --tap | tee test_results.tap | lumpy-log test --raw-output
```

---

## Common Issues

### "No input provided" Error

Make sure your test framework is actually outputting to stdout:

```bash
# Bad - redirects to file descriptor
pytest --tap 2>&1 > output.log | lumpy-log test

# Good - outputs to stdout
pytest --tap | lumpy-log test
```

### TAP Format Not Detected

Ensure your test framework is configured for TAP output:

```bash
# Verify TAP output first
pytest --tap | head -n 20

# Should see lines like:
# 1..45
# ok 1 test_something
# ok 2 test_another
```

### Windows Encoding Issues

Use UTF-8 encoding:

```powershell
# PowerShell
$OutputEncoding = [System.Text.Encoding]::UTF8
pytest --tap | lumpy-log test
```

---

## Need Help?

- Check that your test framework supports TAP output
- Verify TAP format by viewing output: `pytest --tap | head`
- Use `--verbose` flag for debugging: `lumpy-log test --verbose`
- Include raw output if needed: `lumpy-log test --raw-output`

For more information, see:
- [README.md](README.md) - Main documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [TAP Specification](https://testanything.org/)
