class Styles:
    DARK_THEME = """
    QMainWindow {
        background-color: #383838;
        border: 1px solid #383838;
    }

    QTabWidget {
        background-color: #252526;
        color: #e9e9e9;
        border: none;
    }

    QTabWidget::pane {
        border: 1px transparent;
        background-color: #252526;
        padding: 1px
    }

    QTabBar {
        background-color: #1e1e1e;
    }

    QTabBar::tab {
        background-color: #1e1e1e;
        color: #e9e9e9;
        padding: 3px 18px;
        margin-right: 1px;
        margin-left: 1px;
        border: 1px;
        border-top-left-radius: 1px;
        border-top-right-radius: 1px;
        background-clip: border;
        min-width: 100px;
        text-align: center;
        font-weight: 500;
    }

    /* Add more style rules here */
    """
