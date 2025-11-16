import uuid
from typing import Dict, List, Any
import logging

from src.adk_core import Task, TaskStatus # pyright: ignore[reportMissingImports]
from src.agents import Agent # pyright: ignore[reportMissingImports]

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """Execute multi-agent workflows"""
    
    def __init__(self):
        self.workflows: Dict[str, Dict] = {}
        self.execution_history: List[Dict] = []
        logger.info("Workflow Engine initialized")
    
    def define_workflow(self, workflow_id: str, name: str, steps: List[Dict]) -> Dict:
        """Define a workflow"""
        from datetime import datetime
        workflow = {
            "workflow_id": workflow_id,
            "name": name,
            "steps": steps,
            "created_at": datetime.now().isoformat()
        }
        self.workflows[workflow_id] = workflow
        logger.info(f"Workflow defined: {name}")
        return workflow
    
    def execute_workflow(self, workflow_id: str, agents: Dict[str, Agent]) -> Dict:
        """Execute a workflow"""
        from datetime import datetime
        
        if workflow_id not in self.workflows:
            return {"success": False, "error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        execution = {
            "workflow_id": workflow_id,
            "started_at": datetime.now().isoformat(),
            "steps": []
        }
        
        # Execute each step
        for step in workflow["steps"]:
            agent_id = step.get("agent_id")
            task_type = step.get("task_type")
            parameters = step.get("parameters", {})
            
            if agent_id not in agents:
                execution["steps"].append({
                    "agent_id": agent_id,
                    "status": "failed",
                    "error": "Agent not found"
                })
                continue
            
            agent = agents[agent_id]
            task = Task(
                task_id=str(uuid.uuid4()),
                task_type=task_type,
                status=TaskStatus.PENDING,
                parameters=parameters
            )
            
            result = agent.execute_task(task)
            
            execution["steps"].append({
                "agent_id": agent_id,
                "task_type": task_type,
                "status": "completed" if result.success else "failed",
                "result": result.result,
                "execution_time": result.execution_time
            })
        
        execution["completed_at"] = datetime.now().isoformat()
        self.execution_history.append(execution)
        
        return execution
    
    def get_stats(self) -> Dict:
        """Get workflow engine stats"""
        return {
            "workflows_defined": len(self.workflows),
            "workflows_executed": len(self.execution_history),
            "workflows": list(self.workflows.keys())
        }

class SystemOrchestrator:
    """Orchestrate entire system"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.workflow_engine = WorkflowEngine()
        logger.info("System Orchestrator initialized")
    
    def register_agent(self, agent: Agent) -> bool:
        """Register agent"""
        self.agents[agent.agent_id] = agent
        logger.info(f"Agent registered: {agent.name}")
        return True
    
    def get_system_report(self) -> Dict:
        """Get system report"""
        agents_status = [agent.get_status() for agent in self.agents.values()]
        
        return {
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "total_agents": len(self.agents),
            "agents": agents_status,
            "workflows": self.workflow_engine.get_stats()
        }