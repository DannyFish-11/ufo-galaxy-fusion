# ADLINK Pocket AI (RTX A500) 规格和性能

## 核心规格

| 规格项 | 参数 |
|-------|------|
| **GPU** | NVIDIA RTX A500 (Ampere GA107) |
| **VRAM** | 4 GB GDDR6 |
| **CUDA Cores** | 2,048 |
| **Tensor Cores** | 64 |
| **RT Cores** | 16 |
| **AI 性能** | 100 TOPS (DENSE INT8 inference) |
| **FP32 性能** | 6.54 TFLOPS |
| **内存带宽** | 96 GB/s |
| **功耗** | 25W |
| **接口** | Thunderbolt 3.0 (PCIe 3.0 x4) |
| **尺寸** | 106 x 72 x 25 mm |
| **重量** | 250g |
| **供电** | USB-C PD 3.0（15V/40W+）|

## 系统要求

**必须：**
- Thunderbolt 3 或更高版本（支持 eGPU）
- Windows 10/11 或 Linux Ubuntu
- 支持 Resizable BAR
- USB-C PD 适配器（15V/40W+）

**不支持：**
- ❌ macOS
- ❌ 菊花链（Daisy Chain）
- ❌ Linux 热插拔

## LLM 性能估算

**基于 RTX A500 的规格：**
- VRAM：4GB（足够运行 3B-4B 模型）
- CUDA Cores：2,048（约为 RTX 4060 的 1/2）
- 内存带宽：96 GB/s（约为 RTX 4060 的 1/2）

**预估性能（8B Q4_K_M 模型）：**
- 文本生成速度：**25-35 tokens/s**（约为 RTX 4060 的 50%）
- 相对 M4 Max：**30-35%**

**支持的模型规模：**
- ✅ 3B 模型（流畅，25-35 tokens/s）
- ✅ 4B 模型（流畅，20-30 tokens/s）
- ⚠️ 8B 模型（需要量化，10-15 tokens/s）
- ❌ 13B+ 模型（VRAM 不足）

## 优势

1. ✅ **极致便携**
   - 尺寸：106 x 72 x 25 mm（约一副扑克牌大小）
   - 重量：250g
   - 可以放在口袋里

2. ✅ **即插即用**
   - Thunderbolt 3 连接
   - 无需外接电源（USB-C PD 供电）

3. ✅ **功耗低**
   - 仅 25W
   - 可以用充电宝供电

4. ✅ **价格相对便宜**
   - 估计 $300-500

## 劣势

1. ❌ **VRAM 有限**
   - 只有 4GB
   - 无法运行 8B+ 模型

2. ❌ **性能有限**
   - 约为 RTX 4060 的 50%
   - 约为 M4 Max 的 30-35%

3. ⚠️ **需要 Thunderbolt 3+**
   - 华为轻薄笔记本可能不支持
   - 需要检查

4. ⚠️ **不支持 macOS**
   - 只支持 Windows 和 Linux

## 价格

- **估计：** $300-500
- **购买渠道：** ADLINK 官网、Amazon、eBay

## 适用场景

- ✅ 运行小型模型（3B-4B）
- ✅ AI 开发和测试
- ✅ 图像处理和视频编辑
- ⚠️ 不适合大型 LLM（8B+）
