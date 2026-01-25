#!/usr/bin/env python3
"""
UFO Galaxy Fusion - Unified Startup Script

统一启动脚本

这是融合系统的入口，负责：
1. 加载配置
2. 初始化拓扑
3. 启动统一编排引擎
4. 启动所有节点
5. 提供统一的 API 接口

作者: Manus AI
日期: 2026-01-25
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from fusion.topology_manager import TopologyManager
from fusion.unified_orchestrator import UnifiedOrchestrator, Task, TaskType, TaskPriority

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(PROJECT_ROOT / 'logs' / 'fusion.log', mode='a')
    ]
)

logger = logging.getLogger(__name__)


class FusionSystem:
    """
    融合系统
    
    统一的系统入口，管理整个融合系统的生命周期
    """
    
    def __init__(self, config_path: str):
        """
        初始化融合系统
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.topology_manager: TopologyManager = None
        self.orchestrator: UnifiedOrchestrator = None
        self.is_running = False
        
        logger.info("="*80)
        logger.info("🚀 UFO Galaxy Fusion System")
        logger.info("="*80)
    
    async def initialize(self):
        """初始化系统"""
        logger.info("📋 Initializing Fusion System...")
        
        # 1. 加载拓扑配置
        topology_config = self.config_path / "topology.json"
        if not topology_config.exists():
            raise FileNotFoundError(f"Topology config not found: {topology_config}")
        
        logger.info(f"📊 Loading topology from: {topology_config}")
        self.topology_manager = TopologyManager(str(topology_config))
        
        # 打印拓扑统计
        stats = self.topology_manager.get_topology_stats()
        logger.info(f"✅ Topology loaded:")
        logger.info(f"   - Total nodes: {stats['total_nodes']}")
        logger.info(f"   - Layers: {stats['layers']}")
        logger.info(f"   - Domains: {len(stats.get('domains', {}))}")
        
        # 2. 初始化统一编排引擎
        logger.info("🎯 Initializing UnifiedOrchestrator...")
        self.orchestrator = UnifiedOrchestrator(
            topology_manager=self.topology_manager,
            enable_predictive_routing=True,
            enable_adaptive_balancing=True
        )
        
        await self.orchestrator.start()
        
        logger.info("✅ Fusion System initialized successfully")
    
    async def start(self):
        """启动系统"""
        logger.info("🚀 Starting Fusion System...")
        
        await self.initialize()
        
        self.is_running = True
        
        logger.info("="*80)
        logger.info("✅ Fusion System is running!")
        logger.info("="*80)
        logger.info("")
        logger.info("📊 System Status:")
        logger.info(f"   - Topology nodes: {len(self.topology_manager.nodes)}")
        logger.info(f"   - Orchestrator: Active")
        logger.info(f"   - Predictive routing: Enabled")
        logger.info(f"   - Adaptive balancing: Enabled")
        logger.info("")
        logger.info("🎯 Ready to accept tasks!")
        logger.info("")
    
    async def stop(self):
        """停止系统"""
        logger.info("🛑 Stopping Fusion System...")
        
        self.is_running = False
        
        if self.orchestrator:
            await self.orchestrator.stop()
        
        logger.info("✅ Fusion System stopped")
    
    async def submit_task(
        self,
        description: str,
        task_type: TaskType,
        priority: TaskPriority = TaskPriority.NORMAL,
        **kwargs
    ) -> str:
        """
        提交任务
        
        Args:
            description: 任务描述
            task_type: 任务类型
            priority: 任务优先级
            **kwargs: 其他参数
        
        Returns:
            任务 ID
        """
        if not self.is_running:
            raise RuntimeError("Fusion System is not running")
        
        import uuid
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        task = Task(
            task_id=task_id,
            description=description,
            task_type=task_type,
            priority=priority,
            **kwargs
        )
        
        await self.orchestrator.submit_task(task)
        
        return task_id
    
    async def execute_task(self, task: Task) -> Dict:
        """
        执行任务
        
        Args:
            task: 任务对象
        
        Returns:
            执行结果
        """
        if not self.is_running:
            raise RuntimeError("Fusion System is not running")
        
        return await self.orchestrator.execute_task(task)
    
    def get_stats(self) -> Dict:
        """获取系统统计"""
        if not self.orchestrator:
            return {}
        
        return self.orchestrator.get_stats()


async def run_demo():
    """运行演示"""
    logger.info("🎬 Running Fusion System Demo...")
    logger.info("")
    
    # 初始化系统
    config_path = PROJECT_ROOT / "config"
    fusion = FusionSystem(config_path)
    
    try:
        # 启动系统
        await fusion.start()
        
        # 等待一下
        await asyncio.sleep(2)
        
        # 示例任务 1: 混合任务（跨层级）
        logger.info("="*80)
        logger.info("📝 Demo Task 1: Hybrid Task (Cross-Layer)")
        logger.info("="*80)
        
        task1 = Task(
            task_id="demo_task_1",
            description="Analyze image and extract text",
            task_type=TaskType.HYBRID,
            priority=TaskPriority.HIGH,
            required_capabilities=["vision", "ocr", "text_processing"],
            preferred_domain="vision"
        )
        
        logger.info(f"📤 Submitting task: {task1.description}")
        result1 = await fusion.execute_task(task1)
        
        logger.info(f"✅ Task completed!")
        logger.info(f"   - Execution path: {' -> '.join(task1.execution_path)}")
        logger.info(f"   - Latency: {result1.get('total_latency_ms', 0):.1f}ms")
        logger.info("")
        
        # 示例任务 2: 感知任务
        logger.info("="*80)
        logger.info("📝 Demo Task 2: Perception Task")
        logger.info("="*80)
        
        task2 = Task(
            task_id="demo_task_2",
            description="Capture camera image",
            task_type=TaskType.PERCEPTION,
            priority=TaskPriority.NORMAL,
            required_capabilities=["camera", "image_capture"],
            preferred_domain="vision"
        )
        
        logger.info(f"📤 Submitting task: {task2.description}")
        result2 = await fusion.execute_task(task2)
        
        logger.info(f"✅ Task completed!")
        logger.info(f"   - Execution path: {' -> '.join(task2.execution_path)}")
        logger.info(f"   - Latency: {result2.get('total_latency_ms', 0):.1f}ms")
        logger.info("")
        
        # 示例任务 3: 认知任务
        logger.info("="*80)
        logger.info("📝 Demo Task 3: Cognitive Task")
        logger.info("="*80)
        
        task3 = Task(
            task_id="demo_task_3",
            description="Analyze sentiment of text",
            task_type=TaskType.COGNITIVE,
            priority=TaskPriority.NORMAL,
            required_capabilities=["nlu", "sentiment_analysis"],
            preferred_domain="nlu"
        )
        
        logger.info(f"📤 Submitting task: {task3.description}")
        result3 = await fusion.execute_task(task3)
        
        logger.info(f"✅ Task completed!")
        logger.info(f"   - Execution path: {' -> '.join(task3.execution_path)}")
        logger.info(f"   - Latency: {result3.get('total_latency_ms', 0):.1f}ms")
        logger.info("")
        
        # 打印统计
        logger.info("="*80)
        logger.info("📊 System Statistics")
        logger.info("="*80)
        
        stats = fusion.get_stats()
        logger.info(f"   - Total tasks: {stats.get('total_tasks', 0)}")
        logger.info(f"   - Completed tasks: {stats.get('completed_tasks', 0)}")
        logger.info(f"   - Failed tasks: {stats.get('failed_tasks', 0)}")
        logger.info(f"   - Average latency: {stats.get('average_latency_ms', 0):.1f}ms")
        logger.info("")
        
        topology_stats = stats.get('topology_stats', {})
        logger.info(f"   - Topology nodes: {topology_stats.get('total_nodes', 0)}")
        logger.info(f"   - Average load: {topology_stats.get('average_load', 0):.2f}")
        logger.info(f"   - Max load: {topology_stats.get('max_load', 0):.2f}")
        logger.info("")
        
        logger.info("🎉 Demo completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}", exc_info=True)
    
    finally:
        # 停止系统
        await fusion.stop()


async def run_interactive():
    """运行交互模式"""
    logger.info("🎮 Running Fusion System in Interactive Mode...")
    logger.info("")
    
    # 初始化系统
    config_path = PROJECT_ROOT / "config"
    fusion = FusionSystem(config_path)
    
    try:
        # 启动系统
        await fusion.start()
        
        logger.info("="*80)
        logger.info("🎮 Interactive Mode")
        logger.info("="*80)
        logger.info("")
        logger.info("Commands:")
        logger.info("  - task <description>: Submit a task")
        logger.info("  - stats: Show system statistics")
        logger.info("  - quit: Exit")
        logger.info("")
        
        while fusion.is_running:
            try:
                # 读取用户输入
                user_input = input("fusion> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["quit", "exit", "q"]:
                    break
                
                elif user_input.lower() == "stats":
                    stats = fusion.get_stats()
                    logger.info("📊 System Statistics:")
                    logger.info(f"   - Total tasks: {stats.get('total_tasks', 0)}")
                    logger.info(f"   - Completed: {stats.get('completed_tasks', 0)}")
                    logger.info(f"   - Failed: {stats.get('failed_tasks', 0)}")
                    logger.info(f"   - Avg latency: {stats.get('average_latency_ms', 0):.1f}ms")
                
                elif user_input.lower().startswith("task "):
                    description = user_input[5:].strip()
                    
                    task = Task(
                        task_id=f"interactive_{int(asyncio.get_event_loop().time())}",
                        description=description,
                        task_type=TaskType.HYBRID,
                        priority=TaskPriority.NORMAL
                    )
                    
                    logger.info(f"📤 Executing task: {description}")
                    result = await fusion.execute_task(task)
                    logger.info(f"✅ Task completed! Path: {' -> '.join(task.execution_path)}")
                
                else:
                    logger.warning(f"⚠️  Unknown command: {user_input}")
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")
        
    finally:
        await fusion.stop()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="UFO Galaxy Fusion System")
    parser.add_argument(
        "--mode",
        choices=["demo", "interactive", "server"],
        default="demo",
        help="Run mode"
    )
    
    args = parser.parse_args()
    
    # 创建日志目录
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    
    try:
        if args.mode == "demo":
            asyncio.run(run_demo())
        elif args.mode == "interactive":
            asyncio.run(run_interactive())
        elif args.mode == "server":
            logger.info("🌐 Server mode not implemented yet")
    
    except KeyboardInterrupt:
        logger.info("\n🛑 Interrupted by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
