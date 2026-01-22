# GIGABYTE AORUS RTX 5060 Ti AI BOX 规格和性能

## 核心规格

| 规格项 | 参数 |
|-------|------|
| **GPU** | NVIDIA GeForce RTX 5060 Ti 16GB (Blackwell架构) |
| **VRAM** | 16 GB GDDR7 |
| **GPU 时钟** | 2572 MHz |
| **内存时钟** | 28 Gbps |
| **接口** | Thunderbolt 5 (PCIe 4.0 x4, 80Gbps) |
| **功耗** | 330W（电源适配器）|
| **尺寸** | 243.7 x 117.4 x 48.2 mm |
| **重量** | 955g（不含支架）|
| **供电** | 20V/16.5A（330W 电源适配器）|

## I/O 接口

**Thunderbolt 5：**
- 1x Thunderbolt 5 Type-C（连接 PC）
- 1x Thunderbolt 5 Type-C（连接外设，支持 USB4 V2.0 和 PD 3.0）

**USB：**
- 1x USB 3.2 Gen 2 Type-C
- 2x USB 3.2 Gen 2 Type-A

**其他：**
- 1x 以太网端口
- 3x DisplayPort 2.1b
- 1x HDMI 2.1b

**充电：**
- 支持 PD 3.0，最高 100W 笔记本充电

## 系统要求

**必须：**
- 笔记本/台式机带 Thunderbolt 端口，支持外接 GPU
- 确认 Thunderbolt 5 兼容性
- Microsoft Windows 11 version 25H2 或更高

**不支持：**
- ❌ macOS（未明确说明，但 GIGABYTE 通常不支持）

## LLM 性能估算

**基于 RTX 5060 Ti 16GB 的规格：**
- VRAM：16GB（足够运行 13B 模型）
- 架构：Blackwell（最新一代）
- 内存：GDDR7（最快）

**预估性能（8B Q4_K_M 模型）：**
- 文本生成速度：**60-80 tokens/s**（与 RTX 4060 相当或略好）
- 相对 M4 Max：**60-80%**

**支持的模型规模：**
- ✅ 3B-4B 模型（非常流畅，80-100 tokens/s）
- ✅ 8B 模型（流畅，60-80 tokens/s）
- ✅ 13B 模型（可用，30-50 tokens/s）
- ⚠️ 20B+ 模型（需要量化，15-25 tokens/s）

## 优势

1. ✅ **大 VRAM**
   - 16GB GDDR7
   - 可以运行 13B 模型
   - 最新的 GDDR7 内存

2. ✅ **Thunderbolt 5**
   - 80Gbps 带宽（是 TB3 的 2 倍）
   - 接近桌面级性能
   - 支持菊花链

3. ✅ **完整的 I/O**
   - 3x USB 端口
   - 以太网端口
   - 100W 笔记本充电

4. ✅ **最新架构**
   - NVIDIA Blackwell
   - 支持 DLSS 4

## 劣势

1. ❌ **体积较大**
   - 243.7 x 117.4 x 48.2 mm
   - 955g（比 Pocket AI 重 4 倍）
   - 不能放在口袋里

2. ❌ **需要外接电源**
   - 330W 电源适配器
   - 不能用充电宝供电

3. ⚠️ **需要 Thunderbolt 5**
   - 华为轻薄笔记本可能不支持
   - 需要检查

4. ⚠️ **价格较高**
   - 估计 $800-1200（RTX 5060 Ti 16GB + 外壳 + 电源）

## 价格估算

**组件成本：**
- RTX 5060 Ti 16GB：$500-700
- eGPU 外壳 + 电源：$300-500
- **总计：** $800-1200

**购买渠道：**
- GIGABYTE 官网
- Amazon
- Newegg

## 适用场景

- ✅ 运行中大型模型（8B-13B）
- ✅ 游戏（1080p-2K）
- ✅ 创意工作（3D 渲染、视频编辑）
- ✅ AI 应用（本地运行）
- ✅ 适合固定场所使用（桌面）
- ⚠️ 不适合移动使用（体积大、需要电源）

## 与 Pocket AI 对比

| 特性 | Pocket AI (RTX A500) | AORUS RTX 5060 Ti AI BOX |
|------|---------------------|-------------------------|
| **VRAM** | 4GB GDDR6 | 16GB GDDR7 |
| **性能** | 低（25-35 tokens/s）| 高（60-80 tokens/s）|
| **便携性** | ✅ 极佳（250g）| ❌ 一般（955g）|
| **供电** | ✅ USB-C PD（40W）| ❌ 电源适配器（330W）|
| **价格** | ✅ 低（$300-500）| ❌ 高（$800-1200）|
| **适用场景** | 移动、轻度使用 | 固定、重度使用 |
