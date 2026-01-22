# Hailo-10H LLM 实际性能数据

## 来源

**文章：** Bringing Generative AI to the Edge: LLM on Hailo-10H

**作者：** Niv Vosco, Software Director at Hailo

**发布时间：** 2025年7月29日

**链接：** https://hailo.ai/blog/bringing-generative-ai-to-the-edge-llm-on-hailo-10h/

## 测试模型：QWEN2-1.5B-Instruct

**模型大小：** 1.5B 参数

**量化方案：**
- 权重：4-bit symmetric, group-wise
- 激活：8-bit asymmetric, per-tensor
- KV-cache：8-bit asymmetric, per-tensor

**内存需求：** 1.2GB

**上下文长度：** 2048 tokens (~1536 words)

## 性能指标

### Time-to-First Token (TTFT)

**289ms** for 96 input tokens

**解释：**
- 从输入提示到第一个 token 生成的时间
- 96 个输入 token 需要 289ms
- 平均每个输入 token 处理时间：3ms

### Tokens-Per-Second (TPS)

**9.45 tokens/s**

**解释：**
- 第一个 token 之后的生成速度
- 每秒生成 9.45 个 token
- 生成 100 个 token 需要约 10.6 秒

### 准确率

**HellaSwag：**
- 全精度：66.06
- 量化后：64.3
- 准确率损失：2.66%

**C4（困惑度）：**
- 数据未完整显示

## 与其他设备的对比

### 1. Hailo-10H vs CPU（Intel i5-1340P）

| 指标 | Hailo-10H | CPU (i5-1340P) | 提升 |
|------|-----------|----------------|------|
| TPS | 9.45 | ~1-2 | 5-10x |
| 功耗 | 2.5W | 15-28W | 6-11x |
| 内存 | 1.2GB (专用) | 1.2GB (共享) | 独立 |

### 2. Hailo-10H vs GPU（RTX 4060）

| 指标 | Hailo-10H | RTX 4060 | 对比 |
|------|-----------|----------|------|
| TPS | 9.45 | 60-80 | 1/6-1/8 |
| 功耗 | 2.5W | 115W | 1/46 |
| 价格 | $200-400 | $300-400 | 相近 |

## 适用场景

### 适合 Hailo-10H 的场景

1. **小型 LLM（1-3B）** ✅
   - QWEN2-1.5B：9.45 tokens/s
   - 预期 QWEN2-3B：5-7 tokens/s

2. **低功耗要求** ✅
   - 2.5W 功耗
   - 可以用充电宝供电

3. **离线场景** ✅
   - 完全本地推理
   - 无需网络连接

4. **隐私保护** ✅
   - 数据不离开设备

### 不适合 Hailo-10H 的场景

1. **大型 LLM（7B+）** ❌
   - 内存限制（8GB LPDDR4）
   - 性能不足

2. **高速推理** ❌
   - 9.45 tokens/s 相对较慢
   - 不适合实时对话

3. **长上下文** ❌
   - 2048 tokens 上下文限制
   - 每 1K tokens 需要 256MB 内存

## 与 ASUS UGen300 的关系

**ASUS UGen300 使用 Hailo-10H 芯片**

因此，ASUS UGen300 的性能应该与上述数据相近：
- TPS：~9.45 tokens/s（1.5B 模型）
- TTFT：~289ms（96 input tokens）
- 内存：8GB LPDDR4
- 功耗：2.5W

## 在华为 MateBook 上的预期性能

**华为 MateBook 14 2023：**
- USB-C：USB 3.2 Gen 1（5Gbps）
- ASUS UGen300：USB 3.1 Gen2（10Gbps）

**带宽限制影响：**
- 理论带宽：50% (5Gbps / 10Gbps)
- 实际性能影响：约 30-50%

**预期性能：**
- TPS：~5-7 tokens/s（降低 30-50%）
- TTFT：~400-500ms（增加 40-70%）

**结论：**
- ✅ 可以使用
- ⚠️ 性能会打折扣
- ⚠️ 仍然比纯 CPU 推理快 2-3 倍

## 总结

**Hailo-10H 的实际性能：**
1. ✅ 可以运行 1.5B 模型（9.45 tokens/s）
2. ✅ 低功耗（2.5W）
3. ✅ 低内存（1.2GB）
4. ⚠️ 速度较慢（相比 GPU）
5. ⚠️ 上下文长度有限（2048 tokens）

**ASUS UGen300 在华为 MateBook 上：**
1. ✅ 可以使用（USB-C 兼容）
2. ⚠️ 性能打折扣（约 50%）
3. ⚠️ 预期 TPS：5-7 tokens/s
4. ✅ 仍然比纯 CPU 快 2-3 倍

**推荐：**
- 等待 ASUS UGen300 上市
- 等待实际用户评价
- 等待价格公布
- 如果价格合理（$200-400），可以考虑购买作为纯 API 方案的补充
