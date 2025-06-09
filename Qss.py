class SharedStyle:
    @staticmethod
    def applyStyle(widget):  # 按钮变化
        widget.setStyleSheet("""#pushButton_create_user{
                                background-color: rgb(0, 0, 0);
                                color: rgb(255, 255, 255);
                                border: 3px solid rgb(0,0,0);
                                border-radius:10px
                            }
                                #pushButton_create_user:hover{
                            
                                color: rgb(0, 0, 0);
                                background-color: rgb(255, 255, 255);
                            }
                                #pushButton_create_user:pressed{
                                padding-top:5px;
                                padding-left:5px
                            }
                            """)

    @staticmethod
    def textStyle(widget):
        widget.setStyleSheet("""
                                border:2px solid rgb(186,186,186);
                                border-radius:10px
                            """)

    @staticmethod
    def selectStyle(widget):
        widget.setStyleSheet("""#comboBox_project{
                                border-radius:11px;
                                background-color: rgb(184, 184, 184);
                                color: rgb(56,56,56);
                            }
                                #comboBox_project:hover{
                                border-radius:0px;
                                background-color: rgb(184, 184, 184);
                                border-top-left-radius:10px;
                                border-top-right-radius:10px;
                                border-bottom-right-radius:10px;
                                color: rgb(56,56,56);
                            }
                                #comboBox_project::drop-down{
                                border-top-right-radius:5px;
                                border-bottom-right-radius:5px;
                                background-color: rgb(40, 40, 40);
                                color: rgb(40,40,40);
                                min-width:30px;
                            }
                                #comboBox_project::down-arrow{
                                image: url(:/icons/arrow-down-filling.png);
                                height:18px;
                                width:18px;
                            }
                            
                            """)

    @staticmethod
    def menuBar(widget):  # 菜单栏样式
        widget.setStyleSheet("""
                                QTabWidget::tab-bar {
                                    alignment: left; /* 将选项卡栏左对齐 */
                                    background-color: #f2f2f2;
                                    border: none;
                                    border-bottom: 1px solid #ccc;
                                    padding: 5px;
                                }
                                QTabBar::tab {
                                    background-color: #e0e0e0;
                                    border: none;
                                    border-top-left-radius: 4px;
                                    border-top-right-radius: 4px;
                                    padding: 8px 12px;
                                    margin-right: 2px;
                                    font-weight: bold;
                                    color: #333;
                                }
                                QTabBar::tab:selected {
                                    background-color: #fff;
                                    border-bottom: 2px solid #555;
                                    color: #555;
                                }
                                QTabBar::tab:!selected:hover {
                                    background-color: #ccc;
                                    color: #555;
                                }
                                QTabWidget::pane {
                                    border: 1px solid #ccc;
                                    background-color: #fff;
                                }
                            """)
