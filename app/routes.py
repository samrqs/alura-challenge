import json

from app.models import Feedback, Classification
from .extensions import db

from flask import Blueprint
from flask import request, jsonify
from classifier import sentiment_classifier

main_bp = Blueprint("main", __name__)

@main_bp.route("/feedbacks", methods=["POST"])
def classifier():
    data = request.json
    feedback = data.get("feedback")

    if not feedback:
        return jsonify({"erro": "Feedback is required"}), 400
    
    novo_feedback = Feedback(
        feedback_text=feedback,
    )
    
    db.session.add(novo_feedback)
    db.session.commit()

    result = json.loads(sentiment_classifier(feedback))

    sentiment = result.get("sentiment")
    features = result.get("requested_features", [])

    classifications = []
    for feature in features:
        classification = Classification(
            sentiment=sentiment,
            code=feature["code"],
            reason=feature["reason"],
            feedbacks_id=novo_feedback.id
        )
        db.session.add(classification)
        classifications.append(classification)

    db.session.commit()

    return jsonify({
        "feedback_id": str(novo_feedback.id),
        "sentiment": sentiment,
        "requested_features": [
            {
                "code": classification.code,
                "reason": classification.reason
            } 
        ]
    }), 201
