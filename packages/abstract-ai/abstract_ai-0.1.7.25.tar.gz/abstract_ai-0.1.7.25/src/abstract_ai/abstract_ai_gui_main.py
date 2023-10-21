from .abstract_browser import AbstractBrowser
from .abstract_ai_gui_layout import get_total_layout
from .abstract_ai_gui_backend import GptManager
gpt_mgr = GptManager()
gpt_mgr.while_window()
