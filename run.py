import time
from sqlalchemy.exc import OperationalError # type: ignore
from app import create_app, db
import os
from flask import jsonify

app = create_app()

# Add health check endpoint
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    # Get port from environment variable with fallback
    port = int(os.environ.get('PORT', 8000))
    
    # Log the DB URI for debugging
    db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
    print(f"[DEBUG] SQLALCHEMY_DATABASE_URI: {db_uri}")
    print(f"[DEBUG] Starting app on port {port}")
    
    # Wait for MySQL to be ready
    with app.app_context():
        for _ in range(10):
            try:
                db.create_all()
                break
            except OperationalError as e:
                print(f"⏳ Waiting for database to be ready... {e}")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Unexpected error during DB setup: {e}")
                time.sleep(2)
        else:
            print("❌ Database did not become available in time.")

    try:
        app.run(host="0.0.0.0", port=port, debug=False)
    except Exception as e:
        print(f"❌ Flask app failed to start: {e}")