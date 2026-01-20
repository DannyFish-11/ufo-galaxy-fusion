#!/usr/bin/env python3
"""
Node 74: 51World 数字孪生推演节点
主入口文件
"""

import asyncio
import logging
from digital_twin_simulator import DigitalTwinSimulator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    """主函数"""
    logger.info("启动 Node 74: 51World 数字孪生推演节点")
    
    # 创建模拟器实例
    simulator = DigitalTwinSimulator()
    
    try:
        # 启动模拟器
        await simulator.start()
        
        # 保持运行
        logger.info("Node 74 运行中，按 Ctrl+C 停止")
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        logger.info("收到停止信号")
    except Exception as e:
        logger.error(f"运行错误: {e}", exc_info=True)
    finally:
        # 清理资源
        await simulator.stop()
        logger.info("Node 74 已停止")

if __name__ == "__main__":
    asyncio.run(main())
