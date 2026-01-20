package com.ufo.galaxy.client

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // 启动悬浮窗服务
        val intent = Intent(this, FloatingWindowService::class.java)
        startService(intent)
        
        // 关闭主 Activity（悬浮窗会保持运行）
        finish()
    }
}
