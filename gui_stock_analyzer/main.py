import sys
import yfinance as yf
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextBrowser, QComboBox, QPlainTextEdit
import numpy as np

class StockAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color:gray')
        self.setFixedHeight(900)
        self.setFixedWidth(1700)
        self.setWindowTitle("Stock Analyzer App")
        

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.central_widget.addTab(self.tab1, "Enter Stock")
        self.central_widget.addTab(self.tab2, "Analysis Results")

        self.create_tab1_ui()
        self.create_tab2_ui()

    def create_tab1_ui(self):
        layout = QVBoxLayout()
        self.stock_input = QLineEdit()
        analyze_button = QPushButton("Analyze")

        layout.addWidget(self.stock_input)
        layout.addWidget(analyze_button)

        self.tab1.setLayout(layout)

        analyze_button.clicked.connect(self.analyze_stock)

    def create_tab2_ui(self):
        layout = QVBoxLayout()
        self.analysis_result = QTextBrowser()

                # Create three QPlainTextEdit fields
        self.month_data_text = QPlainTextEdit()
        self.year_data_text = QPlainTextEdit()
        self.name_text = QPlainTextEdit()

        # Set placeholders for the fields
        self.month_data_text.setPlaceholderText("1-Month Data")
        self.year_data_text.setPlaceholderText("1-Year Data")
        self.name_text.setPlaceholderText("Your Name")

        # Create two Matplotlib canvases within the second tab
        self.plot_widget_1m = pg.PlotWidget(title='Stock Prices for the Past Month')
        self.plot_widget_1yr = pg.PlotWidget(title='Stock Prices for the Past Year')

        # Create a dropdown to select the graph
        self.graph_selector = QComboBox()
        self.graph_selector.addItem("1 Month")
        self.graph_selector.addItem("1 Year")
        self.graph_selector.currentIndexChanged.connect(self.update_graph)

        
        layout.addWidget(self.month_data_text)
        layout.addWidget(self.year_data_text)
        layout.addWidget(self.name_text)

   
        layout.addWidget(self.graph_selector)
        layout.addWidget(self.plot_widget_1m)
        layout.addWidget(self.plot_widget_1yr)
        self.tab2.setLayout(layout)

        # Initially hide the 1-year graph
        self.plot_widget_1yr.hide()

    def analyze_stock(self):
        stock_symbol = self.stock_input.text()
        if stock_symbol:
            try:
                stock_data = yf.Ticker(stock_symbol)
                history_1month = stock_data.history(period="1mo")
                history_1yr = stock_data.history(period="12mo")
                prices_close_1mo = history_1month["Close"]
                prices_close_1yr = history_1yr["Close"]
                dates_1mo = prices_close_1mo.index
                dates_1yr = prices_close_1yr.index

                # Display the prices and dates
                result_text_1mo = "Date\tClose Price\n"
                for date, price in zip(dates_1mo, prices_close_1mo):
                    result_text_1mo += f"{date.strftime('%m-%d')}\t{price:.2f}\n"
                
                result_text_1yr = "Date\tClose Price\n"
                for date, price in zip(dates_1yr, prices_close_1yr):
                    result_text_1yr += f"{date.strftime('%Y-%m-%d')}\t{price:.2f}\n"

                self.month_data_text.setPlainText(result_text_1mo)
                self.year_data_text.setPlainText(result_text_1yr)

                # Generate and display the graphs for the past month and past year
                self.graph_1m(dates_1mo, prices_close_1mo)
                self.graph_1yr(dates_1yr, prices_close_1yr)

            except Exception as e:
                self.analysis_result.setPlainText(f"Error: {str(e)}")
        else:
            self.analysis_result.setPlainText("Please enter a stock ticker.")
    
    def update_graph(self):
        selected_index = self.graph_selector.currentIndex()
        if selected_index == 0:
            # Show the 1-month graph and hide the 1-year graph
            self.plot_widget_1m.show()
            self.plot_widget_1yr.hide()
        else:
            # Show the 1-year graph and hide the 1-month graph
            self.plot_widget_1m.hide()
            self.plot_widget_1yr.show()


    def graph_1m(self, dates, prices_close):
        x = np.arange(len(dates))  # Create a numerical X-axis

        # Clear previous plot
        self.plot_widget_1m.clear()

        # Create and display the pyqtgraph plot for one month of data
        self.plot_widget_1m.plot(x, prices_close, pen='b', name='Stock Prices')
        self.plot_widget_1m.setLabel('left', 'Price', units='USD')
        
        # Format the X-axis labels
        axis = self.plot_widget_1m.getAxis('bottom')
        axis_ticks = self.plot_widget_1m.getAxis('bottom')
        axis.setTicks([[(i, date.strftime('%m-%d')) for i, date in enumerate(dates)]])
        
        self.plot_widget_1yr.showGrid(x=True, y=True)

    def graph_1yr(self, dates, prices_close):
        x = np.arange(len(dates))  # Create a numerical X-axis

        # Clear previous plot
        self.plot_widget_1yr.clear()

        # Create and display the pyqtgraph plot for one year of data
        self.plot_widget_1yr.plot(x, prices_close, pen='r', name='Stock Prices')
        self.plot_widget_1yr.setLabel('left', 'Price', units='USD')
        
        # Format the X-axis labels
        axis = self.plot_widget_1yr.getAxis('bottom')
        axis_ticks = self.plot_widget_1yr.getAxis('bottom')
        axis.setTicks([[(i, date.strftime('%m-%d')) for i, date in enumerate(dates)]])
        
        self.plot_widget_1yr.showGrid(x=True, y=True)

def main():
    app = QApplication(sys.argv)
    window = StockAnalyzerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
