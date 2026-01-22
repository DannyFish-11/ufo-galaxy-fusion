#!/usr/bin/env python3
"""
Academic Research Workflow
学术研究融合工作流

功能:
1. 一键触发：研究主题 → 完整报告
2. 自动化流程：搜索 → 保存 → 分析 → 报告
3. 进度跟踪和状态管理
"""

import os
import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
import httpx

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 节点配置
NODE_97_URL = os.getenv("NODE_97_URL", "http://localhost:8097")  # 学术搜索
NODE_104_URL = os.getenv("NODE_104_URL", "http://localhost:8104")  # AgentCPM
NODE_80_URL = os.getenv("NODE_80_URL", "http://localhost:8080")  # 记忆系统

class AcademicResearchWorkflow:
    """学术研究工作流"""
    
    def __init__(self):
        self.node_97_url = NODE_97_URL
        self.node_104_url = NODE_104_URL
        self.node_80_url = NODE_80_URL
    
    async def run_complete_research(
        self,
        topic: str,
        search_sources: List[str] = ["arxiv", "semantic_scholar"],
        max_papers: int = 20,
        research_depth: str = "deep"
    ) -> Dict:
        """运行完整的研究工作流"""
        
        workflow_id = f"research_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"开始研究工作流: {workflow_id}")
        logger.info(f"研究主题: {topic}")
        
        result = {
            "workflow_id": workflow_id,
            "topic": topic,
            "status": "running",
            "steps": []
        }
        
        try:
            # 步骤 1: 学术搜索（Node_97）
            logger.info("步骤 1/4: 搜索相关论文...")
            papers = await self._search_papers(topic, search_sources, max_papers)
            result["steps"].append({
                "step": 1,
                "name": "学术搜索",
                "status": "completed",
                "papers_found": len(papers)
            })
            logger.info(f"找到 {len(papers)} 篇相关论文")
            
            # 步骤 2: 保存到记忆系统（Node_80）
            logger.info("步骤 2/4: 保存论文到记忆系统...")
            saved_count = await self._save_papers_to_memory(papers)
            result["steps"].append({
                "step": 2,
                "name": "保存论文",
                "status": "completed",
                "papers_saved": saved_count
            })
            logger.info(f"保存了 {saved_count} 篇论文")
            
            # 步骤 3: 深度研究（Node_104）
            logger.info("步骤 3/4: 生成深度研究报告...")
            research_task = await self._generate_research_report(topic, research_depth)
            result["steps"].append({
                "step": 3,
                "name": "深度研究",
                "status": "pending",
                "task_id": research_task["task_id"]
            })
            logger.info(f"研究任务已创建: {research_task['task_id']}")
            
            # 等待研究完成
            logger.info("等待研究报告生成...")
            report = await self._wait_for_research_completion(research_task["task_id"])
            result["steps"][2]["status"] = "completed"
            result["steps"][2]["report_length"] = len(report.get("content", ""))
            
            # 步骤 4: 整理和输出
            logger.info("步骤 4/4: 整理研究成果...")
            summary = await self._create_research_summary(topic, papers, report)
            result["steps"].append({
                "step": 4,
                "name": "整理成果",
                "status": "completed"
            })
            
            result["status"] = "completed"
            result["summary"] = summary
            result["papers"] = papers[:5]  # 只返回前 5 篇
            result["report"] = report
            
            logger.info(f"研究工作流完成: {workflow_id}")
            return result
        
        except Exception as e:
            logger.error(f"研究工作流失败: {e}")
            result["status"] = "failed"
            result["error"] = str(e)
            return result
    
    async def _search_papers(
        self,
        topic: str,
        sources: List[str],
        max_results: int
    ) -> List[Dict]:
        """搜索论文"""
        all_papers = []
        
        for source in sources:
            try:
                url = f"{self.node_97_url}/search"
                data = {
                    "query": topic,
                    "source": source,
                    "max_results": max_results // len(sources),
                    "save_to_memos": True  # 自动保存
                }
                
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(url, json=data)
                    response.raise_for_status()
                
                result = response.json()
                papers = result.get("papers", [])
                all_papers.extend(papers)
                
                logger.info(f"从 {source} 找到 {len(papers)} 篇论文")
            
            except Exception as e:
                logger.error(f"搜索 {source} 失败: {e}")
        
        return all_papers
    
    async def _save_papers_to_memory(self, papers: List[Dict]) -> int:
        """保存论文到记忆系统"""
        saved_count = 0
        
        for paper in papers:
            try:
                url = f"{self.node_80_url}/academic/paper_note"
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(url, json=paper)
                    response.raise_for_status()
                
                saved_count += 1
            
            except Exception as e:
                logger.error(f"保存论文失败: {e}")
        
        return saved_count
    
    async def _generate_research_report(
        self,
        topic: str,
        depth: str
    ) -> Dict:
        """生成研究报告"""
        url = f"{self.node_104_url}/deep_research"
        data = {
            "topic": topic,
            "depth": depth,
            "output_format": "markdown",
            "save_to_memos": True
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
        
        return response.json()
    
    async def _wait_for_research_completion(
        self,
        task_id: str,
        max_wait: int = 600
    ) -> Dict:
        """等待研究完成"""
        url = f"{self.node_104_url}/task/{task_id}"
        
        for i in range(max_wait // 5):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                
                task_status = response.json()
                status = task_status.get("status")
                progress = task_status.get("progress", 0)
                
                logger.info(f"研究进度: {progress}%")
                
                if status == "completed":
                    result = task_status.get("result", {})
                    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    return {"content": content, "task_status": task_status}
                
                elif status == "failed":
                    error = task_status.get("error", "Unknown error")
                    raise Exception(f"研究失败: {error}")
                
                await asyncio.sleep(5)
            
            except Exception as e:
                logger.error(f"检查任务状态失败: {e}")
        
        raise Exception("研究超时")
    
    async def _create_research_summary(
        self,
        topic: str,
        papers: List[Dict],
        report: Dict
    ) -> Dict:
        """创建研究摘要"""
        return {
            "topic": topic,
            "papers_analyzed": len(papers),
            "report_length": len(report.get("content", "")),
            "sources": list(set([p.get("source") for p in papers])),
            "top_papers": [
                {
                    "title": p.get("title"),
                    "authors": p.get("authors", [])[:3],
                    "url": p.get("url")
                }
                for p in papers[:3]
            ],
            "completed_at": datetime.now().isoformat()
        }
    
    async def quick_search(self, topic: str, max_results: int = 10) -> Dict:
        """快速搜索（仅搜索和保存）"""
        logger.info(f"快速搜索: {topic}")
        
        papers = await self._search_papers(
            topic,
            ["arxiv", "semantic_scholar"],
            max_results
        )
        
        return {
            "topic": topic,
            "papers_found": len(papers),
            "papers": papers
        }
    
    async def get_research_status(self, workflow_id: str) -> Dict:
        """获取研究状态"""
        # 这里应该从数据库或缓存中获取状态
        # 简化版本直接返回示例
        return {
            "workflow_id": workflow_id,
            "status": "running",
            "progress": 75
        }

# CLI 接口
async def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python academic_research_workflow.py <研究主题>")
        print("示例: python academic_research_workflow.py '量子机器学习'")
        sys.exit(1)
    
    topic = sys.argv[1]
    
    workflow = AcademicResearchWorkflow()
    result = await workflow.run_complete_research(topic)
    
    print("\n" + "="*80)
    print(f"研究工作流: {result['workflow_id']}")
    print(f"主题: {result['topic']}")
    print(f"状态: {result['status']}")
    print("="*80)
    
    for step in result.get("steps", []):
        status_icon = "✅" if step["status"] == "completed" else "⏳"
        print(f"{status_icon} 步骤 {step['step']}: {step['name']} - {step['status']}")
    
    if result["status"] == "completed":
        summary = result.get("summary", {})
        print("\n" + "="*80)
        print("研究摘要")
        print("="*80)
        print(f"分析论文数: {summary.get('papers_analyzed')}")
        print(f"报告长度: {summary.get('report_length')} 字符")
        print(f"数据源: {', '.join(summary.get('sources', []))}")
        print(f"完成时间: {summary.get('completed_at')}")
        
        print("\n前 3 篇重要论文:")
        for i, paper in enumerate(summary.get("top_papers", []), 1):
            print(f"{i}. {paper['title']}")
            print(f"   作者: {', '.join(paper['authors'])}")
            print(f"   链接: {paper['url']}\n")
    
    else:
        print(f"\n错误: {result.get('error')}")

if __name__ == "__main__":
    asyncio.run(main())
