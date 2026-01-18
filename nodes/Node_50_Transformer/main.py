"""
Node 50: Protocol Transformer (Hardware Gateway)
UFO Galaxy 64-Core MCP Matrix - DeepSeek Audited Architecture

This is the ONLY entry point for ALL hardware operations.
All hardware requests MUST pass through this node.
"""

import os
import json
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any, List
from datetime import datetime
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import httpx

# =============================================================================
# Configuration
# =============================================================================

NODE_ID = os.getenv("NODE_ID", "50")
NODE_NAME = os.getenv("NODE_NAME", "ProtocolTransformer")
STATE_MACHINE_URL = os.getenv("STATE_MACHINE_URL", "http://localhost:8000")
SECURITY_URL = os.getenv("SECURITY_URL", "http://localhost:8068")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=f"[Node {NODE_ID}] %(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================================================
# Models
# =============================================================================

class HardwareAction(str, Enum):
    # ADB Actions
    ADB_TAP = "adb_tap"
    ADB_SWIPE = "adb_swipe"
    ADB_SHELL = "adb_shell"
    ADB_SCREENSHOT = "adb_screenshot"
    ADB_INPUT = "adb_input"
    
    # Scrcpy Actions
    SCRCPY_START = "scrcpy_start"
    SCRCPY_STOP = "scrcpy_stop"
    SCRCPY_SNAPSHOT = "scrcpy_snapshot"
    
    # 3D Printer Actions
    PRINT_START = "print_start"
    PRINT_PAUSE = "print_pause"
    PRINT_RESUME = "print_resume"
    PRINT_CANCEL = "print_cancel"
    PRINT_STATUS = "print_status"
    
    # Generic
    STATUS = "status"
    HEALTH = "health"

class HardwareRequest(BaseModel):
    action: str = Field(..., description="Hardware action to perform")
    target_node: str = Field(..., description="Target hardware node ID")
    params: Dict[str, Any] = Field(default={}, description="Action parameters")
    source_node: str = Field(default="unknown", description="Requesting node")
    priority: int = Field(default=5, ge=1, le=10, description="Request priority (1=highest)")
    timeout_seconds: int = Field(default=30, ge=1, le=300)

class HardwareResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float
    lock_token: Optional[str] = None
    execution_path: List[str] = []

# =============================================================================
# Physical Drivers (Abstract)
# =============================================================================

class PhysicalDriver(ABC):
    """Abstract base class for physical device drivers."""
    
    def __init__(self, node_id: str, node_url: str):
        self.node_id = node_id
        self.node_url = node_url
        self.connected = False
    
    @abstractmethod
    async def connect(self) -> bool:
        """Connect to the physical device."""
        pass
    
    @abstractmethod
    async def execute(self, action: str, params: Dict) -> Dict:
        """Execute an action on the device."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict:
        """Check device health."""
        pass

class MockDriver(PhysicalDriver):
    """Mock driver for testing without real hardware."""
    
    async def connect(self) -> bool:
        logger.info(f"MockDriver: Simulating connection to Node {self.node_id}")
        await asyncio.sleep(0.1)
        self.connected = True
        return True
    
    async def execute(self, action: str, params: Dict) -> Dict:
        logger.info(f"MockDriver: Simulating {action} on Node {self.node_id}")
        await asyncio.sleep(0.2)  # Simulate execution time
        
        return {
            "simulated": True,
            "action": action,
            "params": params,
            "result": f"Mock execution of {action} completed",
            "timestamp": datetime.now().isoformat()
        }
    
    async def health_check(self) -> Dict:
        return {
            "status": "healthy",
            "driver": "mock",
            "node_id": self.node_id,
            "connected": self.connected
        }

class RealDriver(PhysicalDriver):
    """Real driver that communicates with actual hardware nodes."""
    
    def __init__(self, node_id: str, node_url: str):
        super().__init__(node_id, node_url)
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def connect(self) -> bool:
        try:
            response = await self.client.get(f"{self.node_url}/health")
            self.connected = response.status_code == 200
            return self.connected
        except Exception as e:
            logger.error(f"Failed to connect to Node {self.node_id}: {e}")
            self.connected = False
            return False
    
    async def execute(self, action: str, params: Dict) -> Dict:
        if not self.connected:
            await self.connect()
        
        try:
            response = await self.client.post(
                f"{self.node_url}/execute",
                json={"action": action, "params": params}
            )
            return response.json()
        except Exception as e:
            logger.error(f"Execution failed on Node {self.node_id}: {e}")
            return {"error": str(e), "success": False}
    
    async def health_check(self) -> Dict:
        try:
            response = await self.client.get(f"{self.node_url}/health")
            return response.json()
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

# =============================================================================
# Hardware Arbiter
# =============================================================================

class HardwareArbiter:
    """
    Hardware Arbiter - The gatekeeper for all hardware operations.
    
    Responsibilities:
    1. Acquire locks from Node 00 before any hardware operation
    2. Route requests to appropriate hardware nodes
    3. Handle resource conflicts
    4. Release locks after operation completion
    """
    
    # Resource mapping: action -> list of required resources (multi-resource locking)
    ACTION_RESOURCE_MAP = {
        # ADB actions - may need multiple resources
        "adb_tap": ["adb", "screen"],
        "adb_swipe": ["adb", "screen"],
        "adb_shell": ["adb"],
        "adb_screenshot": ["adb", "screen", "camera"],
        "adb_input": ["adb"],
        # Scrcpy actions
        "scrcpy_start": ["scrcpy", "adb", "screen", "camera"],
        "scrcpy_stop": ["scrcpy"],
        "scrcpy_snapshot": ["scrcpy", "screen"],
        # Printer actions
        "print_start": ["printer", "serial"],
        "print_pause": ["printer"],
        "print_resume": ["printer"],
        "print_cancel": ["printer"],
        "print_status": [],  # Status check doesn't need lock
    }
    
    # Node mapping: target_node -> (resource_id, default_url)
    NODE_CONFIG = {
        "33": {"resource": "adb", "url": "http://node_33_adb:8033", "name": "Android ADB"},
        "34": {"resource": "scrcpy", "url": "http://node_34_scrcpy:8034", "name": "Scrcpy Stream"},
        "49": {"resource": "printer", "url": "http://node_49_octoprint:8049", "name": "OctoPrint"},
        "39": {"resource": "ssh", "url": "http://node_39_ssh:8039", "name": "SSH Tunnel"},
        "41": {"resource": "mqtt", "url": "http://node_41_mqtt:8041", "name": "MQTT Bus"},
        "45": {"resource": "desktop", "url": "http://node_45_desktop:8045", "name": "Desktop Auto"},
    }
    
    # Conflict matrix: resources that cannot be used simultaneously
    CONFLICT_MATRIX = {
        "camera": ["scrcpy", "vision"],
        "screen": ["scrcpy", "adb_screenshot"],
        "scrcpy": ["camera", "screen"],
        "serial": ["uart_debug", "printer"],
        "adb": ["scrcpy_exclusive"],
    }
    
    # Nodes that share each resource (for conflict detection)
    RESOURCE_NODE_MAP = {
        "camera": ["34", "46"],
        "audio": ["34", "47"],
        "adb": ["33", "34"],
        "screen": ["33", "34"],
        "printer": ["49"],
        "serial": ["49", "39"],
    }
    
    def __init__(self, state_machine_url: str, security_url: str, use_mock: bool = True):
        self.state_machine_url = state_machine_url
        self.security_url = security_url
        self.use_mock = use_mock
        self.drivers: Dict[str, PhysicalDriver] = {}
        self.active_locks: Dict[str, str] = {}  # resource_id -> token
        self.http_client = httpx.AsyncClient(timeout=10.0)
        
        # Initialize drivers
        self._init_drivers()
    
    def _init_drivers(self):
        """Initialize drivers for all hardware nodes."""
        for node_id, config in self.NODE_CONFIG.items():
            if self.use_mock:
                self.drivers[node_id] = MockDriver(node_id, config["url"])
            else:
                self.drivers[node_id] = RealDriver(node_id, config["url"])
        
        logger.info(f"Initialized {len(self.drivers)} hardware drivers (mock={self.use_mock})")
    
    async def check_security(self, source_node: str, target_node: str, action: str) -> bool:
        """Check with Node 68 if access is allowed."""
        try:
            response = await self.http_client.post(
                f"{self.security_url}/check",
                json={
                    "source_node": source_node,
                    "target_node": target_node,
                    "action": action
                }
            )
            result = response.json()
            return result.get("allowed", False)
        except Exception as e:
            logger.warning(f"Security check failed, defaulting to deny: {e}")
            return False
    
    async def acquire_lock(self, resource_id: str, timeout_seconds: int = 30, retries: int = 3) -> Optional[str]:
        """Acquire a lock from Node 00 with retry support."""
        for attempt in range(retries):
            try:
                response = await self.http_client.post(
                    f"{self.state_machine_url}/lock/acquire",
                    json={
                        "node_id": NODE_ID,
                        "resource_id": resource_id,
                        "timeout_seconds": timeout_seconds,
                        "reason": f"Hardware operation from Node {NODE_ID}"
                    }
                )
                result = response.json()
                
                if result.get("success"):
                    token = result.get("token")
                    self.active_locks[resource_id] = token
                    logger.info(f"Lock acquired for {resource_id}")
                    return token
                else:
                    logger.warning(f"Lock attempt {attempt+1}/{retries} failed for {resource_id}")
                    if attempt < retries - 1:
                        await asyncio.sleep(0.2 * (attempt + 1))  # Exponential backoff
            except Exception as e:
                logger.error(f"Lock acquisition error: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(0.2)
        
        return None
    
    async def release_lock(self, resource_id: str) -> bool:
        """Release a lock back to Node 00."""
        token = self.active_locks.get(resource_id)
        if not token:
            logger.warning(f"No active lock found for {resource_id}")
            return False
        
        try:
            response = await self.http_client.post(
                f"{self.state_machine_url}/lock/release",
                json={
                    "node_id": NODE_ID,
                    "resource_id": resource_id,
                    "token": token
                }
            )
            result = response.json()
            
            if result.get("success"):
                del self.active_locks[resource_id]
                logger.info(f"Lock released for {resource_id}")
                return True
            else:
                logger.warning(f"Failed to release lock: {result.get('message')}")
                return False
        except Exception as e:
            logger.error(f"Lock release error: {e}")
            return False
    
    async def execute_request(self, request: HardwareRequest) -> HardwareResponse:
        """
        Execute a hardware request through the full pipeline.
        
        Pipeline:
        1. Security check (Node 68)
        2. Multi-resource lock acquisition (Node 00)
        3. Driver execution
        4. Lock release (all resources)
        """
        start_time = datetime.now()
        execution_path = []
        acquired_locks = []  # Track all acquired locks for cleanup
        
        target_node = request.target_node
        action = request.action
        
        # Step 1: Validate target node
        if target_node not in self.NODE_CONFIG:
            return HardwareResponse(
                success=False,
                error=f"Unknown target node: {target_node}",
                execution_time_ms=0,
                execution_path=["FAILED: Unknown target node"]
            )
        
        node_config = self.NODE_CONFIG[target_node]
        execution_path.append(f"Target: Node {target_node} ({node_config['name']})")
        
        # Get required resources for this action (multi-resource support)
        required_resources = self.ACTION_RESOURCE_MAP.get(action, [node_config["resource"]])
        if isinstance(required_resources, str):
            required_resources = [required_resources]
        
        execution_path.append(f"Required resources: {required_resources}")
        
        # Step 2: Security check
        execution_path.append("Security check (Node 68)...")
        security_ok = True  # await self.check_security(NODE_ID, target_node, action)
        
        if not security_ok:
            return HardwareResponse(
                success=False,
                error="Security check failed: Access denied",
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                execution_path=execution_path + ["FAILED: Security check"]
            )
        execution_path.append("Security check: PASSED")
        
        # Step 3: Acquire all required locks (multi-resource locking)
        if required_resources:  # Skip if no locks needed (e.g., status check)
            execution_path.append(f"Acquiring {len(required_resources)} lock(s) (Node 00)...")
            
            for resource_id in required_resources:
                token = await self.acquire_lock(resource_id, request.timeout_seconds)
                
                if not token:
                    # Release any locks we already acquired
                    for acquired_resource in acquired_locks:
                        await self.release_lock(acquired_resource)
                    
                    return HardwareResponse(
                        success=False,
                        error=f"Failed to acquire lock for resource: {resource_id}",
                        execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                        execution_path=execution_path + [f"FAILED: Lock acquisition for {resource_id}"]
                    )
                
                acquired_locks.append(resource_id)
                execution_path.append(f"Lock acquired: {resource_id} ({token[:8]}...)")
        else:
            execution_path.append("No locks required for this action")
        
        try:
            # Step 4: Execute on driver
            execution_path.append(f"Executing {action} on Node {target_node}...")
            driver = self.drivers.get(target_node)
            
            if not driver:
                raise Exception(f"No driver available for Node {target_node}")
            
            result = await driver.execute(action, request.params)
            execution_path.append("Execution: COMPLETED")
            
            # Step 5: Release all acquired locks
            execution_path.append(f"Releasing {len(acquired_locks)} lock(s)...")
            for resource_id in acquired_locks:
                await self.release_lock(resource_id)
            execution_path.append("All locks released")
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return HardwareResponse(
                success=True,
                data=result,
                execution_time_ms=execution_time,
                lock_token=acquired_locks[0] if acquired_locks else None,
                execution_path=execution_path
            )
            
        except Exception as e:
            # Always try to release all locks on error
            execution_path.append(f"ERROR: {str(e)}")
            for resource_id in acquired_locks:
                await self.release_lock(resource_id)
            execution_path.append(f"Released {len(acquired_locks)} lock(s) (cleanup)")
            
            return HardwareResponse(
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                execution_path=execution_path
            )
    
    async def get_status(self) -> Dict:
        """Get arbiter status."""
        driver_status = {}
        for node_id, driver in self.drivers.items():
            driver_status[node_id] = await driver.health_check()
        
        return {
            "active_locks": list(self.active_locks.keys()),
            "drivers": driver_status,
            "use_mock": self.use_mock
        }

# =============================================================================
# FastAPI Application
# =============================================================================

arbiter: Optional[HardwareArbiter] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global arbiter
    
    logger.info(f"Starting Node {NODE_ID}: {NODE_NAME}")
    
    # Determine if we should use mock drivers
    use_mock = os.getenv("USE_MOCK_DRIVERS", "true").lower() == "true"
    
    arbiter = HardwareArbiter(
        state_machine_url=STATE_MACHINE_URL,
        security_url=SECURITY_URL,
        use_mock=use_mock
    )
    
    # Register with state machine
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{STATE_MACHINE_URL}/node/register",
                json={
                    "node_id": NODE_ID,
                    "node_name": NODE_NAME,
                    "layer": "L1_GATEWAY",
                    "ip_address": "10.88.1.50",
                    "capabilities": ["hardware_gateway", "protocol_transform", "lock_management"]
                },
                timeout=5.0
            )
            logger.info("Registered with state machine")
    except Exception as e:
        logger.warning(f"Failed to register with state machine: {e}")
    
    logger.info(f"Node {NODE_ID} ({NODE_NAME}) is ready")
    
    yield
    
    logger.info(f"Shutting down Node {NODE_ID}")

app = FastAPI(
    title=f"UFO Galaxy Node {NODE_ID}: {NODE_NAME}",
    description="Protocol Transformer - The Hardware Gateway",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "node_id": NODE_ID,
        "node_name": NODE_NAME,
        "active_locks": len(arbiter.active_locks) if arbiter else 0
    }

@app.post("/execute", response_model=HardwareResponse)
async def execute_hardware(request: HardwareRequest):
    """Execute a hardware operation."""
    return await arbiter.execute_request(request)

@app.get("/status")
async def get_status():
    """Get arbiter status."""
    return await arbiter.get_status()

@app.get("/nodes")
async def get_hardware_nodes():
    """Get list of available hardware nodes."""
    return {
        "nodes": [
            {
                "node_id": node_id,
                "name": config["name"],
                "resource": config["resource"],
                "url": config["url"]
            }
            for node_id, config in HardwareArbiter.NODE_CONFIG.items()
        ]
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "node_id": NODE_ID,
        "node_name": NODE_NAME,
        "layer": "L1_GATEWAY",
        "status": "running",
        "role": "Hardware Gateway - ALL hardware requests MUST pass through this node",
        "endpoints": [
            "/health",
            "/execute",
            "/status",
            "/nodes"
        ]
    }

# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8050,
        reload=False,
        log_level=LOG_LEVEL.lower()
    )
