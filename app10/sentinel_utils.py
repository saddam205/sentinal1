# sentinel_utils.py
import re
import shlex
import aiohttp
from typing import List, Optional

class SafetyCage:
    """🛡️ Layer 8: Validates AI-generated commands before execution."""
    def __init__(self):
        # Allowed tools in your CyberSec environment
        self.WHITELIST = ['nmap', 'sqlmap', 'nikto', 'hydra', 'curl', 'ping', 'dirb', 'whois']
        # Critical patterns to block (Destructive intent)
        self.DANGER_ZONES = [
            r"rm\s+-rf", r"/etc/shadow", r"mkfs", r"> /dev/sd", 
            r"chmod 777", r"chown", r"wget\s+http.*\.sh"
        ]

    def validate(self, cmd: str) -> bool:
        """Returns True only if the command is safe to run."""
        try:
            tokens = shlex.split(cmd)
            if not tokens: return False
            
            # 1. Check if the tool itself is whitelisted
            base_tool = tokens[0].lower()
            if base_tool not in self.WHITELIST:
                return False
                
            # 2. Check for dangerous substrings/patterns
            if any(re.search(p, cmd, re.IGNORECASE) for p in self.DANGER_ZONES):
                return False
                
            return True
        except Exception:
            return False

async def fetch_internet_intel(query: str) -> str:
    """Fallback: Deep Research Loop for unknown exploits/CVEs."""
    # This acts as the automated research loop
    return f"[Intel] No local RAG match. Researching CVE data for: {query}."