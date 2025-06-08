"""Tool definitions and handlers."""

from .stock import query_stock_price
from .chart import draw_plotly_chart
from .image import generate_image_tool
from .search import internet_search
from .linkedin import draft_linkedin_post
from .python_file import create_python_file, execute_python_file
from .browser import open_browser
from .database import execute_sql
from .email import draft_email

tools = [
    query_stock_price,
    draw_plotly_chart,
    generate_image_tool,
    internet_search,
    draft_linkedin_post,
    create_python_file,
    execute_python_file,
    open_browser,
    execute_sql,
    draft_email,
]

__all__ = ["tools"]
