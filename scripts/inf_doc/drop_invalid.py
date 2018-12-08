import pandas as pd
import json

from backend.models import EvaluationResult
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy(app)

    results = db.session.query(EvaluationResult).all()
    for result in results:
        validity = result.validity
        if result.precision == result.recall:
            validity = False
        if result.precision == -1 or result.recall == -1:
            validity = False
        if not validity:
            db.session.delete(result)
            db.session.commit()
