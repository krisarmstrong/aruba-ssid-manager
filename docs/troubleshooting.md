# Troubleshooting Guide

## Common Issues and Solutions

### SSH Connection Issues

#### Issue: "Connection refused" or "Cannot connect to host"

**Symptoms:**
```
ERROR - pexpect.exceptions.ExceptionPexpect: ... Connection refused
```

**Root Causes:**
1. Aruba controller unreachable on network
2. SSH service not running on controller
3. SSH port not accessible (firewall blocking)
4. Incorrect IP address

**Solutions:**

1. **Verify Network Connectivity**
   ```bash
   ping <CONTROLLER_IP>
   ```
   If ping fails, check network connectivity and firewall rules.

2. **Verify SSH Service**
   ```bash
   # Try manual SSH connection
   ssh admin@<CONTROLLER_IP>
   ```
   If connection fails here, SSH may not be enabled on controller.

3. **Check Firewall Rules**
   ```bash
   # From your machine, check if port 22 is accessible
   nc -zv <CONTROLLER_IP> 22
   ```
   If it fails, check firewall rules on both client and network.

4. **Verify IP Address**
   ```bash
   # Confirm you have the correct IP
   # Check controller's web interface or management interface
   ```

5. **Check SSH Port**
   If SSH is on non-standard port (not 22):
   - Edit the script to specify custom port in SSH spawn command
   - Or use SSH config file: `~/.ssh/config`

---

#### Issue: "Authentication failed" or "Permission denied"

**Symptoms:**
```
ERROR - pexpect.exceptions.ExceptionPexpect: ... Permission denied
```

**Root Causes:**
1. Incorrect username or password
2. User account doesn't exist on controller
3. User doesn't have SSH access privileges
4. Password contains special characters causing parsing issues

**Solutions:**

1. **Verify Credentials Manually**
   ```bash
   ssh admin@<CONTROLLER_IP>
   # Test login with same credentials
   ```

2. **Confirm User Privileges**
   - Log into controller via web interface
   - Verify user account exists and has CLI access rights
   - Check user role has configuration privileges

3. **Handle Special Characters in Password**
   If password contains special characters:
   ```bash
   # Use interactive mode (more secure)
   aruba-ssid-manager --interactive

   # Or properly escape in script
   PASSWORD='my$pass!word'
   aruba-ssid-manager --password "$PASSWORD" ...
   ```

4. **Check SSH Key-Based Auth** (if using keys)
   ```bash
   ssh-keyscan -t rsa <CONTROLLER_IP> >> ~/.ssh/known_hosts
   ssh -i ~/.ssh/id_rsa admin@<CONTROLLER_IP>
   ```

---

### Command Execution Issues

#### Issue: "Timeout waiting for command"

**Symptoms:**
```
ERROR - pexpect.exceptions.TIMEOUT: Timeout exceeded in read_nonblocking()
```

**Root Causes:**
1. Command prompt not responding (default timeout: 30 seconds)
2. SSID/VLAN already exists causing different prompt behavior
3. Controller CPU overloaded
4. Network latency/congestion

**Solutions:**

1. **Check Controller Status**
   ```bash
   # SSH to controller and check
   ssh admin@<CONTROLLER_IP>
   show system
   # Check CPU and memory utilization
   ```

2. **Verify Configuration Doesn't Exist**
   ```bash
   show wlan ssid-profile <SSID_NAME>
   # If it exists, either modify or delete it first
   ```

3. **Test Commands Manually**
   ```bash
   ssh admin@<CONTROLLER_IP>
   configure terminal
   wlan ssid-profile TEST-SSID
   ssid-name TEST-SSID
   # Check if each command completes quickly
   ```

4. **Check Network Latency**
   ```bash
   ping -c 10 <CONTROLLER_IP>
   # High latency may cause timeout. If consistently > 1s, investigate network
   ```

5. **Increase Timeout (Code Modification)**
   Edit `aruba-ssid-manager`, line 99:
   ```python
   session = pexpect.spawn(..., timeout=60)  # Increase from 30 to 60
   ```

---

#### Issue: "Command failed" or "Syntax error"

**Symptoms:**
```
ERROR - Failed to execute command or received unexpected prompt
```

**Root Causes:**
1. SSID name contains invalid characters
2. VLAN ID out of valid range (1-4094)
3. WLAN profile doesn't exist
4. Command sequence incorrect for controller model

**Solutions:**

1. **Validate SSID Name**
   - Must be 1-32 characters
   - Can contain letters, numbers, hyphens, underscores
   - Cannot start with hyphen
   - Test valid SSID: `MyNetwork_2024`

2. **Validate VLAN ID**
   - Range: 1-4094 (0 and 4095 reserved)
   - Example valid: `10`, `100`, `2000`

3. **Verify WLAN Profile Exists**
   ```bash
   ssh admin@<CONTROLLER_IP>
   show wlan profile
   # Verify the profile name matches exactly
   ```

4. **Check Controller Model and Firmware**
   ```bash
   ssh admin@<CONTROLLER_IP>
   show system
   # Some older models may use different syntax
   ```

5. **Test Commands in Interactive SSH**
   ```bash
   ssh admin@<CONTROLLER_IP>
   configure terminal
   wlan ssid-profile <YOUR_SSID>
   ssid-name <YOUR_SSID>
   vlan 10
   exit
   # Verify each step works interactively
   ```

---

### Logging and Debug Issues

#### Issue: No log output or log file not created

**Symptoms:**
- No messages printed to console
- `--logfile` parameter doesn't create file

**Root Causes:**
1. Log file path doesn't exist or not writable
2. Logging not configured properly
3. Verbose flag not enabled

**Solutions:**

1. **Verify Log Directory Exists**
   ```bash
   mkdir -p /var/log/aruba
   chmod 755 /var/log/aruba
   ```

2. **Test with Verbose Flag**
   ```bash
   aruba-ssid-manager --interactive --verbose
   ```

3. **Write to Current Directory First**
   ```bash
   aruba-ssid-manager --interactive --verbose --logfile ./aruba_config.log
   ```

4. **Check File Permissions**
   ```bash
   ls -la /var/log/aruba_config.log
   # Should have owner as current user or 'aruba' service user
   ```

5. **Enable Debug Output**
   Review this code addition to main module if needed:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

---

### Interactive Mode Issues

#### Issue: Input prompts not appearing or appearing incorrectly

**Symptoms:**
- Prompts don't show up
- Input doesn't echo
- Script seems to hang

**Root Causes:**
1. Terminal not properly configured
2. Buffering issues
3. Script not reaching interactive input

**Solutions:**

1. **Use Unbuffered Python**
   ```bash
   python -m aruba_ssid_manager --interactive
   ```

2. **Clear Terminal**
   ```bash
   clear
   aruba-ssid-manager --interactive
   ```

3. **Test with Verbose Output**
   ```bash
   aruba-ssid-manager --interactive --verbose
   ```

4. **Check Arguments Parsing**
   If some arguments provided, script might not go interactive:
   ```bash
   # This won't be interactive (all args provided)
   aruba-ssid-manager --host 10.0.0.1 --username admin

   # This WILL be interactive (missing args)
   aruba-ssid-manager --host 10.0.0.1
   ```

---

### SSID Configuration Issues

#### Issue: SSID created but not visible or not working

**Symptoms:**
- Script completes successfully
- SSID doesn't appear in wireless networks
- Devices can't connect to SSID

**Root Causes:**
1. SSID successfully created but not enabled
2. WLAN profile not active
3. Controller radio disabled
4. VLAN not properly configured on controller

**Solutions:**

1. **Verify SSID Created**
   ```bash
   ssh admin@<CONTROLLER_IP>
   show wlan ssid-profile <SSID_NAME>
   ```

2. **Check WLAN Profile Association**
   ```bash
   show wlan profile <PROFILE_NAME>
   # Verify SSID is assigned to profile
   ```

3. **Enable SSID If Disabled**
   ```bash
   configure terminal
   wlan ssid-profile <SSID_NAME>
   enable
   exit
   write memory
   ```

4. **Verify Radio Status**
   ```bash
   show wlan radio
   # Confirm radios are enabled (2.4GHz and/or 5GHz)
   ```

5. **Check VLAN Configuration**
   ```bash
   show vlan <VLAN_ID>
   # Verify VLAN exists and is not disabled
   ```

---

#### Issue: Hidden SSID not working

**Symptoms:**
- SSID shows as hidden but appears in networks list
- Can't connect to hidden SSID

**Root Causes:**
1. Hide SSID command failed silently
2. Not all APs broadcasting the setting
3. Client/AP caching old broadcast settings

**Solutions:**

1. **Verify Hide Setting**
   ```bash
   ssh admin@<CONTROLLER_IP>
   show wlan ssid-profile <SSID_NAME>
   # Look for "hidden" or "broadcast" setting
   ```

2. **Force Update on All APs**
   ```bash
   configure terminal
   wlan ssid-profile <SSID_NAME>
   exit
   # Force commit to all APs
   clear wlan ap session all
   # Or reboot APs
   ```

3. **Clear Client Cache**
   On client device:
   - Forget the network
   - Clear WiFi cache
   - Reconnect

---

### Version and Dependency Issues

#### Issue: "ModuleNotFoundError: No module named 'pexpect'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'pexpect'
```

**Root Causes:**
1. Dependencies not installed
2. Wrong Python environment/virtualenv activated
3. Multiple Python versions installed

**Solutions:**

1. **Install Dependencies**
   ```bash
   pip install -e .
   ```

2. **Verify pexpect Installation**
   ```bash
   python -c "import pexpect; print(pexpect.__version__)"
   ```

3. **Check Python Version**
   ```bash
   python --version
   # Should be 3.9 or higher
   ```

4. **Use Specific Python Version**
   ```bash
   python3.11 -m pip install -e .
   python3.11 -m aruba_ssid_manager --interactive
   ```

5. **Activate Virtualenv**
   ```bash
   source venv/bin/activate
   pip install -e .
   aruba-ssid-manager --interactive
   ```

---

#### Issue: Type annotation errors (Python < 3.9)

**Symptoms:**
```
SyntaxError: invalid syntax (on type annotation lines)
```

**Root Causes:**
1. Running Python version < 3.9
2. Type annotations using newer syntax

**Solution:**
Upgrade Python to 3.9 or higher:
```bash
python --version
# Should show 3.9.x or higher
python3.11 -m aruba_ssid_manager --interactive
```

---

### Performance and Resource Issues

#### Issue: Script uses excessive CPU or memory

**Symptoms:**
- Script runs very slowly
- High CPU usage
- Memory consumption increasing

**Root Causes:**
1. Network latency causing repeated retries
2. Logging too much data
3. Large logfile growing unbounded

**Solutions:**

1. **Disable Verbose Logging if Not Needed**
   ```bash
   # Remove --verbose flag
   aruba-ssid-manager --interactive
   ```

2. **Use Smaller Logfile**
   ```bash
   aruba-ssid-manager --interactive --logfile /tmp/aruba.log
   ```

3. **Implement Log Rotation**
   ```bash
   # Use logrotate as configured in deployment.md
   ```

4. **Check Network Latency**
   ```bash
   mtr <CONTROLLER_IP>
   # Look for high latency or packet loss
   ```

---

## Debugging Techniques

### Enable Verbose Logging

Always include `--verbose` flag when troubleshooting:
```bash
aruba-ssid-manager --interactive --verbose --logfile debug.log
```

### Capture Full SSH Session

Add pexpect logging to debug SSH communication:
```python
import pexpect
pexpect.spawn(...).logfile = open('session.log', 'wb')
```

### Manual SSH Testing

Test exact commands manually:
```bash
ssh admin@<CONTROLLER_IP>
configure terminal
wlan ssid-profile <SSID_NAME>
ssid-name <SSID_NAME>
# Manually verify each step
```

### Check System Logs

```bash
# Linux system logs
tail -f /var/log/syslog | grep ssh

# macOS system logs
log stream --predicate 'process == "ssh"'
```

---

## Getting Help

1. **Check Documentation**
   - [architecture.md](architecture.md) - System design
   - [api.md](api.md) - Function reference
   - [deployment.md](deployment.md) - Installation guide

2. **Enable Verbose Logging**
   ```bash
   aruba-ssid-manager --interactive --verbose
   ```

3. **Consult contributing.md**
   - See [contributing.md](contributing.md) for bug reporting
   - Include verbose logs and exact error messages

---

---

Author: Kris Armstrong
