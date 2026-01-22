# NVIDIA DGX Spark 规格和性能

## 核心规格

| 规格项 | 参数 |
|-------|------|
| **架构** | NVIDIA Grace Blackwell (GB10) |
| **GPU** | Blackwell Architecture |
| **CPU** | 20 核 ARM（10x Cortex-X925 + 10x Cortex-A725）|
| **Tensor Cores** | 第 5 代 |
| **AI 性能** | 最高 1 PFLOP FP4 |
| **统一内存** | 128 GB LPDDR5x（统一内存）|
| **内存带宽** | 273 GB/s |
| **存储** | 4 TB NVMe M.2（自加密）|
| **网络** | 10 GbE + ConnectX-7 NIC @ 200 Gbps |
| **功耗** | 240W（TDP 140W）|
| **尺寸** | 紧凑桌面形态 |

## 支持的 LLM

- **最大参数：** 200B（推理）
- **微调：** 最高 70B 参数
- **支持模型：** DeepSeek, Meta Llama, NVIDIA, Google, Qwen 等

## 预装软件

- NVIDIA AI 软件栈
- NVIDIA Isaac（机器人）
- NVIDIA Metropolis（智慧城市）
- NVIDIA Holoscan（医疗）

## 适用场景

1. **原型开发** - 开发、测试和验证 AI 模型
2. **模型微调** - 微调最高 70B 参数的模型
3. **推理** - 测试和推理最高 200B 参数的模型
4. **数据科学** - 高性能数据科学工作
5. **边缘应用** - 开发边缘 AI 应用

## 价格

- **未公开官方价格**
- 社区讨论估计：$2,000-3,000
- 需要通过 NVIDIA Marketplace 购买

## 性能评估（来自社区）

- **推理速度：** 比 M4 Max 慢（ARM 架构限制）
- **适用场景：** 原型开发、模型微调
- **不适合：** 生产环境的实时推理
- **优势：** 紧凑、功耗低、预装软件完整
