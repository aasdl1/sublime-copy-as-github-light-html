import sublime
import sublime_plugin

class CopyCustomizedStyleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # ================= 配置区域 =================
        # EXPORT_THEME = "GitHub Light.sublime-color-scheme"
        # 常用：Github Light / GitHub Light High Contrast / (Packages/Github Color Theme/GitHub.tmTheme) / One Light
        # My own designed based Github Light called "Github_Light_AAS"
        EXPORT_THEME = "GitHub_Light_AAS.sublime-color-scheme"
        
        # 2. 设置字体: 强制 Consolas 以对抗 OneNote 的字体清洗
        EXPORT_FONT = "Consolas"
        EXPORT_SIZE = 11
        # ===========================================

        window = self.view.window()
        
        # --- 1. 获取选中文本 (支持多光标) ---
        selections = self.view.sel()
        text_to_copy = ""
        has_selection = False
        
        for region in selections:
            if not region.empty():
                has_selection = True
                text_to_copy += self.view.substr(region) + "\n"
        
        # 去除末尾多余换行
        text_to_copy = text_to_copy.rstrip()

        # 如果用户什么都没选，就不执行（避免误操作）
        if not has_selection or not text_to_copy:
            sublime.status_message("⚠️ Unselected Text")
            return

        # --- 2. 创建隐形面板 (Ghost Panel) ---
        panel_name = "ghost_copier_panel"
        # 销毁可能残留的旧面板
        window.destroy_output_panel(panel_name) 
        panel = window.create_output_panel(panel_name)

        # --- 3. 写入文本 ---
        panel.run_command('append', {'characters': text_to_copy})

        # --- 4. 同步语法高亮 ---
        current_syntax = self.view.settings().get('syntax')
        if current_syntax:
            panel.assign_syntax(current_syntax)

        # --- 5. 应用样式配置 ---
        settings = panel.settings()
        settings.set('color_scheme', EXPORT_THEME)
        settings.set('font_face', EXPORT_FONT)
        settings.set('font_size', EXPORT_SIZE)
        
        # 关键：关闭所有可能干扰复制的 UI 元素
        settings.set('line_numbers', False)
        settings.set('gutter', False)
        settings.set('word_wrap', False) # 防止窄屏自动换行影响代码格式

        # --- 6. 核心：后台全选并复制 ---
        # 必须选中面板内的内容，copy_as_html 才能工作
        panel.sel().clear()
        panel.sel().add(sublime.Region(0, panel.size()))

        # 执行原生复制，enclosing_tags 保证字体样式被包裹
        panel.run_command('copy_as_html', {'enclosing_tags': True})

        # --- 7. 清理 ---
        window.destroy_output_panel(panel_name)
        sublime.status_message(f"✅ Copied with own style ({EXPORT_FONT})")