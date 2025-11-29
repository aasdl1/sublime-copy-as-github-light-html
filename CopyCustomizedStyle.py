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

        # --- 1. 获取选中文本 ---
        selections = self.view.sel()
        text_to_copy = ""
        has_selection = False
        
        # 优化：使用列表推导式拼接字符串比 += 更快且更省内存（对于超大文本）
        fragments = [self.view.substr(r) for r in selections if not r.empty()]
        if not fragments:
             sublime.status_message("⚠️ Unselected Text")
             return
        
        text_to_copy = "\n".join(fragments) # 用 join 替代 +=

        panel_name = "ghost_copier_panel"
        
        # 1. 先清理可能的残留（入口清理）
        window.destroy_output_panel(panel_name) 

        # 2. 开始创建和操作
        try:
            panel = window.create_output_panel(panel_name)
            
            # 写入文本
            panel.run_command('append', {'characters': text_to_copy})

            # 同步语法
            current_syntax = self.view.settings().get('syntax')
            if current_syntax:
                panel.assign_syntax(current_syntax)

            # 设置样式
            settings = panel.settings()
            settings.set('color_scheme', EXPORT_THEME)
            settings.set('font_face', EXPORT_FONT)
            settings.set('font_size', EXPORT_SIZE)
            settings.set('line_numbers', False)
            settings.set('gutter', False)
            settings.set('word_wrap', False)

            # 全选并复制
            panel.sel().clear()
            panel.sel().add(sublime.Region(0, panel.size()))
            panel.run_command('copy_as_html', {'enclosing_tags': True})
            
            # theme_base, _ = os.path.splitext("GitHub_Light_AAS.sublime-color-scheme")
            sublime.status_message("✅ Copied with own style")

        except Exception as e:
            # 万一出错了，打印日志
            print(f"Ghost Copy Error: {e}")
            sublime.status_message("❌ Copy Failed, Please check the console")
            
        finally:
            # 3. 无论成功还是失败，只要面板被创建了，最后一定要销毁！
            # 这就是“防泄漏”的终极防线
            window.destroy_output_panel(panel_name)

