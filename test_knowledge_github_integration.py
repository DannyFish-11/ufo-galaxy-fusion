"""
集成测试：Node_105 + Node_106
================================

测试 Node_105 (Unified Knowledge Base) 和 Node_106 (GitHub Flow) 的集成功能

作者：Manus AI
日期：2026-01-22
"""

import asyncio
import httpx
import json

# ANSI 颜色代码
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

class IntegrationTester:
    """集成测试器"""
    
    def __init__(self):
        self.node_105_url = "http://localhost:8105"
        self.node_106_url = "http://localhost:8106"
        self.passed = 0
        self.failed = 0
    
    async def test_node_105_health(self):
        """测试 Node_105 健康检查"""
        print(f"\n{BLUE}[测试 1] Node_105 健康检查{RESET}")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.node_105_url}/health")
                response.raise_for_status()
                data = response.json()
                
                assert data["status"] == "healthy"
                assert data["node_id"] == "105"
                
                print(f"{GREEN}✅ 通过{RESET}")
                print(f"   - 状态: {data['status']}")
                print(f"   - 知识条目数: {data['knowledge_count']}")
                print(f"   - Mock 模式: {data['mock_mode']}")
                self.passed += 1
        except Exception as e:
            print(f"{RED}❌ 失败: {e}{RESET}")
            self.failed += 1
    
    async def test_node_106_health(self):
        """测试 Node_106 健康检查"""
        print(f"\n{BLUE}[测试 2] Node_106 健康检查{RESET}")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.node_106_url}/health")
                response.raise_for_status()
                data = response.json()
                
                assert data["status"] == "healthy"
                assert data["node_id"] == "106"
                
                print(f"{GREEN}✅ 通过{RESET}")
                print(f"   - 状态: {data['status']}")
                print(f"   - Mock 模式: {data['mock_mode']}")
                print(f"   - GitHub Mock: {data['github_mock']}")
                self.passed += 1
        except Exception as e:
            print(f"{RED}❌ 失败: {e}{RESET}")
            self.failed += 1
    
    async def test_add_text_knowledge(self):
        """测试添加文本知识"""
        print(f"\n{BLUE}[测试 3] 添加文本知识到 Node_105{RESET}")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.node_105_url}/add",
                    json={
                        "source_type": "text",
                        "content": "量子计算是一种利用量子力学原理进行计算的技术。",
                        "metadata": {"category": "quantum", "test": True}
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                assert data["success"] == True
                assert "entry_id" in data
                
                print(f"{GREEN}✅ 通过{RESET}")
                print(f"   - Entry ID: {data['entry_id']}")
                self.passed += 1
        except Exception as e:
            print(f"{RED}❌ 失败: {e}{RESET}")
            self.failed += 1
    
    async def test_search_knowledge(self):
        """测试搜索知识"""
        print(f"\n{BLUE}[测试 4] 搜索知识{RESET}")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.node_105_url}/search",
                    json={
                        "query": "量子计算",
                        "top_k": 5,
                        "search_type": "hybrid"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                assert data["success"] == True
                assert data["count"] >= 0
                
                print(f"{GREEN}✅ 通过{RESET}")
                print(f"   - 找到 {data['count']} 条结果")
                if data["results"]:
                    print(f"   - 第一条: {data['results'][0]['content'][:50]}...")
                self.passed += 1
        except Exception as e:
            print(f"{RED}❌ 失败: {e}{RESET}")
            self.failed += 1
    
    async def test_ask_knowledge(self):
        """测试 RAG 问答"""
        print(f"\n{BLUE}[测试 5] RAG 问答{RESET}")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.node_105_url}/ask",
                    json={
                        "question": "什么是量子计算？",
                        "top_k": 3
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                assert data["success"] == True
                assert "answer" in data
                assert "sources" in data
                
                print(f"{GREEN}✅ 通过{RESET}")
                print(f"   - 答案长度: {len(data['answer'])} 字符")
                print(f"   - 引用来源数: {len(data['sources'])}")
                self.passed += 1
        except Exception as e:
            print(f"{RED}❌ 失败: {e}{RESET}")
            self.failed += 1
    
    async def test_create_issue(self):
        """测试创建 GitHub Issue"""
        print(f"\n{BLUE}[测试 6] 创建 GitHub Issue{RESET}")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.node_106_url}/create_issue",
                    json={
                        "repo": "test/repo",
                        "title": "测试 Issue",
                        "body": "这是一个测试 Issue",
                        "labels": ["test"]
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                assert data["success"] == True
                assert "issue_number" in data
                
                print(f"{GREEN}✅ 通过{RESET}")
                print(f"   - Issue 编号: {data['issue_number']}")
                print(f"   - Issue URL: {data.get('issue_url', 'N/A')}")
                self.passed += 1
        except Exception as e:
            print(f"{RED}❌ 失败: {e}{RESET}")
            self.failed += 1
    
    async def test_generate_code(self):
        """测试代码生成"""
        print(f"\n{BLUE}[测试 7] 根据 Issue 生成代码{RESET}")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.node_106_url}/generate_code",
                    json={
                        "repo": "test/repo",
                        "issue_number": 1,
                        "branch_name": "feature/test"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                assert data["success"] == True
                assert "code" in data
                assert "branch" in data
                
                print(f"{GREEN}✅ 通过{RESET}")
                print(f"   - 分支名: {data['branch']}")
                print(f"   - 代码长度: {len(data['code'])} 字符")
                self.passed += 1
        except Exception as e:
            print(f"{RED}❌ 失败: {e}{RESET}")
            self.failed += 1
    
    async def test_review_pr(self):
        """测试 PR 审查"""
        print(f"\n{BLUE}[测试 8] 审查 Pull Request{RESET}")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.node_106_url}/review_pr",
                    json={
                        "repo": "test/repo",
                        "pr_number": 1
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                assert data["success"] == True
                assert "review_comments" in data
                
                print(f"{GREEN}✅ 通过{RESET}")
                print(f"   - PR 编号: {data['pr_number']}")
                print(f"   - 审查意见长度: {len(data['review_comments'])} 字符")
                self.passed += 1
        except Exception as e:
            print(f"{RED}❌ 失败: {e}{RESET}")
            self.failed += 1
    
    async def test_stats(self):
        """测试统计信息"""
        print(f"\n{BLUE}[测试 9] 获取 Node_105 统计信息{RESET}")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.node_105_url}/stats")
                response.raise_for_status()
                data = response.json()
                
                assert "total_entries" in data
                assert "source_types" in data
                
                print(f"{GREEN}✅ 通过{RESET}")
                print(f"   - 总条目数: {data['total_entries']}")
                print(f"   - 数据源类型: {data['source_types']}")
                self.passed += 1
        except Exception as e:
            print(f"{RED}❌ 失败: {e}{RESET}")
            self.failed += 1
    
    async def run_all_tests(self):
        """运行所有测试"""
        print(f"\n{'='*80}")
        print(f"{YELLOW}开始集成测试：Node_105 + Node_106{RESET}")
        print(f"{'='*80}")
        
        # 测试 Node_105
        await self.test_node_105_health()
        await self.test_add_text_knowledge()
        await self.test_search_knowledge()
        await self.test_ask_knowledge()
        await self.test_stats()
        
        # 测试 Node_106
        await self.test_node_106_health()
        await self.test_create_issue()
        await self.test_generate_code()
        await self.test_review_pr()
        
        # 总结
        print(f"\n{'='*80}")
        print(f"{YELLOW}测试总结{RESET}")
        print(f"{'='*80}")
        print(f"{GREEN}✅ 通过: {self.passed}{RESET}")
        print(f"{RED}❌ 失败: {self.failed}{RESET}")
        print(f"总计: {self.passed + self.failed}")
        print(f"成功率: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        print(f"{'='*80}\n")
        
        if self.failed == 0:
            print(f"{GREEN}🎉 所有测试通过！{RESET}")
        else:
            print(f"{YELLOW}⚠️ 部分测试失败，请检查节点是否正在运行。{RESET}")
            print(f"\n启动命令：")
            print(f"  Node_105: cd nodes/Node_105_UnifiedKnowledgeBase && python main.py")
            print(f"  Node_106: cd nodes/Node_106_GitHubFlow && python main.py")

async def main():
    """主函数"""
    tester = IntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
