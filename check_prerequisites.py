"""
UFO³ Galaxy - 前置环境检查脚本
================================

检查所有前置环境是否正确安装和配置

作者：Manus AI
日期：2026-01-23
"""

import os
import sys
import subprocess
import platform
from typing import Dict, List, Tuple

# ANSI 颜色代码
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

def print_header(text: str):
    """打印标题"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

def print_section(text: str):
    """打印章节"""
    print(f"\n{CYAN}{text}{RESET}")
    print(f"{CYAN}{'-'*80}{RESET}")

def check_command(command: str, args: List[str] = None) -> Tuple[bool, str]:
    """检查命令是否可用"""
    if args is None:
        args = ["--version"]
    
    try:
        result = subprocess.run(
            [command] + args,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # 提取版本信息
            output = result.stdout + result.stderr
            version = output.split('\n')[0] if output else "已安装"
            return True, version
        else:
            return False, ""
    except FileNotFoundError:
        return False, ""
    except Exception as e:
        return False, str(e)

def check_python() -> Dict:
    """检查 Python 环境"""
    result = {
        "name": "Python",
        "required": True,
        "installed": False,
        "version": "",
        "message": "",
        "fix": ""
    }
    
    # 检查 Python 版本
    version = sys.version.split()[0]
    major, minor = sys.version_info[:2]
    
    result["installed"] = True
    result["version"] = version
    
    if major >= 3 and minor >= 11:
        result["message"] = f"✅ Python {version} (满足要求: 3.11+)"
    else:
        result["message"] = f"⚠️  Python {version} (推荐升级到 3.11+)"
        result["fix"] = "访问 https://www.python.org/downloads/ 下载最新版本"
    
    return result

def check_pip() -> Dict:
    """检查 pip"""
    result = {
        "name": "pip",
        "required": True,
        "installed": False,
        "version": "",
        "message": "",
        "fix": ""
    }
    
    installed, version = check_command("pip", ["--version"])
    
    if installed:
        result["installed"] = True
        result["version"] = version
        result["message"] = f"✅ {version}"
    else:
        result["message"] = "❌ pip 未安装"
        result["fix"] = "Python 安装时应该已包含 pip，请重新安装 Python"
    
    return result

def check_git() -> Dict:
    """检查 Git"""
    result = {
        "name": "Git",
        "required": True,
        "installed": False,
        "version": "",
        "message": "",
        "fix": ""
    }
    
    installed, version = check_command("git", ["--version"])
    
    if installed:
        result["installed"] = True
        result["version"] = version
        result["message"] = f"✅ {version}"
    else:
        result["message"] = "❌ Git 未安装"
        result["fix"] = "访问 https://git-scm.com/download/win 下载并安装"
    
    return result

def check_tailscale() -> Dict:
    """检查 Tailscale"""
    result = {
        "name": "Tailscale",
        "required": False,
        "installed": False,
        "version": "",
        "message": "",
        "fix": ""
    }
    
    installed, version = check_command("tailscale", ["version"])
    
    if installed:
        result["installed"] = True
        result["version"] = version
        result["message"] = f"✅ {version}"
        
        # 检查 Tailscale IP
        try:
            ip_result = subprocess.run(
                ["tailscale", "ip", "-4"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if ip_result.returncode == 0:
                ip = ip_result.stdout.strip()
                result["message"] += f" (IP: {ip})"
            else:
                result["message"] += " (未登录)"
        except:
            pass
    else:
        result["message"] = "⚠️  Tailscale 未安装（跨设备通信需要）"
        result["fix"] = "访问 https://tailscale.com/download 下载并安装"
    
    return result

def check_adb() -> Dict:
    """检查 ADB"""
    result = {
        "name": "ADB",
        "required": False,
        "installed": False,
        "version": "",
        "message": "",
        "fix": ""
    }
    
    installed, version = check_command("adb", ["--version"])
    
    if installed:
        result["installed"] = True
        result["version"] = version
        result["message"] = f"✅ {version}"
    else:
        result["message"] = "⚠️  ADB 未安装（安卓设备控制需要）"
        result["fix"] = "访问 https://developer.android.com/studio/releases/platform-tools 下载并安装"
    
    return result

def check_python_packages() -> Dict:
    """检查 Python 包"""
    result = {
        "name": "Python 包",
        "required": True,
        "installed": False,
        "packages": {},
        "message": "",
        "fix": ""
    }
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "httpx",
        "pydantic"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            result["packages"][package] = "✅"
        except ImportError:
            result["packages"][package] = "❌"
            missing_packages.append(package)
    
    if not missing_packages:
        result["installed"] = True
        result["message"] = "✅ 所有核心包已安装"
    else:
        result["message"] = f"❌ 缺少 {len(missing_packages)} 个核心包"
        result["fix"] = f"运行: pip install {' '.join(missing_packages)}"
    
    return result

def main():
    """主函数"""
    print_header("UFO³ Galaxy - 前置环境检查")
    
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"架构: {platform.machine()}")
    
    # 检查所有环境
    checks = [
        check_python(),
        check_pip(),
        check_git(),
        check_tailscale(),
        check_adb(),
        check_python_packages()
    ]
    
    # 统计
    required_count = sum(1 for c in checks if c["required"])
    required_installed = sum(1 for c in checks if c["required"] and c["installed"])
    optional_installed = sum(1 for c in checks if not c["required"] and c["installed"])
    
    # 显示结果
    print_section("检查结果")
    
    for check in checks:
        status = "必需" if check["required"] else "可选"
        print(f"\n[{status}] {check['name']}")
        print(f"  {check['message']}")
        
        if check.get("packages"):
            for pkg, status in check["packages"].items():
                print(f"    - {pkg}: {status}")
        
        if check["fix"]:
            print(f"  💡 修复: {check['fix']}")
    
    # 总结
    print_section("总结")
    
    print(f"必需环境: {required_installed}/{required_count} 已安装")
    print(f"可选环境: {optional_installed}/{len(checks) - required_count} 已安装")
    
    if required_installed == required_count:
        print(f"\n{GREEN}✅ 所有必需环境已就绪，可以开始部署！{RESET}")
        print(f"\n下一步:")
        print(f"  1. 运行 deploy.bat 进行一键部署")
        print(f"  2. 运行 start_system.bat 启动系统")
        return 0
    else:
        print(f"\n{RED}❌ 还有 {required_count - required_installed} 个必需环境未安装{RESET}")
        print(f"\n请按照上方的修复建议安装缺失的环境")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        print()
        input("按 Enter 键退出...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}检查已取消{RESET}")
        sys.exit(1)
