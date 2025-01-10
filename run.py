from app import create_app  # Import the application factory function

# Create the Flask app instance
app = create_app()

# Only run the app if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)