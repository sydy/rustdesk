#!/usr/bin/env python3
"""
Script to create a signed custom configuration for RustDesk Windows version.
This sets the default configuration for:
- ID Server: 115.190.126.11
- KEY: GQmOf5Ad8rjQb0PVzUvc7ZvDKD4V01EcfWiirEB+KiU=
- Security: Full Access
- Password: lm8p2E5936 (fixed password)
"""

import json
import base64

# Configuration to be embedded
config = {
    "default-settings": {
        "custom-rendezvous-server": "115.190.126.11",
        "key": "GQmOf5Ad8rjQb0PVzUvc7ZvDKD4V01EcfWiirEB+KiU=",
        "access-mode": "full",
        "permanent-password": "lm8p2E5936",
        "verification-method": "use-permanent-password",
        "approve-mode": "password"
    }
}

# The public key from the RustDesk source code (used for verification)
# The corresponding private key would be needed to sign the configuration
PUBLIC_KEY = "5Qbwsde3unUcJBtrx9ZkvUmwFNoExHzpryHuPUdqlWM="

def create_unsigned_config():
    """Create the unsigned configuration for testing purposes"""
    # Convert to JSON
    json_data = json.dumps(config, separators=(',', ':'))
    
    # Base64 encode
    encoded_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
    
    print("Unsigned configuration (for testing):")
    print(encoded_data)
    print()
    
    # Write to file
    with open('custom.txt', 'w') as f:
        f.write(encoded_data)
    
    print("Configuration written to custom.txt")
    print()
    print("Note: This is an unsigned configuration. For production use,")
    print("you would need to sign it with the corresponding private key.")
    print()
    print("Configuration details:")
    print(f"- ID Server: {config['default-settings']['custom-rendezvous-server']}")
    print(f"- KEY: {config['default-settings']['key']}")
    print(f"- Access Mode: {config['default-settings']['access-mode']}")
    print(f"- Fixed Password: {config['default-settings']['permanent-password']}")
    print(f"- Verification Method: {config['default-settings']['verification-method']}")
    
if __name__ == "__main__":
    create_unsigned_config()