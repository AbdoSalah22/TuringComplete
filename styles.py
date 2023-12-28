# Set a common stylesheet for the buttons
button_stylesheet = (
    "QPushButton {"
    "    background-color: #4CAF50;"
    "    border: none;"
    "    color: white;"
    "    padding: 15px 32px;"
    "    text-align: center;"
    "    font-size: 16px;"
    "    margin: 4px 2px;"
    "}"
    "QPushButton:hover {"
    "    background-color: #45a049;"
    "}"
)

# Set a common stylesheet for QLineEdit and QComboBox
widget_stylesheet = (
    "QLineEdit, QComboBox {"
    "    background-color: #f2f2f2;"
    "    border: 1px solid #ccc;"
    "    padding: 10px;"
    "    margin: 4px 2px;"
    "    font-size: 18px;"
    "    color: #333;"
    "}"
    "QComboBox::drop-down {"
    "    border: 1px solid #ccc; /* Light gray border */"
    "    width: 20px; /* Set width of the drop-down arrow */"
    "    background-color: #f2f2f2; /* Light gray background */"
    "}"
)

title_stylesheet = (
    "QLabel {"
    "    background-color: #45a049; /* Blue background */"
    "    color: white; /* White text color */"
    "    font-size: 32px; /* Larger font size */"
    "    padding: 10px;"
    "    border-radius: 10px; /* Rounded corners */"
    "}"
)

accepted_stylesheet = (
    "QLabel {"
    "    color: #45a049;"
    "    font-size: 16px;"
    "    qproperty-alignment: AlignCenter;"
    "    font-weight: bold;"
    "}"
)

rejected_stylesheet = (
    "QLabel {"
    "    color: #FF0000;"
    "    font-size: 16px;"
    "    qproperty-alignment: AlignCenter;"
    "    font-weight: bold;"
    "}"
)

hide_stylesheet = (
    "QLabel {"
    "    color: #FFF;"
    "    font-size: 16px; /* Larger font size */"
    "}"
)