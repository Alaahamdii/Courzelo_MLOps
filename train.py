import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from jinja2 import Template

# Load the CSV file
data = pd.read_csv('Courzello_DB.Course.csv')

# Select relevant columns
selected_columns = ['Price', 'Category', 'Language', 'Required Score', 'Numbers of Attendee']
filtered_data = data[selected_columns]

# One-hot encode the categorical features
encoded_data = pd.get_dummies(filtered_data.drop(columns=['Numbers of Attendee']), columns=['Category', 'Language'])

# Define the features and target variable
X = encoded_data
y = filtered_data['Numbers of Attendee']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the entire dataset
predictions = model.predict(X)

# Calculate regression metrics
mse = mean_squared_error(y, predictions)
r2 = r2_score(y, predictions)

# Add predictions to the original data
filtered_data['Predicted Number of Attendees'] = predictions

# Sort the data by the predicted number of attendees in descending order
sorted_data = filtered_data.sort_values(by='Predicted Number of Attendees', ascending=False)

# Create an HTML report
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Course Attendance Prediction Report</title>
</head>
<body>
    <h1>Course Attendance Prediction Report</h1>
    <h2>Model Performance</h2>
    <p>Mean Squared Error (MSE): {{ mse }}</p>
    <p>R² Score: {{ r2 }}</p>
    <h2>Top Courses by Predicted Number of Attendees</h2>
    <table border="1">
        <tr>
            <th>Price</th>
            <th>Category</th>
            <th>Language</th>
            <th>Required Score</th>
            <th>Predicted Number of Attendees</th>
        </tr>
        {% for index, row in top_courses.iterrows() %}
        <tr>
            <td>{{ row['Price'] }}</td>
            <td>{{ row['Category'] }}</td>
            <td>{{ row['Language'] }}</td>
            <td>{{ row['Required Score'] }}</td>
            <td>{{ row['Predicted Number of Attendees'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Select the top 10 courses
top_courses = sorted_data.head(10)

# Render the HTML
template = Template(html_template)
html_content = template.render(mse=mse, r2=r2, top_courses=top_courses)

# Write the HTML to a file
with open('course_attendance_report.html', 'w') as f:
    f.write(html_content)

print("Report generated: course_attendance_report.html")
