# correlation_engine.py - Complete Correlation Engine Layer
# Event-Driven Security Intelligence Platform
# Part of CyberSec Lab v6.2

import json
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import numpy as np
from collections import defaultdict
import threading
import queue
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================== ENUMS & CONSTANTS ====================

class EventType(str, Enum):
    """Unified event types across all tools"""
    # Reconnaissance Events
    PORT_SCAN = "PORT_SCAN"
    SERVICE_DETECTION = "SERVICE_DETECTION"
    OS_FINGERPRINT = "OS_FINGERPRINT"
    DIRECTORY_ENUM = "DIRECTORY_ENUM"
    VULNERABILITY_SCAN = "VULNERABILITY_SCAN"
    
    # Vulnerability Events
    SQL_INJECTION_POTENTIAL = "SQL_INJECTION_POTENTIAL"
    SQL_INJECTION_CONFIRMED = "SQL_INJECTION_CONFIRMED"
    XSS_POTENTIAL = "XSS_POTENTIAL"
    XSS_CONFIRMED = "XSS_CONFIRMED"
    COMMAND_INJECTION = "COMMAND_INJECTION"
    FILE_INCLUSION = "FILE_INCLUSION"
    
    # Authentication Events
    WEAK_CREDENTIALS = "WEAK_CREDENTIALS"
    BRUTE_FORCE_SUCCESS = "BRUTE_FORCE_SUCCESS"
    CREDENTIAL_COMPROMISED = "CREDENTIAL_COMPROMISED"
    DEFAULT_CREDENTIALS = "DEFAULT_CREDENTIALS"
    
    # Database Events
    DATABASE_EXPOSED = "DATABASE_EXPOSED"
    DATA_EXFILTRATION = "DATA_EXFILTRATION"
    DATABASE_SCHEMA_DISCOVERED = "DATABASE_SCHEMA_DISCOVERED"
    
    # Exploitation Events
    REMOTE_SHELL_ESTABLISHED = "REMOTE_SHELL_ESTABLISHED"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"
    CODE_EXECUTION = "CODE_EXECUTION"
    
    # Network Events
    MITM_DETECTED = "MITM_DETECTED"
    TRAFFIC_ANOMALY = "TRAFFIC_ANOMALY"
    CREDENTIAL_SNIFFED = "CREDENTIAL_SNIFFED"
    
    # Wireless Events
    WEP_CRACKED = "WEP_CRACKED"
    WPA_HANDSHAKE_CAPTURED = "WPA_HANDSHAKE_CAPTURED"
    WPA_CRACKED = "WPA_CRACKED"
    
    # Post-Exploitation
    PERSISTENCE_ESTABLISHED = "PERSISTENCE_ESTABLISHED"
    LATERAL_MOVEMENT = "LATERAL_MOVEMENT"
    CREDENTIAL_DUMP = "CREDENTIAL_DUMP"
    
    # Unknown
    UNKNOWN = "UNKNOWN"


class SeverityLevel(float, Enum):
    """Numeric severity levels for scoring"""
    INFO = 0.5
    LOW = 2.0
    MEDIUM = 4.0
    HIGH = 7.0
    CRITICAL = 9.0
    MAX = 10.0


class AttackPhase(str, Enum):
    """MITRE ATT&CK phases"""
    RECONNAISSANCE = "RECONNAISSANCE"
    RESOURCE_DEVELOPMENT = "RESOURCE_DEVELOPMENT"
    INITIAL_ACCESS = "INITIAL_ACCESS"
    EXECUTION = "EXECUTION"
    PERSISTENCE = "PERSISTENCE"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"
    DEFENSE_EVASION = "DEFENSE_EVASION"
    CREDENTIAL_ACCESS = "CREDENTIAL_ACCESS"
    DISCOVERY = "DISCOVERY"
    LATERAL_MOVEMENT = "LATERAL_MOVEMENT"
    COLLECTION = "COLLECTION"
    COMMAND_AND_CONTROL = "COMMAND_AND_CONTROL"
    EXFILTRATION = "EXFILTRATION"
    IMPACT = "IMPACT"


# ==================== CORE DATA MODELS ====================

@dataclass
class SecurityEvent:
    """Unified security event model - Core Intelligence Unit"""
    event_id: str
    event_type: EventType
    severity: float
    asset: str
    evidence: Dict[str, Any]
    timestamp: datetime
    source_tool: str
    confidence: float = 0.8
    tags: List[str] = field(default_factory=list)
    raw_output: Optional[str] = None
    mitre_phase: Optional[AttackPhase] = None
    user_id: Optional[int] = None
    
    def __post_init__(self):
        if not self.event_id:
            self.event_id = str(uuid.uuid4())
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        result['event_type'] = self.event_type.value
        result['mitre_phase'] = self.mitre_phase.value if self.mitre_phase else None
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SecurityEvent':
        """Create from dictionary"""
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        if 'event_type' in data and isinstance(data['event_type'], str):
            data['event_type'] = EventType(data['event_type'])
        if 'mitre_phase' in data and data['mitre_phase'] and isinstance(data['mitre_phase'], str):
            data['mitre_phase'] = AttackPhase(data['mitre_phase'])
        return cls(**data)
    
    def hash_key(self) -> str:
        """Generate unique hash for deduplication"""
        key_str = f"{self.event_type.value}_{self.asset}_{self.timestamp.strftime('%Y%m%d%H')}"
        return hashlib.md5(key_str.encode()).hexdigest()


@dataclass
class Trigger:
    """Action trigger from correlation engine"""
    trigger_id: str
    trigger_type: str
    target: str
    parameters: Dict[str, Any]
    priority: int
    source_event_id: str
    timestamp: datetime
    executed: bool = False
    result: Optional[Dict] = None


# ==================== LAYER 1: TOOL RESULT NORMALIZER ====================

class ToolResultNormalizer:
    """Convert tool-specific outputs to unified SecurityEvents"""
    
    # ========== SCANNER NORMALIZERS ==========
    
    def normalize_nmap(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert nmap output to security events"""
        events = []
        
        # Extract open ports as PORT_SCAN events
        if 'ports' in raw_output:
            ports = raw_output.get('ports', [])
            if ports:
                events.append(SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.PORT_SCAN,
                    severity=SeverityLevel.INFO,
                    asset=target,
                    evidence={'ports': ports, 'count': len(ports)},
                    timestamp=datetime.utcnow(),
                    source_tool='nmap',
                    tags=['reconnaissance', 'port_scan'],
                    mitre_phase=AttackPhase.RECONNAISSANCE
                ))
        
        # Extract services as SERVICE_DETECTION events
        if 'services' in raw_output:
            services = raw_output.get('services', [])
            for service in services:
                events.append(SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.SERVICE_DETECTION,
                    severity=SeverityLevel.INFO,
                    asset=f"{target}:{service.get('port', 'unknown')}",
                    evidence=service,
                    timestamp=datetime.utcnow(),
                    source_tool='nmap',
                    tags=['reconnaissance', 'service_detection'],
                    mitre_phase=AttackPhase.RECONNAISSANCE
                ))
        
        # Extract OS detection
        if raw_output.get('os'):
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.OS_FINGERPRINT,
                severity=SeverityLevel.INFO,
                asset=target,
                evidence={'os': raw_output['os']},
                timestamp=datetime.utcnow(),
                source_tool='nmap',
                tags=['reconnaissance', 'os_fingerprint'],
                mitre_phase=AttackPhase.RECONNAISSANCE
            ))
        
        # Extract vulnerabilities from NSE scripts
        vulns = raw_output.get('vulnerabilities', [])
        for vuln in vulns:
            event_type = EventType.UNKNOWN
            severity = SeverityLevel.MEDIUM
            
            vuln_name = vuln.get('name', '').lower()
            if 'sql' in vuln_name:
                event_type = EventType.SQL_INJECTION_POTENTIAL
                severity = SeverityLevel.HIGH
            elif 'xss' in vuln_name:
                event_type = EventType.XSS_POTENTIAL
                severity = SeverityLevel.MEDIUM
            elif 'rce' in vuln_name or 'remote' in vuln_name:
                event_type = EventType.COMMAND_INJECTION
                severity = SeverityLevel.CRITICAL
            
            if event_type != EventType.UNKNOWN:
                events.append(SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=event_type,
                    severity=severity,
                    asset=target,
                    evidence=vuln,
                    timestamp=datetime.utcnow(),
                    source_tool='nmap_script',
                    tags=['vulnerability', 'nse'],
                    mitre_phase=AttackPhase.INITIAL_ACCESS
                ))
        
        return events
    
    def normalize_masscan(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert masscan output to security events"""
        events = []
        
        if 'ports' in raw_output:
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.PORT_SCAN,
                severity=SeverityLevel.INFO,
                asset=target,
                evidence={'ports': raw_output['ports'], 'type': 'masscan'},
                timestamp=datetime.utcnow(),
                source_tool='masscan',
                tags=['reconnaissance', 'mass_scan'],
                mitre_phase=AttackPhase.RECONNAISSANCE
            ))
        
        return events
    
       
    # ========== WEB TOOL NORMALIZERS ==========
    
    def normalize_sqlmap(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert SQLMap output to security events"""
        events = []
        
        # SQL Injection potential
        if raw_output.get('success'):
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.SQL_INJECTION_CONFIRMED,
                severity=SeverityLevel.CRITICAL,
                asset=target,
                evidence=raw_output,
                timestamp=datetime.utcnow(),
                source_tool='sqlmap',
                confidence=0.95,
                tags=['web', 'sqli', 'confirmed'],
                mitre_phase=AttackPhase.INITIAL_ACCESS
            ))
            
            # Database exposure
            if 'databases' in raw_output:
                events.append(SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.DATABASE_SCHEMA_DISCOVERED,
                    severity=SeverityLevel.HIGH,
                    asset=target,
                    evidence={'databases': raw_output['databases']},
                    timestamp=datetime.utcnow(),
                    source_tool='sqlmap',
                    tags=['database', 'discovery'],
                    mitre_phase=AttackPhase.DISCOVERY
                ))
        
        return events
    
    def normalize_nikto(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert Nikto output to security events"""
        events = []
        
        vulns = raw_output.get('vulnerabilities', [])
        for vuln in vulns:
            vuln_name = vuln.get('name', '').lower()
            
            if 'xss' in vuln_name:
                events.append(SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.XSS_POTENTIAL,
                    severity=SeverityLevel.HIGH,
                    asset=f"{target}{vuln.get('path', '')}",
                    evidence=vuln,
                    timestamp=datetime.utcnow(),
                    source_tool='nikto',
                    tags=['web', 'xss'],
                    mitre_phase=AttackPhase.INITIAL_ACCESS
                ))
            elif 'sql' in vuln_name:
                events.append(SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.SQL_INJECTION_POTENTIAL,
                    severity=SeverityLevel.CRITICAL,
                    asset=f"{target}{vuln.get('path', '')}",
                    evidence=vuln,
                    timestamp=datetime.utcnow(),
                    source_tool='nikto',
                    tags=['web', 'sqli'],
                    mitre_phase=AttackPhase.INITIAL_ACCESS
                ))
            elif 'file' in vuln_name or 'include' in vuln_name:
                events.append(SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.FILE_INCLUSION,
                    severity=SeverityLevel.HIGH,
                    asset=f"{target}{vuln.get('path', '')}",
                    evidence=vuln,
                    timestamp=datetime.utcnow(),
                    source_tool='nikto',
                    tags=['web', 'lfi'],
                    mitre_phase=AttackPhase.INITIAL_ACCESS
                ))
        
        return events
    
    def normalize_gobuster(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert Gobuster output to security events"""
        events = []
        
        dirs = raw_output.get('directories', [])
        if dirs:
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.DIRECTORY_ENUM,
                severity=SeverityLevel.LOW,
                asset=target,
                evidence={'directories': dirs, 'count': len(dirs)},
                timestamp=datetime.utcnow(),
                source_tool='gobuster',
                tags=['web', 'enumeration'],
                mitre_phase=AttackPhase.RECONNAISSANCE
            ))
        
        return events
    
    def normalize_burp(self, finding: Dict, target: str) -> SecurityEvent:
        """Convert Burp Suite finding to security event"""
        severity_map = {
            'CRITICAL': SeverityLevel.CRITICAL,
            'HIGH': SeverityLevel.HIGH,
            'MEDIUM': SeverityLevel.MEDIUM,
            'LOW': SeverityLevel.LOW,
            'INFO': SeverityLevel.INFO
        }
        
        title = finding.get('title', '').lower()
        
        if 'sql' in title:
            event_type = EventType.SQL_INJECTION_CONFIRMED
        elif 'xss' in title:
            event_type = EventType.XSS_CONFIRMED
        elif 'command' in title:
            event_type = EventType.COMMAND_INJECTION
        elif 'directory' in title:
            event_type = EventType.DIRECTORY_ENUM
        else:
            event_type = EventType.UNKNOWN
        
        return SecurityEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            severity=severity_map.get(finding.get('severity', 'MEDIUM'), SeverityLevel.MEDIUM),
            asset=finding.get('path', target),
            evidence=finding,
            timestamp=datetime.utcnow(),
            source_tool='burp_suite',
            tags=['web', 'burp', event_type.value.lower()],
            mitre_phase=AttackPhase.INITIAL_ACCESS
        )
    
    def normalize_wpscan(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert WPScan output to security events"""
        events = []
        
        vulns = raw_output.get('vulnerabilities', [])
        for vuln in vulns:
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.UNKNOWN,
                severity=SeverityLevel.MEDIUM,
                asset=target,
                evidence=vuln,
                timestamp=datetime.utcnow(),
                source_tool='wpscan',
                tags=['wordpress', 'vulnerability'],
                mitre_phase=AttackPhase.INITIAL_ACCESS
            ))
        
        return events
    
    # ========== PASSWORD ATTACK NORMALIZERS ==========
    
    def normalize_hydra(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert Hydra output to security events"""
        events = []
        
        creds = raw_output.get('credentials', [])
        for cred in creds:
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.CREDENTIAL_COMPROMISED,
                severity=SeverityLevel.CRITICAL,
                asset=target,
                evidence=cred,
                timestamp=datetime.utcnow(),
                source_tool='hydra',
                confidence=0.95,
                tags=['authentication', 'bruteforce', 'credentials'],
                mitre_phase=AttackPhase.CREDENTIAL_ACCESS
            ))
            
            # Also add weak credentials event
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.WEAK_CREDENTIALS,
                severity=SeverityLevel.HIGH,
                asset=target,
                evidence=cred,
                timestamp=datetime.utcnow(),
                source_tool='hydra',
                tags=['authentication', 'weak'],
                mitre_phase=AttackPhase.CREDENTIAL_ACCESS
            ))
        
        return events
    
    def normalize_john(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert John the Ripper output to security events"""
        events = []
        
        cracked = raw_output.get('cracked', [])
        if cracked:
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.CREDENTIAL_COMPROMISED,
                severity=SeverityLevel.CRITICAL,
                asset=target,
                evidence={'cracked_passwords': cracked, 'count': len(cracked)},
                timestamp=datetime.utcnow(),
                source_tool='john',
                tags=['password', 'cracking'],
                mitre_phase=AttackPhase.CREDENTIAL_ACCESS
            ))
        
        return events
    
    def normalize_hashcat(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert Hashcat output to security events"""
        events = []
        
        if raw_output.get('cracked'):
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.CREDENTIAL_COMPROMISED,
                severity=SeverityLevel.CRITICAL,
                asset=target,
                evidence=raw_output,
                timestamp=datetime.utcnow(),
                source_tool='hashcat',
                tags=['password', 'gpu', 'cracking'],
                mitre_phase=AttackPhase.CREDENTIAL_ACCESS
            ))
        
        return events
    
    # ========== EXPLOITATION NORMALIZERS ==========
    
    def normalize_metasploit(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert Metasploit output to security events"""
        events = []
        
        if raw_output.get('session'):
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.REMOTE_SHELL_ESTABLISHED,
                severity=SeverityLevel.MAX,
                asset=target,
                evidence=raw_output,
                timestamp=datetime.utcnow(),
                source_tool='metasploit',
                confidence=0.98,
                tags=['exploitation', 'shell', 'meterpreter'],
                mitre_phase=AttackPhase.EXECUTION
            ))
        
        if raw_output.get('privilege'):
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.PRIVILEGE_ESCALATION,
                severity=SeverityLevel.CRITICAL,
                asset=target,
                evidence=raw_output,
                timestamp=datetime.utcnow(),
                source_tool='metasploit',
                tags=['post-exploitation', 'privesc'],
                mitre_phase=AttackPhase.PRIVILEGE_ESCALATION
            ))
        
        return events
    
    # ========== SNIFFER NORMALIZERS ==========
    
    def normalize_wireshark(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert Wireshark output to security events"""
        events = []
        
        # Check for credential sniffing
        if raw_output.get('unencrypted_creds'):
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.CREDENTIAL_SNIFFED,
                severity=SeverityLevel.HIGH,
                asset=raw_output.get('dst_ip', target),
                evidence=raw_output,
                timestamp=datetime.utcnow(),
                source_tool='wireshark',
                tags=['network', 'sniffing'],
                mitre_phase=AttackPhase.CREDENTIAL_ACCESS
            ))
        
        # Check for traffic anomalies
        protocols = raw_output.get('protocols', {})
        if protocols.get('HTTP') and protocols['HTTP'] > 100:
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.TRAFFIC_ANOMALY,
                severity=SeverityLevel.MEDIUM,
                asset=target,
                evidence={'http_traffic': protocols['HTTP']},
                timestamp=datetime.utcnow(),
                source_tool='wireshark',
                tags=['network', 'traffic'],
                mitre_phase=AttackPhase.COLLECTION
            ))
        
        return events
    
    def normalize_ettercap(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert Ettercap output to security events"""
        events = []
        
        if 'arp_poisoning' in raw_output:
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.MITM_DETECTED,
                severity=SeverityLevel.CRITICAL,
                asset=target,
                evidence=raw_output,
                timestamp=datetime.utcnow(),
                source_tool='ettercap',
                tags=['network', 'mitm', 'arp'],
                mitre_phase=AttackPhase.COLLECTION
            ))
        
        return events
    
    # ========== WIRELESS NORMALIZERS ==========
    
    def normalize_aircrack(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert Aircrack-ng output to security events"""
        events = []
        
        if raw_output.get('handshake'):
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.WPA_HANDSHAKE_CAPTURED,
                severity=SeverityLevel.HIGH,
                asset=target,
                evidence={'handshake': True, 'bssid': raw_output.get('bssid')},
                timestamp=datetime.utcnow(),
                source_tool='aircrack-ng',
                tags=['wireless', 'wpa'],
                mitre_phase=AttackPhase.CREDENTIAL_ACCESS
            ))
        
        if raw_output.get('key'):
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.WPA_CRACKED,
                severity=SeverityLevel.CRITICAL,
                asset=target,
                evidence={'key': raw_output['key']},
                timestamp=datetime.utcnow(),
                source_tool='aircrack-ng',
                tags=['wireless', 'cracked'],
                mitre_phase=AttackPhase.CREDENTIAL_ACCESS
            ))
        
        return events
    
    # ========== POST-EXPLOITATION NORMALIZERS ==========
    
    def normalize_mimikatz(self, raw_output: Dict, target: str) -> List[SecurityEvent]:
        """Convert Mimikatz output to security events"""
        events = []
        
        if 'credentials' in raw_output:
            events.append(SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.CREDENTIAL_DUMP,
                severity=SeverityLevel.CRITICAL,
                asset=target,
                evidence=raw_output,
                timestamp=datetime.utcnow(),
                source_tool='mimikatz',
                tags=['windows', 'credentials', 'lsass'],
                mitre_phase=AttackPhase.CREDENTIAL_ACCESS
            ))
        
        return events


# ==================== LAYER 2: EVENT BUS ====================

class EventBus:
    """Event-driven core - all events flow through here"""
    
    def __init__(self):
        self.subscribers: Dict[EventType, List['EventHandler']] = defaultdict(list)
        self.global_subscribers: List['EventHandler'] = []
        self.event_queue = queue.Queue()
        self.processing = False
        self.stats = {
            'total_events': 0,
            'events_by_type': defaultdict(int),
            'start_time': datetime.utcnow()
        }
        self._start_processing()
    
    def subscribe(self, handler: 'EventHandler', event_types: Optional[List[EventType]] = None):
        """Subscribe handler to specific event types or all events"""
        if event_types:
            for event_type in event_types:
                self.subscribers[event_type].append(handler)
        else:
            self.global_subscribers.append(handler)
    
    def publish(self, event: SecurityEvent):
        """Publish event to all subscribers"""
        self.event_queue.put(event)
        self.stats['total_events'] += 1
        self.stats['events_by_type'][event.event_type] += 1
    
    def publish_many(self, events: List[SecurityEvent]):
        """Publish multiple events"""
        for event in events:
            self.publish(event)
    
    def _start_processing(self):
        """Start background event processing"""
        self.processing = True
        
        def processor():
            while self.processing:
                try:
                    event = self.event_queue.get(timeout=1)
                    self._process_event(event)
                    self.event_queue.task_done()
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"Event processing error: {e}")
        
        thread = threading.Thread(target=processor, daemon=True)
        thread.start()
    
    def _process_event(self, event: SecurityEvent):
        """Process single event"""
        for handler in self.subscribers.get(event.event_type, []):
            try:
                handler.handle(event)
            except Exception as e:
                logger.error(f"Handler error for {event.event_type}: {e}")
        
        for handler in self.global_subscribers:
            try:
                handler.handle(event)
            except Exception as e:
                logger.error(f"Global handler error: {e}")
    
    def stop(self):
        """Stop event processing"""
        self.processing = False
    
    def get_stats(self) -> Dict:
        """Get event bus statistics"""
        return {
            **self.stats,
            'queue_size': self.event_queue.qsize(),
            'uptime_seconds': (datetime.utcnow() - self.stats['start_time']).total_seconds()
        }


class EventHandler:
    """Base class for event handlers"""
    
    def handle(self, event: SecurityEvent):
        """Handle event - to be overridden"""
        raise NotImplementedError


# ==================== LAYER 3: CORRELATION ENGINE ====================

class CorrelationEngine(EventHandler):
    """
    Layer 7: Core Correlation Engine
    Connects Attack Graph, Risk Engine, and Decision Brain to identify multi-stage threats.
    """
    
    def __init__(self, attack_graph, risk_engine, decision_engine):
        super().__init__()
        self.attack_graph = attack_graph
        self.risk_engine = risk_engine
        self.decision_engine = decision_engine
        
        # State Management
        self.memory: List[SecurityEvent] = []
        self.event_window: Dict[str, List[SecurityEvent]] = defaultdict(list)
        self.triggers: List[Dict] = []
        
        # Load correlation rules
        self.correlation_rules = self._load_correlation_rules()
        logger.info(f"✓ Correlation Engine initialized with {len(self.correlation_rules)} active rules")

    def _load_correlation_rules(self) -> List[Dict]:
        """Load comprehensive correlation rules for multi-stage attack detection"""
        return [
            {
                'name': 'SQLi + DB Exposure = Critical',
                'pattern': [EventType.SQL_INJECTION_CONFIRMED, EventType.DATABASE_SCHEMA_DISCOVERED],
                'time_window': 300,
                'action': 'escalate',
                'new_severity': SeverityLevel.MAX
            },
            {
                'name': 'Credentials + Open Port = Attack Chain',
                'pattern': [EventType.CREDENTIAL_COMPROMISED, EventType.PORT_SCAN],
                'time_window': 600,
                'action': 'chain_detected',
                'new_event_type': EventType.LATERAL_MOVEMENT
            },
            {
                'name': 'Shell + Credential Dump = Full Compromise',
                'pattern': [EventType.REMOTE_SHELL_ESTABLISHED, EventType.CREDENTIAL_DUMP],
                'time_window': 1800,
                'action': 'full_compromise',
                'new_severity': SeverityLevel.MAX
            },
            {
                'name': 'WPA Handshake + Crack = WiFi Compromised',
                'pattern': [EventType.WPA_HANDSHAKE_CAPTURED, EventType.WPA_CRACKED],
                'time_window': 3600,
                'action': 'wifi_compromised',
                'new_severity': SeverityLevel.CRITICAL
            },
            {
                'name': 'Multiple XSS = Web App Vulnerable',
                'pattern': [EventType.XSS_POTENTIAL, EventType.XSS_POTENTIAL, EventType.XSS_POTENTIAL],
                'time_window': 600,
                'action': 'web_vulnerable',
                'new_severity': SeverityLevel.HIGH
            }
        ]

    def handle(self, event: SecurityEvent):
        """Process incoming event through correlation pipeline"""
        logger.info(f"Correlating event: {event.event_type.value} from {event.source_tool}")
        
        self.memory.append(event)
        self.attack_graph.update(event)
        
        # Update window and clean old events
        event_hash = event.hash_key() if hasattr(event, 'hash_key') else event.asset
        self.event_window[event_hash].append(event)
        self._clean_event_window()
        
        # Execute correlation logic
        correlated_events = self._apply_correlation_rules(event)
        
        # Recalculate Risk & trigger followups
        self.risk_engine.recalculate(self.memory)
        new_triggers = self._trigger_followups(event, correlated_events)
        self.triggers.extend(new_triggers)
        
        if len(self.memory) > 5:
            self.decision_engine.analyze(self.memory, self.attack_graph)

    def _clean_event_window(self, max_age_hours: int = 1):
        """Maintains memory efficiency for long-running scans"""
        cutoff = datetime.utcnow().timestamp() - (max_age_hours * 3600)
        for key in list(self.event_window.keys()):
            self.event_window[key] = [e for e in self.event_window[key] if e.timestamp.timestamp() > cutoff]
            if not self.event_window[key]:
                del self.event_window[key]

    def _apply_correlation_rules(self, event: SecurityEvent) -> List[SecurityEvent]:
        """Detect multi-stage attack patterns using rule signatures"""
        correlated = []
        now = datetime.utcnow()
        
        for rule in self.correlation_rules:
            pattern = rule['pattern']
            window = rule['time_window']
            
            recent_matches = [
                e for e in self.memory[-50:] 
                if e.event_type in pattern 
                and (now - e.timestamp).total_seconds() < window
                and e.asset == event.asset
            ]
            
            found_types = {e.event_type for e in recent_matches}
            
            if all(p in found_types for p in pattern):
                match_ids = sorted([e.event_id for e in recent_matches])
                rule_signature = hashlib.md5(f"{rule['name']}_{''.join(match_ids)}".encode()).hexdigest()
                
                if any(rule_signature in getattr(t, 'tags', []) for t in correlated):
                    continue

                logger.warning(f"🔥 ATTACK PATTERN DETECTED: {rule['name']}")
                
                new_event = SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=rule.get('new_event_type', EventType.LATERAL_MOVEMENT),
                    severity=rule.get('new_severity', SeverityLevel.CRITICAL),
                    asset=event.asset,
                    evidence={'rule_name': rule['name'], 'signature': rule_signature},
                    timestamp=now,
                    source_tool='correlation_engine',
                    tags=['correlated', rule['action'], rule_signature],
                    mitre_phase=AttackPhase.LATERAL_MOVEMENT
                )
                correlated.append(new_event)
        return correlated

    def _trigger_followups(self, event: SecurityEvent, correlated_events: List[SecurityEvent]) -> List[Dict]:
        """Generate triggers for the ActiveExploitEngine"""
        new_triggers = []
        for e in [event] + correlated_events:
            if e.severity >= SeverityLevel.HIGH or 'correlated' in e.tags:
                new_triggers.append({
                    'id': str(uuid.uuid4()),
                    'type': 'ALERT',
                    'priority': 'URGENT' if e.severity == SeverityLevel.MAX else 'NORMAL',
                    'description': f"Security Trigger: {e.event_type.value} on {e.asset}",
                    'source_event': e.event_id
                })
        return new_triggers


# ==================== LAYER 4: ATTACK GRAPH ====================

class AttackNode:
    """Node in attack graph"""
    
    def __init__(self, name: str, node_type: str = "event"):
        self.node_id = str(uuid.uuid4())
        self.name = name
        self.node_type = node_type
        self.children: List['AttackNode'] = []
        self.parents: List['AttackNode'] = []
        self.events: List[SecurityEvent] = []
        self.score = 0.0
        self.timestamp = datetime.utcnow()
    
    def add_child(self, child: 'AttackNode'):
        if child not in self.children:
            self.children.append(child)
            child.parents.append(self)
    
    def add_event(self, event: SecurityEvent):
        self.events.append(event)
        self.timestamp = datetime.utcnow()
        self.score = max([e.severity for e in self.events]) if self.events else 0


class AttackGraph:
    """Graph-based attack path modeling"""
    
    def __init__(self):
        self.nodes: Dict[str, AttackNode] = {}
        self.asset_nodes: Dict[str, AttackNode] = {}
        self.event_to_node: Dict[str, str] = {}
        self.graph_stats = {
            'total_nodes': 0,
            'total_edges': 0,
            'max_depth': 0
        }
    
    def update(self, event: SecurityEvent):
        """Update attack graph with new event"""
        asset_node = self._get_or_create_asset_node(event.asset)
        event_node = self._get_or_create_event_node(event.event_type.value)
        event_node.add_event(event)
        asset_node.add_child(event_node)
        self.event_to_node[event.event_id] = event_node.node_id
        self._detect_attack_chains()
        self._update_stats()
    
    def _get_or_create_asset_node(self, asset: str) -> AttackNode:
        if asset not in self.asset_nodes:
            node = AttackNode(asset, node_type="asset")
            self.asset_nodes[asset] = node
            self.nodes[node.node_id] = node
        return self.asset_nodes[asset]
    
    def _get_or_create_event_node(self, event_name: str) -> AttackNode:
        for node in self.nodes.values():
            if node.name == event_name and node.node_type == "event":
                return node
        node = AttackNode(event_name, node_type="event")
        self.nodes[node.node_id] = node
        return node
    
    def _detect_attack_chains(self):
        for asset_node in self.asset_nodes.values():
            if len(asset_node.children) >= 2:
                children = sorted(asset_node.children, key=lambda x: x.timestamp)
                if len(children) >= 3:
                    logger.info(f"Potential attack chain detected for asset {asset_node.name}")
    
    def get_attack_paths(self, asset: str) -> List[List[str]]:
        if asset not in self.asset_nodes:
            return []
        
        paths = []
        root = self.asset_nodes[asset]
        
        def dfs(node: AttackNode, current_path: List[str]):
            current_path.append(node.name)
            if not node.children:
                paths.append(current_path.copy())
            else:
                for child in node.children:
                    dfs(child, current_path)
            current_path.pop()
        
        dfs(root, [])
        return paths
    
    def get_critical_paths(self) -> List[List[str]]:
        critical_paths = []
        for asset_node in self.asset_nodes.values():
            if asset_node.score >= SeverityLevel.HIGH:
                paths = self.get_attack_paths(asset_node.name)
                critical_paths.extend(paths)
        return critical_paths
    
    def _update_stats(self):
        self.graph_stats['total_nodes'] = len(self.nodes)
        edges = sum(len(n.children) for n in self.nodes.values())
        self.graph_stats['total_edges'] = edges
        
        max_depth = 0
        for asset_node in self.asset_nodes.values():
            paths = self.get_attack_paths(asset_node.name)
            if paths:
                max_depth = max(max_depth, max(len(p) for p in paths))
        self.graph_stats['max_depth'] = max_depth
    
    def to_dict(self) -> Dict:
        return {
            'nodes': [
                {
                    'id': node.node_id,
                    'name': node.name,
                    'type': node.node_type,
                    'score': node.score,
                    'timestamp': node.timestamp.isoformat()
                }
                for node in self.nodes.values()
            ],
            'edges': [
                {
                    'from': parent.node_id,
                    'to': child.node_id
                }
                for parent in self.nodes.values()
                for child in parent.children
            ],
            'stats': self.graph_stats
        }


# ==================== LAYER 5: RISK ENGINE ====================

class RiskEngine:
    """Dynamic risk scoring based on events"""
    
    def __init__(self):
        self.base_weights = {
            EventType.SQL_INJECTION_CONFIRMED: 9.0,
            EventType.CREDENTIAL_COMPROMISED: 9.0,
            EventType.REMOTE_SHELL_ESTABLISHED: 10.0,
            EventType.PRIVILEGE_ESCALATION: 9.5,
            EventType.CREDENTIAL_DUMP: 9.0,
            EventType.WPA_CRACKED: 8.5,
            EventType.MITM_DETECTED: 8.0,
            EventType.COMMAND_INJECTION: 8.5,
            EventType.SQL_INJECTION_POTENTIAL: 6.0,
            EventType.XSS_CONFIRMED: 7.0,
            EventType.DATABASE_SCHEMA_DISCOVERED: 7.0,
            EventType.WEAK_CREDENTIALS: 5.0,
            EventType.WPA_HANDSHAKE_CAPTURED: 5.0,
        }
        
        self.asset_scores: Dict[str, float] = {}
        self.overall_score = 0.0
        self.score_history: List[Tuple[datetime, float]] = []
        self.thresholds = {
            'low': 3.0,
            'medium': 5.0,
            'high': 7.0,
            'critical': 9.0
        }
    
    def recalculate(self, events: List[SecurityEvent]) -> float:
        if not events:
            return 0.0
        
        asset_events = defaultdict(list)
        for event in events:
            asset_events[event.asset].append(event)
        
        total_weighted = 0.0
        total_assets = 0
        
        for asset, asset_event_list in asset_events.items():
            asset_score = self._calculate_asset_score(asset_event_list)
            self.asset_scores[asset] = asset_score
            total_weighted += asset_score
            total_assets += 1
        
        self.overall_score = total_weighted / max(total_assets, 1)
        
        self.score_history.append((datetime.utcnow(), self.overall_score))
        if len(self.score_history) > 100:
            self.score_history = self.score_history[-100:]
        
        return self.overall_score
    
    def _calculate_asset_score(self, events: List[SecurityEvent]) -> float:
        if not events:
            return 0.0
        
        score = 0.0
        event_types_seen = set()
        
        for event in events:
            weight = self.base_weights.get(event.event_type, 1.0)
            weight *= event.confidence
            
            hours_ago = (datetime.utcnow() - event.timestamp).total_seconds() / 3600
            recency_factor = max(0.5, 1.0 - (hours_ago / 24))
            weight *= recency_factor
            
            if event.event_type not in event_types_seen:
                event_types_seen.add(event.event_type)
                weight *= 1.2
            
            score += weight
        
        return min(score / len(events) * 1.5, 10.0)
    
    def get_risk_level(self, score: float = None) -> str:
        if score is None:
            score = self.overall_score
        
        if score >= self.thresholds['critical']:
            return "CRITICAL"
        elif score >= self.thresholds['high']:
            return "HIGH"
        elif score >= self.thresholds['medium']:
            return "MEDIUM"
        elif score >= self.thresholds['low']:
            return "LOW"
        else:
            return "INFO"
    
    def get_top_risks(self, n: int = 5) -> List[Tuple[str, float]]:
        return sorted(self.asset_scores.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def get_risk_trend(self) -> Dict:
        if len(self.score_history) < 2:
            return {'trend': 'stable', 'change': 0.0}
        
        recent = self.score_history[-5:]
        if len(recent) < 2:
            return {'trend': 'stable', 'change': 0.0}
        
        first = recent[0][1]
        last = recent[-1][1]
        change = ((last - first) / first) * 100 if first > 0 else 0
        
        if change > 10:
            trend = 'increasing'
        elif change < -10:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change': round(change, 1),
            'current': round(self.overall_score, 2)
        }


# ==================== LAYER 6: DECISION ENGINE ====================

class DecisionEngine:
    """AI-powered decision making"""
    
    def __init__(self, rag_system=None, llm_reasoner=None, attack_graph=None):
        self.rag = rag_system
        self.llm = llm_reasoner
        self.attack_graph = attack_graph
        self.decisions: List[Dict] = []
    
    def analyze(self, events: List[SecurityEvent], attack_graph: AttackGraph):
        if not events:
            return
        
        context = self._build_context(events, attack_graph)
        
        if self.rag and hasattr(self.rag, 'search'):
            try:
                similar = self.rag.search(context['summary'], k=3)
                context['similar_patterns'] = similar
            except Exception as e:
                logger.error(f"RAG search error: {e}")
        
        recommendations = self._generate_recommendations(context)
        
        decision = {
            'timestamp': datetime.utcnow().isoformat(),
            'context': context,
            'recommendations': recommendations,
            'event_count': len(events)
        }
        self.decisions.append(decision)
        
        return decision
    
    def _build_context(self, events: List[SecurityEvent], attack_graph: AttackGraph) -> Dict:
        asset_events = defaultdict(list)
        for event in events:
            asset_events[event.asset].append(event)
        
        total_events = len(events)
        unique_types = len(set(e.event_type for e in events))
        avg_severity = sum(e.severity for e in events) / max(total_events, 1)
        critical_paths = attack_graph.get_critical_paths()
        
        return {
            'summary': f"Analysis of {total_events} events across {len(asset_events)} assets",
            'total_events': total_events,
            'unique_event_types': unique_types,
            'avg_severity': round(avg_severity, 2),
            'assets': list(asset_events.keys()),
            'critical_paths': critical_paths[:3],
            'top_events': sorted(events, key=lambda x: x.severity, reverse=True)[:5]
        }
    
    def _generate_recommendations(self, context: Dict) -> List[Dict]:
        recommendations = []
        
        if context['avg_severity'] > 8:
            recommendations.append({
                'type': 'immediate_action',
                'priority': 'CRITICAL',
                'action': 'ISOLATE_ASSETS',
                'reason': 'Critical severity level detected',
                'assets': context['assets']
            })
        
        if context['unique_event_types'] > 5:
            recommendations.append({
                'type': 'comprehensive_scan',
                'priority': 'HIGH',
                'action': 'RUN_FULL_VULNERABILITY_SCAN',
                'reason': 'Multiple attack vectors detected',
                'assets': context['assets']
            })
        
        if len(context['critical_paths']) > 0:
            recommendations.append({
                'type': 'path_analysis',
                'priority': 'HIGH',
                'action': 'BLOCK_ATTACK_PATHS',
                'reason': 'Active attack chains detected',
                'paths': context['critical_paths']
            })
        
        return recommendations
    
    def predict_next_attack(self, events: List[SecurityEvent]) -> Dict:
        if not events:
            return {}
        
        event_types = [e.event_type for e in events[-10:]]
        
        chains = {
            (EventType.PORT_SCAN, EventType.SERVICE_DETECTION): 
                {'next': EventType.VULNERABILITY_SCAN, 'confidence': 0.7},
            (EventType.SQL_INJECTION_POTENTIAL, EventType.SQL_INJECTION_CONFIRMED):
                {'next': EventType.DATABASE_SCHEMA_DISCOVERED, 'confidence': 0.9},
            (EventType.CREDENTIAL_COMPROMISED,):
                {'next': EventType.REMOTE_SHELL_ESTABLISHED, 'confidence': 0.8},
            (EventType.WPA_HANDSHAKE_CAPTURED,):
                {'next': EventType.WPA_CRACKED, 'confidence': 0.6},
        }
        
        for pattern, prediction in chains.items():
            if all(et in event_types for et in pattern):
                return {
                    'predicted_event': prediction['next'].value if hasattr(prediction['next'], 'value') else prediction['next'],
                    'confidence': prediction['confidence'],
                    'based_on': [e.value for e in pattern]
                }
        
        return {}


# ==================== LAYER 7: INTELLIGENCE MEMORY ====================

class IntelligenceMemory:
    """Learning layer - stores and retrieves attack patterns"""
    
    def __init__(self, vector_store=None):
        self.vector_store = vector_store
        self.patterns: List[Dict] = []
        self.success_rates: Dict[str, float] = {}
        self.pattern_counts: Dict[str, int] = defaultdict(int)
    
    def store_pattern(self, attack_path: List[str], success: bool = True, context: Dict = None):
        pattern_key = "->".join(attack_path)
        
        pattern = {
            'pattern': pattern_key,
            'path': attack_path,
            'success': success,
            'context': context or {},
            'timestamp': datetime.utcnow().isoformat(),
            'count': self.pattern_counts[pattern_key] + 1
        }
        
        self.patterns.append(pattern)
        self.pattern_counts[pattern_key] += 1
        
        total = self.pattern_counts[pattern_key]
        success_count = sum(1 for p in self.patterns if p['pattern'] == pattern_key and p['success'])
        self.success_rates[pattern_key] = success_count / total if total > 0 else 0.5
    
    def get_similar_patterns(self, attack_path: List[str], k: int = 3) -> List[Dict]:
        pattern_key = "->".join(attack_path)
        similar = [p for p in self.patterns if p['pattern'] == pattern_key]
        similar.sort(key=lambda x: x['timestamp'], reverse=True)
        return similar[:k]
    
    def get_success_probability(self, attack_path: List[str]) -> float:
        pattern_key = "->".join(attack_path)
        return self.success_rates.get(pattern_key, 0.5)
    
    def get_most_successful_paths(self, n: int = 5) -> List[Dict]:
        successes = [(k, v) for k, v in self.success_rates.items()]
        successes.sort(key=lambda x: x[1], reverse=True)
        
        result = []
        for pattern, rate in successes[:n]:
            result.append({
                'pattern': pattern,
                'success_rate': rate,
                'occurrences': self.pattern_counts[pattern]
            })
        
        return result
    
    def get_learning_stats(self) -> Dict:
        return {
            'total_patterns': len(self.patterns),
            'unique_patterns': len(self.pattern_counts),
            'avg_success_rate': sum(self.success_rates.values()) / max(len(self.success_rates), 1) if self.success_rates else 0,
            'most_common': sorted(self.pattern_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }


# ==================== FACTORY: COMPLETE SYSTEM BUILDER ====================

class CorrelationSystemFactory:
    """Factory to build complete correlation system"""
    
    @classmethod
    def create_complete_system(cls, rag_system=None, llm_reasoner=None, vector_store=None):
        """Create complete correlation system with all components"""
        
        normalizer = ToolResultNormalizer()
        event_bus = EventBus()
        attack_graph = AttackGraph()
        risk_engine = RiskEngine()
        decision_engine = DecisionEngine(rag_system, llm_reasoner, attack_graph)
        correlation_engine = CorrelationEngine(attack_graph, risk_engine, decision_engine)
        intelligence_memory = IntelligenceMemory(vector_store)
        
        event_bus.subscribe(correlation_engine)
        
        if decision_engine:
            event_bus.subscribe(decision_engine, [
                EventType.SQL_INJECTION_CONFIRMED,
                EventType.REMOTE_SHELL_ESTABLISHED,
                EventType.CREDENTIAL_COMPROMISED
            ])
        
        return {
            'normalizer': normalizer,
            'event_bus': event_bus,
            'correlation_engine': correlation_engine,
            'attack_graph': attack_graph,
            'risk_engine': risk_engine,
            'decision_engine': decision_engine,
            'intelligence_memory': intelligence_memory
        }


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    system = CorrelationSystemFactory.create_complete_system()
    
    print("=" * 60)
    print(" 🧠 CYBERSEC LAB - CORRELATION ENGINE v1.0".center(60))
    print("=" * 60)
    
    normalizer = system['normalizer']
    event_bus = system['event_bus']
    
    nmap_result = {
        'ports': [22, 80, 443],
        'services': [
            {'name': 'ssh', 'port': 22, 'version': 'OpenSSH 7.9'},
            {'name': 'http', 'port': 80, 'version': 'Apache 2.4.49'}
        ],
        'os': 'Linux 4.15',
        'vulnerabilities': [
            {'name': 'SQL Injection Potential', 'severity': 'HIGH', 'port': 80}
        ]
    }
    
    events = normalizer.normalize_nmap(nmap_result, '192.168.1.100')
    event_bus.publish_many(events)
    
    sqlmap_result = {
        'success': True,
        'databases': ['information_schema', 'mysql', 'users_db']
    }
    
    events = normalizer.normalize_sqlmap(sqlmap_result, '192.168.1.100/products.php?id=1')
    event_bus.publish_many(events)
    
    hydra_result = {
        'credentials': [
            {'username': 'admin', 'password': 'password123'}
        ]
    }
    
    events = normalizer.normalize_hydra(hydra_result, '192.168.1.100')
    event_bus.publish_many(events)
    
    time.sleep(2)
    
    print(f"\n📊 Risk Score: {system['risk_engine'].overall_score:.2f} - {system['risk_engine'].get_risk_level()}")
    print(f"\n🌐 Attack Graph: {system['attack_graph'].graph_stats}")
    print(f"\n📈 Event Bus Stats: {system['event_bus'].get_stats()}")
    
    event_bus.stop()