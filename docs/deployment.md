# Deployment Guide

## Prerequisites

- Python 3.9 or higher
- Access to Aruba wireless controller(s)
- SSH enabled on Aruba controller
- Valid SSH credentials with configuration privileges

## System Requirements

### Minimum Requirements
- OS: Linux, macOS, or Windows (with Python 3.9+)
- RAM: 256 MB
- Disk Space: 10 MB
- Network: SSH connectivity to Aruba controller

### Recommended Configuration
- Python 3.11 or higher
- Dedicated system user account for running tool
- Secure credential management system
- Log aggregation for audit trails

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-org/aruba-ssid-manager.git
cd aruba-ssid-manager
```

### 2. Install Dependencies

```bash
pip install -e .
```

The editable install pulls in required dependencies such as:
- `pexpect>=4.8` – SSH session automation

### 3. Verify Installation

```bash
aruba-ssid-manager --help
```

Expected output:
```
usage: aruba-ssid-manager [-h] [--host HOST] [--username USERNAME]
                                  [--password PASSWORD] [--ssid SSID] ...
```

## Configuration

### Environment Setup

#### Option 1: Direct Execution
```bash
aruba-ssid-manager --host 10.0.0.1 --username admin \
  --password mypassword --ssid MySSID --vlan 10 --wlan-profile default
```

#### Option 2: Interactive Mode
```bash
aruba-ssid-manager --interactive
```

#### Option 3: Scheduled Execution (Cron)

Create a configuration file `/etc/aruba/config.sh`:
```bash
#!/bin/bash
HOST="10.0.0.1"
USERNAME="admin"
PASSWORD="secure_password"
SSID="GuestNetwork"
VLAN="20"
WLAN_PROFILE="guest"

python -m aruba_ssid_manager \
  --host "$HOST" \
  --username "$USERNAME" \
  --password "$PASSWORD" \
  --ssid "$SSID" \
  --vlan "$VLAN" \
  --wlan-profile "$WLAN_PROFILE" \
  --logfile /var/log/aruba_config.log
```

Make executable:
```bash
chmod +x /etc/aruba/config.sh
```

#### Option 4: Systemd Service

Create `/etc/systemd/system/aruba-config.service`:
```ini
[Unit]
Description=Aruba SSID Manager
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /opt/aruba/aruba-ssid-manager \
  --host 10.0.0.1 --username admin --password pass \
  --ssid MySSID --vlan 10 --wlan-profile default
StandardOutput=journal
StandardError=journal
User=aruba
Group=aruba

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable aruba-config.service
```

Run manually:
```bash
sudo systemctl start aruba-config.service
```

### Logging Configuration

#### Console Logging
```bash
aruba-ssid-manager --interactive --verbose
```

#### File Logging
```bash
aruba-ssid-manager --interactive --logfile /var/log/aruba_config.log
```

#### Both Console and File
```bash
aruba-ssid-manager --interactive --verbose --logfile /var/log/aruba_config.log
```

## Credential Management

### Security Best Practices

**NEVER commit credentials to version control!**

#### Option 1: Environment Variables (Linux/macOS)

```bash
export ARUBA_HOST="10.0.0.1"
export ARUBA_USERNAME="admin"
export ARUBA_PASSWORD="secure_password"
export ARUBA_SSID="MyNetwork"
export ARUBA_VLAN="10"
export ARUBA_WLAN_PROFILE="default"

aruba-ssid-manager \
  --host "$ARUBA_HOST" \
  --username "$ARUBA_USERNAME" \
  --password "$ARUBA_PASSWORD" \
  --ssid "$ARUBA_SSID" \
  --vlan "$ARUBA_VLAN" \
  --wlan-profile "$ARUBA_WLAN_PROFILE"
```

#### Option 2: Secure Credential Storage

Use tools like:
- **HashiCorp Vault**: Enterprise secret management
- **AWS Secrets Manager**: Cloud-based secrets
- **1Password CLI**: Developer credential manager
- **pass**: Unix password manager

Example with pass:
```bash
aruba-ssid-manager \
  --host 10.0.0.1 \
  --username admin \
  --password "$(pass show aruba/admin_password)" \
  --ssid MySSID --vlan 10 --wlan-profile default
```

#### Option 3: Interactive Prompt (Most Secure)

```bash
aruba-ssid-manager --interactive
```

The password is masked during input and never echoed to terminal.

## Deployment Scenarios

### Scenario 1: Single Controller Configuration

```bash
#!/bin/bash
aruba-ssid-manager \
  --host 192.168.1.100 \
  --username netadmin \
  --password "$(pass show work/aruba)" \
  --ssid CorporateNetwork \
  --vlan 100 \
  --wlan-profile corporate \
  --logfile /var/log/aruba/corporate.log
```

### Scenario 2: Multiple Controllers (Loop)

```bash
#!/bin/bash
CONTROLLERS=("192.168.1.100" "192.168.1.101" "192.168.1.102")
USERNAME="admin"
PASSWORD="$(pass show aruba/admin)"

for CONTROLLER in "${CONTROLLERS[@]}"; do
    echo "Configuring $CONTROLLER..."
    aruba-ssid-manager \
      --host "$CONTROLLER" \
      --username "$USERNAME" \
      --password "$PASSWORD" \
      --ssid SharedNetwork \
      --vlan 50 \
      --wlan-profile default \
      --logfile "/var/log/aruba/config_$CONTROLLER.log"
done
```

### Scenario 3: Ansible Integration

```yaml
- name: Configure Aruba SSID
  hosts: network_admins
  tasks:
    - name: Run SSID configurator
      command: |
        python -m aruba_ssid_manager
        --host {{ inventory_hostname }}
        --username {{ aruba_admin_user }}
        --password {{ aruba_admin_password }}
        --ssid {{ ssid_name }}
        --vlan {{ vlan_id }}
        --wlan-profile {{ wlan_profile }}
        --logfile /var/log/aruba_{{ inventory_hostname }}.log
      register: ssid_config_result
```

### Scenario 4: Container Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY aruba-ssid-manager .

ENTRYPOINT ["python", "aruba-ssid-manager"]
```

Build and run:
```bash
docker build -t aruba-ssid-config .

docker run --rm aruba-ssid-config \
  --host 10.0.0.1 \
  --username admin \
  --password mypassword \
  --ssid DockerSSID \
  --vlan 30 \
  --wlan-profile default
```

## Testing Deployment

### Pre-Deployment Validation

1. **Test SSH Connectivity**
   ```bash
   ssh admin@10.0.0.1
   # Test login, then exit
   ```

2. **Test Script in Dry Run (if available)**
   ```bash
   aruba-ssid-manager --interactive --verbose
   # Verify all prompts and parameters
   ```

3. **Verify Python Version**
   ```bash
   python --version
   # Should be 3.9 or higher
   ```

4. **Check Dependencies**
   ```bash
   python -c "import pexpect; print(pexpect.__version__)"
   ```

### Post-Deployment Verification

1. **Check Logs**
   ```bash
   tail -f /var/log/aruba_config.log
   ```

2. **Verify SSID on Controller**
   ```bash
   ssh admin@10.0.0.1
   show wlan ssid-profile [SSID_NAME]
   ```

3. **Test Connectivity**
   ```bash
   # Connect device to newly configured SSID
   # Verify successful connection and proper VLAN assignment
   ```

## Rollback Procedures

If configuration fails or needs to be reverted:

1. **Manual Rollback via SSH**
   ```bash
   ssh admin@10.0.0.1
   configure terminal
   no wlan ssid-profile [SSID_NAME]
   exit
   write memory
   ```

2. **Configuration Backup**
   ```bash
   # Backup controller config before making changes
   ssh admin@10.0.0.1
   show running-config > backup_$(date +%s).txt
   ```

## Monitoring and Logging

### Log Locations

- **Console Output**: Stdout during execution
- **File Logging**: Specified with `--logfile` parameter
- **System Logging**: If using systemd service, check with `journalctl`

### Recommended Log Rotation

Create `/etc/logrotate.d/aruba`:
```
/var/log/aruba_*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 aruba aruba
    sharedscripts
    postrotate
        systemctl restart aruba-config.service > /dev/null 2>&1 || true
    endscript
}
```

### Alert Configuration

Monitor logs for errors:
```bash
# Email alerts on configuration failures
grep -i "critical\|error" /var/log/aruba_config.log | \
  mail -s "Aruba Config Error" admin@company.com
```

## Performance Considerations

- **Connection Timeout**: 30 seconds per command
- **Typical Execution Time**: 5-15 seconds for single SSID
- **Multiple Controllers**: Run sequentially to avoid overwhelming network

## Security Hardening

1. **File Permissions**
   ```bash
   chmod 700 aruba-ssid-manager
   chmod 600 /etc/aruba/config.sh
   chmod 640 /var/log/aruba_config.log
   ```

2. **User Isolation**
   ```bash
   useradd -r -s /bin/false aruba
   chown aruba:aruba /opt/aruba/
   ```

3. **Audit Logging**
   ```bash
   # Enable auditd for script execution
   auditctl -w /opt/aruba/ -p wa -k aruba_changes
   ```

4. **SSH Key Authentication (Recommended)**
   Use SSH key-based authentication instead of passwords when possible

## Troubleshooting Deployment

See [troubleshooting.md](troubleshooting.md) for common issues and solutions.

## Support

For deployment issues:
1. Check logs with `--verbose` flag
2. Test SSH connectivity independently
3. Verify credentials have configuration privileges
4. Consult [troubleshooting.md](troubleshooting.md)
5. Review [contributing.md](contributing.md) for bug reporting

---

Author: Kris Armstrong
