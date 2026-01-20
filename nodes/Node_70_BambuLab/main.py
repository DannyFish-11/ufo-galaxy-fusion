#!/usr/bin/env python3
"""
Node 70: Bambu Lab 3D 打印机控制节点
主入口文件
"""

import asyncio
import logging
from enhanced_bambu_controller import EnhancedBambuController

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    """主函数"""
    logger.info("启动 Node 70: Bambu Lab 3D 打印机控制节点")
    
    # 创建控制器实例
    controller = EnhancedBambuController()
    
    try:
        # 启动控制器
        await controller.start()
        
        # 保持运行
        logger.info("Node 70 运行中，按 Ctrl+C 停止")
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        logger.info("收到停止信号")
    except Exception as e:
        logger.error(f"运行错误: {e}", exc_info=True)
    finally:
        # 清理资源
        await controller.stop()
        logger.info("Node 70 已停止")

if __name__ == "__main__":
    asyncio.run(main())
