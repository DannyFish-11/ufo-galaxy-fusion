#!/usr/bin/env python3
"""
UFO³ Galaxy 环境检查脚本
检查所有必需的依赖和配置是否就绪

版本: 1.0
日期: 2026-01-22
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def print_header(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python():
    """检查 Python 版本"""
    print("\n[1/8] 检查 Python 版本...")
    version = sys.version_info
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"  ⚠️  警告: 建议使用 Python 3.11 或更高版本")
        return False
    return True

def check_command(command, name):
    """检查命令是否可用"""
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # 提取版本信息的第一行
            version_line = result.stdout.split('\n')[0] if result.stdout else result.stderr.split('\n')[0]
            print(f"  ✓ {name}: {version_line}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print(f"  ✗ {name}: 未安装")
    return False

def check_adb():
    """检查 ADB"""
    print("\n[2/8] 检查 ADB (Android Debug Bridge)...")
    if check_command("adb", "ADB"):
        # 检查连接的设备
        try:
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            devices = [line for line in result.stdout.split('\n') if '\tdevice' in line]
            if devices:
                print(f"  ✓ 检测到 {len(devices)} 台连接的设备:")
                for device in devices:
                    print(f"    - {device.split()[0]}")
            else:
                print(f"  ⚠️  未检测到连接的设备")
        except Exception as e:
            print(f"  ⚠️  无法检查设备: {e}")
        return True
    return False

def check_git():
    """检查 Git"""
    print("\n[3/8] 检查 Git...")
    return check_command("git", "Git")

def check_tailscale():
    """检查 Tailscale"""
    print("\n[4/8] 检查 Tailscale...")
    try:
        result = subprocess.run(
            ["tailscale", "status"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"  ✓ Tailscale: 运行中")
            # 提取 Tailscale IP
            lines = result.stdout.split('\n')
            for line in lines:
                if '100.' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        print(f"    本机 IP: {parts[0]}")
                        break
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print(f"  ✗ Tailscale: 未运行")
    return False

def check_python_packages():
    """检查 Python 包"""
    print("\n[5/8] 检查 Python 包...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "httpx",
        "aiohttp",
    ]
    
    optional_packages = [
        "qiskit",
        "qiskit_aer",
        "qiskit_ibm_runtime",
    ]
    
    all_ok = True
    
    print("  必需包:")
    for package in required_packages:
        try:
            __import__(package)
            print(f"    ✓ {package}")
        except ImportError:
            print(f"    ✗ {package}")
            all_ok = False
    
    print("  可选包:")
    for package in optional_packages:
        try:
            __import__(package)
            print(f"    ✓ {package}")
        except ImportError:
            print(f"    ⚠️  {package} (未安装，量子计算功能将不可用)")
    
    return all_ok

def check_env_file():
    """检查 .env 文件"""
    print("\n[6/8] 检查配置文件...")
    
    env_file = Path(".env")
    if env_file.exists():
        print(f"  ✓ .env 文件存在")
        
        # 读取并检查关键配置
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "TAILSCALE_ENABLED" in content:
            print(f"    ✓ Tailscale 配置已设置")
        else:
            print(f"    ⚠️  Tailscale 配置未设置")
        
        return True
    else:
        print(f"  ⚠️  .env 文件不存在，将使用默认配置")
        return False

def check_project_structure():
    """检查项目结构"""
    print("\n[7/8] 检查项目结构...")
    
    required_dirs = [
        "nodes",
        "galaxy_gateway",
        "enhancements",
    ]
    
    all_ok = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ (缺失)")
            all_ok = False
    
    return all_ok

def check_launcher():
    """检查启动器"""
    print("\n[8/8] 检查启动器...")
    
    launcher = Path("galaxy_launcher.py")
    if launcher.exists():
        print(f"  ✓ galaxy_launcher.py 存在")
        return True
    else:
        print(f"  ✗ galaxy_launcher.py 不存在")
        return False

def main():
    """主函数"""
    print_header("UFO³ Galaxy 环境检查")
    
    print(f"\n系统信息:")
    print(f"  操作系统: {platform.system()} {platform.release()}")
    print(f"  架构: {platform.machine()}")
    
    results = {
        "Python": check_python(),
        "ADB": check_adb(),
        "Git": check_git(),
        "Tailscale": check_tailscale(),
        "Python 包": check_python_packages(),
        "配置文件": check_env_file(),
        "项目结构": check_project_structure(),
        "启动器": check_launcher(),
    }
    
    print_header("检查结果汇总")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n通过: {passed}/{total}")
    print()
    
    for name, result in results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {name}")
    
    if passed == total:
        print("\n🎉 所有检查通过！您可以开始使用 UFO³ Galaxy 了。")
        print("\n启动命令:")
        if platform.system() == "Windows":
            print("  start_ufo3_galaxy.bat")
        else:
            print("  python3 galaxy_launcher.py --include-groups core extended")
        return 0
    else:
        print("\n⚠️  部分检查未通过，请根据上述提示解决问题。")
        print("\n常见问题:")
        if not results["Python 包"]:
            print("  - 安装 Python 包: pip install -r galaxy_gateway/requirements.txt")
        if not results["ADB"]:
            print("  - 安装 ADB: https://developer.android.com/studio/releases/platform-tools")
        if not results["Tailscale"]:
            print("  - 安装 Tailscale: https://tailscale.com/download")
        return 1

if __name__ == "__main__":
    sys.exit(main())
